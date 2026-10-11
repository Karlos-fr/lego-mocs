"""Offline preview of the actual LDraw geometry; no Studio UI automation."""
from functools import lru_cache
from pathlib import Path
import re
import numpy as np
from PIL import Image, ImageDraw
from audit_moc import ROOT, parse, resolve

COLORS = {}
for line in (ROOT/'LDConfig.ldr').read_text().splitlines():
    m = re.search(r'CODE\s+(\d+)\s+VALUE\s+#([0-9A-Fa-f]{6})', line)
    if m: COLORS[int(m[1])] = tuple(bytes.fromhex(m[2]))

@lru_cache(None)
def mesh(ref):
    ref = ref.replace('\\','/')
    p = resolve(ref)
    faces, colors = [], []
    for line in p.read_text(errors='replace').splitlines():
        t=line.split()
        if not t: continue
        if t[0]=='1':
            f,c = mesh(' '.join(t[14:]))
            if not len(f): continue
            m=np.array(t[5:14],float).reshape(3,3)
            faces.append(f@m.T+np.array(t[2:5],float))
            colors.append(np.where(c==16,int(t[1]),c))
        elif t[0] in ('3','4'):
            v=np.array(t[2:],float).reshape(-1,3)
            faces.append(v[[0,1,2]][None,:,:]); colors.append(np.array([int(t[1])]))
            if t[0]=='4':
                faces.append(v[[0,2,3]][None,:,:]); colors.append(np.array([int(t[1])]))
    return (np.concatenate(faces),np.concatenate(colors)) if faces else (np.empty((0,3,3)),np.empty(0,int))

def render(parts,path,view='front',size=(1100,1100)):
    allfaces,allcolors=[],[]
    for p in parts:
        f,c=mesh(p['ref']); allfaces.append(f@p['m'].T+p['p']);allcolors.append(np.where(c==16,p['color'],c))
    f=np.concatenate(allfaces); c=np.concatenate(allcolors)
    # y is down in LDraw. Camera front/right, or back/right for inspection.
    directions={'front':[.9,-.8,-1.3],'back':[.9,-.8,1.3],'bottom':[.9,.8,-1.3]}
    direction=np.array(directions[view]); direction/=np.linalg.norm(direction)
    right=np.cross([0,-1,0],direction);right/=np.linalg.norm(right)
    up=np.cross(direction,right)
    screen=f@np.array([right,up,direction]).T
    lo=screen[:,:,:2].min((0,1));hi=screen[:,:,:2].max((0,1));scale=min((np.array(size)-140)/(hi-lo))
    xy=(screen[:,:,:2]-(lo+hi)/2)*scale+np.array(size)/2
    xy[:,:,1]=size[1]-xy[:,:,1]
    n=np.cross(f[:,1]-f[:,0],f[:,2]-f[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-12)
    light=np.array([-1,-2,-1.5]);light/=np.linalg.norm(light)
    shade=.60+.40*np.abs(n@light)
    rgb=np.array([COLORS.get(int(k),(170,170,170)) for k in c],float)*shade[:,None]
    pixels=np.full((size[1],size[0],3),(235,240,244),dtype=np.uint8)
    depth=np.full((size[1],size[0]),-np.inf,dtype=np.float32)
    for i,tri in enumerate(xy):
        a,b,d=tri
        denominator=(b[1]-d[1])*(a[0]-d[0])+(d[0]-b[0])*(a[1]-d[1])
        if abs(denominator)<.05: continue
        left,top=np.maximum(np.floor(tri.min(0)).astype(int),0)
        rightmost,bottom=np.minimum(np.ceil(tri.max(0)).astype(int),np.array(size)-1)
        if left>rightmost or top>bottom:continue
        ys,xs=np.ogrid[top:bottom+1,left:rightmost+1]
        u=((b[1]-d[1])*(xs+.5-d[0])+(d[0]-b[0])*(ys+.5-d[1]))/denominator
        v=((d[1]-a[1])*(xs+.5-d[0])+(a[0]-d[0])*(ys+.5-d[1]))/denominator
        w=1-u-v
        z=u*screen[i,0,2]+v*screen[i,1,2]+w*screen[i,2,2]
        db=depth[top:bottom+1,left:rightmost+1]
        mask=(u>=-1e-6)&(v>=-1e-6)&(w>=-1e-6)&(z>db)
        db[mask]=z[mask];pixels[top:bottom+1,left:rightmost+1][mask]=rgb[i].astype(np.uint8)
    img=Image.fromarray(pixels);draw=ImageDraw.Draw(img)
    draw.text((22,20),'Apercu des pieces du fichier - rendu hors Studio',fill=(50,65,80))
    img.save(path)
    print(path,'triangles',len(f))

if __name__=='__main__':
    import sys
    from audit_moc import SOURCE
    source=Path(sys.argv[1]) if len(sys.argv)>1 else SOURCE
    render(parse(source),source.with_name(source.stem+'_apercu.png'))
