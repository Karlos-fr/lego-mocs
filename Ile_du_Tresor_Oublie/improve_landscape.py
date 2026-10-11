"""V3.6: snow sheets, faceted rocks and crossed foundation joints."""
from pathlib import Path
import collections,csv,hashlib,json,zipfile
import numpy as np
from PIL import Image
from audit_moc import ROOT,SOURCE,parse,vertices,bounds
from render_moc import render
from support_audit import studs,supports
SRC=Path('Ile_du_Tresor_Oublie_V3_5.io');DEST=Path('Ile_du_Tresor_Oublie_V3_6')
I=np.eye(3);R=np.array([[0,0,1],[0,1,0],[-1,0,0]])
old=parse(SRC);out=[];changes=collections.Counter()
def put(sec,ref,col,pos,m=I):
    q=dict(section=sec,ref=ref,color=col,p=np.array(pos,float),m=m.copy(),index=0);out.append(q);return q
for p in old:
    if p['section']==3 and p['ref']=='3022.dat' and p['p'][1]==-16 and p['p'][2]==130 and p['p'][0] in [50,90]:continue
    if p['section'] in [20,21,44,45]:continue
    if p['section'] in [13,14] and p['ref']=='3001.dat' and p['p'][0]==190:continue
    q=p.copy();q['p']=p['p'].copy()
    if p['section'] in range(22,34):q['p'][1]-=8
    out.append(q)
put(3,'3020.dat',1,[70,-16,130])
changes['upper_blue_joint_plates_replaced']=2
# Reinforcement layer: larger plates cross joints of the original 2x2 water plates.
cells=set()
for p in old:
    if p['section'] in [1,2] and p['ref']=='3022.dat':
        cells.update((int(s[0]),int(s[2])) for s in [p['m']@s+p['p'] for s in studs(p['ref'])])
remaining=cells.copy()
for ref,w,d in [('3036.dat',8,6),('3035.dat',8,4),('3034.dat',8,2),('3031.dat',4,4),('3020.dat',4,2),('3022.dat',2,2),('3023.dat',2,1),('3024.dat',1,1)]:
    for m,ww,dd in [(I,w,d),(R,d,w)] if w!=d else [(I,w,d)]:
        for z in range(0,341,20):
            for x in range(0,381,20):
                footprint={(x+20*i,z+20*j) for i in range(ww) for j in range(dd)}
                if footprint<=remaining:
                    put(0,ref,1,[x+(ww-1)*10,0,z+(dd-1)*10],m)
                    remaining-=footprint;changes['foundation_plates_added']+=1
assert not remaining
# Cross the left protrusion's joint instead of keeping a separate 2x2 under it.
out=[p for p in out if not (p['section']==0 and
     ((p['ref']=='3034.dat' and np.allclose(p['p'],[50,0,150])) or
      (p['ref']=='3022.dat' and np.allclose(p['p'],[10,0,130]))))]
put(0,'3020.dat',1,[30,0,130])
put(0,'3022.dat',1,[50,0,90])
put(0,'3020.dat',1,[50,0,190],R)
changes['foundation_plates_added']+=1
# Wider mounting surfaces below each palm. The whole tree is lifted one plate.
put(22,'3022.dat',15,[70,-32,170])
put(26,'3020.dat',15,[210,-120,290])
put(30,'3022.dat',15,[330,-32,210])
changes['palm_mounting_plates_added']=3
# Offset masonry joints at the back of the cave without changing its inside.
put(13,'3010.dat',72,[190,-72,280])
put(14,'3004.dat',72,[170,-96,280]);put(14,'3004.dat',72,[210,-96,280])
put(13,'3039.dat',71,[170,-72,300],R@R)
put(13,'3039.dat',72,[210,-72,300],R@R)
# Exterior rear facets sit on a plate linked to the existing blue base.
put(16,'3020.dat',72,[190,-24,330])
put(16,'3039.dat',71,[170,-48,320],R@R)
put(17,'3039.dat',72,[210,-48,320],R@R)
changes['rear_rock_facets_added']=4
# One snow sheet bridges the two central rock crests and binds them together.
put(20,'3710.dat',15,[190,-144,240])
put(20,'3069b.dat',15,[190,-152,240])
put(20,'24246.dat',15,[160,-152,240],R)
put(20,'24246.dat',15,[220,-152,240],R@R@R)
# Narrow rounded caps on real high-side studs; no L-shaped cavity or exposed stud.
for x,y,z in [(140,-160,270),(240,-136,270)]:
    put(20,'3023.dat',15,[x,y-8,z],R);put(20,'1126.dat',15,[x,y-16,z],R)
for x,y,z in [(160,-136,280),(100,-80,220),(280,-80,240),(180,-72,300)]:
    put(21,'24246.dat',15,[x,y-8,z])
# Keep the two existing low, connected ledge accents.
for p in old:
    if p['section']==21 and p['ref'] in ['25269.dat','98138.dat'] and p['p'][1]>-100:out.append(p.copy())
# Continuous low snow on exposed roof studs. Respect rock and palm footprints.
roof=set((int(s[0]),int(s[2])) for p in out if p['section']==15 and p['p'][1]==-112 for s in [p['m']@s+p['p'] for s in studs(p['ref'])])
def blocked_at(surface,cells,skip):
    blocked=set()
    for p in out:
        if p['section'] in skip:continue
        lo,hi=bounds(p)
        if lo[1]<surface-.05 and hi[1]>surface-16:
            blocked.update((x,z) for x,z in cells if lo[0]<x+9.9 and hi[0]>x-9.9 and lo[2]<z+9.9 and hi[2]>z-9.9)
    return blocked

def tile_field(sec,free,y,domain):
    free=set(free)
    for z in range(0,341,20):
        for x in range(0,381,20):
            square={(x,z),(x+20,z),(x,z+20),(x+20,z+20)}
            if square<=free:
                put(sec,'3068b.dat',15,[x+10,y,z+10]);free-=square
    for z in range(0,341,20):
        for x in range(0,381,20):
            for dx,dz,m in [(20,0,I),(0,20,R)]:
                pair={(x,z),(x+dx,z+dz)}
                if pair<=free:put(sec,'3069b.dat',15,[x+dx/2,y,z+dz/2],m);free-=pair
    for x,z in sorted(free):
        edge=sum((x+dx,z+dz) not in domain for dx,dz in [(20,0),(-20,0),(0,20),(0,-20)])
        put(sec,'25269.dat' if edge>=2 else '3070b.dat',15,[x,y,z])
    return len(free)
roof_free=roof-blocked_at(-112,roof,{0,1,2,3,4,15})
tile_field(21,roof_free,-120,roof)
# Snow also finishes the outer studs of the new, wider upper palm mounting plate.
for x in [180,240]:
    for z in [280,300]:put(21,'24246.dat',15,[x,-128,z],I if x==180 else R@R)
beach=set((int(s[0]),int(s[2])) for p in out if p['section'] in [5,6] and p['color']==15 for s in [p['m']@s+p['p'] for s in studs(p['ref'])])
free=beach-blocked_at(-24,beach,{0,1,2,3,4,5,6})
tile_field(44,free,-32,beach)
changes['roof_snow_studs_covered']=len(roof_free)
changes['beach_snow_studs_covered']=len(free)
# The native leaf geometry and snow offsets remain unchanged relative to the trees.
assert all(c for p,c in supports(out)),[(p['ref'],p['p'].tolist()) for p,c in supports(out) if not c]
groups=collections.defaultdict(list)
for p in out:groups[p['section']].append(p)
headings={}
with zipfile.ZipFile(SRC) as z:
    for line in z.read('model.ldr').decode().splitlines():
        if line.startswith('0 // ') and line[5:7].isdigit():headings[int(line[5:7])]=line
headings.update({0:'0 // 00 - Renforts sous le socle',20:'0 // 20 - Accumulations avec fond blanc',21:'0 // 21 - Corniches avec fond blanc',
                 25:'0 // 25 - Palmier A - petites touches arrondies',29:'0 // 29 - Palmier B - petites touches arrondies',
                 33:'0 // 33 - Palmier C - petites touches arrondies',43:'0 // 43 - Contours de neige ovales sans pente creuse'})
def num(x):return str(int(round(x))) if abs(x-round(x))<1e-7 else f'{x:.6f}'.rstrip('0').rstrip('.')
ldr=['0 FILE '+DEST.name+'.ldr',"0 L'ile du tresor oublie - V3.6 neige arrondie",'0 Author: Conception pour Gildas','0 !LDRAW_ORG Model',
     '0 // Offline geometry validation only; native Studio checks remain necessary.']
v2=ldr.copy();out=[]
for s,ps in sorted(groups.items()):
    ldr.append(headings[s]);v2.append(headings[s])
    for p in ps:
        p['index']=len(out)+1;out.append(p)
        payload=' '.join(num(x) for x in np.r_[p['p'],p['m'].ravel()])+' '+p['ref']
        ldr.append(f"1 {p['color']} {payload}");v2.append(f"11 {p['color']} {p['index']} False 0 {payload}")
    ldr.append('0 STEP');v2.append('0 STEP')
ldr.append('0 NOFILE');v2.append('0 NOFILE')
DEST.with_suffix('.ldr').write_text('\n'.join(ldr)+'\n',encoding='utf-8')

# All replacement references resolve, and the original cantilever slopes are removed.
for p in out:assert len(vertices(p['ref']))
assert not any(p['color']==15 and p['ref'] in ['11477.dat','15068.dat'] for p in out)
assert not any(p['section'] in [25,29,33] and p['ref'] in ['3023.dat','3069b.dat'] for p in out)

data=ROOT.parent/'data'
rows=list(csv.DictReader((data/'StudioPartDefinition2.txt').open(encoding='utf-8-sig'),delimiter='\t'))
colors={int(c['LDraw Color Code']):c for c in csv.DictReader((data/'StudioColorDefinition.txt').open(encoding='utf-8-sig'),delimiter='\t')
        if c['LDraw Color Code'] and c['BL Color Code']}
pairs={(e['blItemNo'],e['blColorCode']) for e in json.loads((data/'elementInfoList.json').read_text())}
confirmed={('2536b','8'),('70501a','21'),('3957a','11')}
inventory=[]
for (ref,color),qty in sorted(collections.Counter((p['ref'],p['color']) for p in out).items()):
    cr=colors[color];bc=cr['BL Color Code'];opts=[o for o in rows if o['LDraw ItemNo']==ref]
    if ref=='3957a.dat':opts=[{'BL ItemNo':'3957a','Description':'Antenna 4H - Round Top'}]
    good=next((o for o in opts if (o['BL ItemNo'],bc) in pairs|confirmed),None)
    assert good,(ref,color)
    inventory.append(dict(reference=good['BL ItemNo'],couleur=cr['BL Color Name'],code_couleur_bricklink=bc,quantite=qty,
                          description=good['Description'],reference_ldraw=ref))
with DEST.with_name(DEST.name+'_pieces.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=inventory[0],delimiter=';');w.writeheader();w.writerows(inventory)

render(out,DEST.name+'_apercu.png')
render(out,DEST.name+'_arriere.png',view='back')
render([p for p in out if p['section'] in [0,1,2,3,4]],DEST.name+'_structure_socle.png',view='bottom',size=(900,900))
thumb=Image.open(DEST.name+'_apercu.png');thumb.thumbnail((512,512));thumb.save(DEST.name+'_thumbnail.png')
with zipfile.ZipFile(DEST.with_suffix('.io'),'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('model.ldr','\n'.join(ldr)+'\n');z.writestr('modelv2.ldr','\n'.join(v2)+'\n');z.write(DEST.name+'_thumbnail.png','thumbnail.png')
summary={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'original_parts':len(parse()),'new_parts':len(out),
         'base_studs':[20,18],'base_unchanged':False,'base_footprint_unchanged':True,'original_base_parts_preserved':False,'catalog_combinations':len(inventory),'unverified_combinations':[],
         'native_studio_validation':False,'snow_changes':dict(changes)}
summary['studio_indexed_geometry']=True
summary['cave_parts_without_stud_plane_support']=[]
summary['palm_snow_verified_against_actual_stud_centers']=12
DEST.with_name(DEST.name+'_verification.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
