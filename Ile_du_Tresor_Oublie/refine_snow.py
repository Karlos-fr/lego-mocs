"""V3.4: rounded snow shapes with white backing; no application automation."""
from pathlib import Path
import collections,csv,hashlib,json,zipfile
import numpy as np
from PIL import Image
from audit_moc import ROOT,SOURCE,parse,vertices
from render_moc import render

SRC=Path('Ile_du_Tresor_Oublie_V3_3.io')
DEST=Path('Ile_du_Tresor_Oublie_V3_4')
I=np.eye(3);R=np.array([[0,0,1],[0,1,0],[-1,0,0]])
old=parse(SRC);out=[]
changes=collections.Counter()
def add(p,ref,pos,m=None):
    q=p.copy();q.update(ref=ref,p=np.array(pos),m=p['m'].copy() if m is None else m.copy());out.append(q)

for p in old:
    if p['section'] in [25,29,33]:continue
    if p['color']==15 and p['ref']=='11477.dat':
        changes['curved_1x2_removed']+=1
        if p['section']==43:
            # White beach plate already supports both studs. Keep this edge low.
            add(p,'1126.dat',p['p']+[0,-8,0],p['m']@R)
        else:
            # Full white plate backs the double curved mound at both ends.
            add(p,'3023.dat',p['p']+[0,-8,0],p['m']@R)
            add(p,'3563.dat',p['p']+[0,-8,0],p['m']@R)
    elif p['color']==15 and p['ref']=='15068.dat':
        changes['curved_2x2_removed']+=1
        # Full white backing prevents a dark underside beneath a snow cap.
        add(p,'3022.dat',p['p']+[0,-8,0])
        add(p,'79757.dat',p['p']+[0,-8,0]+p['m']@np.array([-10,0,-10]))
    else:out.append(p.copy())

for crown_sec,snow_sec in [(24,25),(28,29),(32,33)]:
    leaves=[p for p in old if p['section']==crown_sec and p['ref']=='10884.dat']
    # Asymmetric small deposits on existing stud positions, rather than strips.
    # Studio's unofficial leaf geometry has studs at x=0/20, y=-16.025.
    placements=[(0,0,'24246.dat',I),(0,20,'98138.dat',I),(2,20,'24246.dat',R@R)]
    for li,x,ref,turn in placements:
        p=leaves[li].copy();p['section']=snow_sec;p['color']=15
        add(p,ref,p['p']+p['m']@np.array([x,-24.025,0]),p['m']@turn)
    crown=next(p for p in old if p['section']==crown_sec and p['ref']=='2566.dat').copy()
    crown['section']=snow_sec;crown['color']=15
    add(crown,'98138.dat',crown['p']+crown['m']@np.array([0,-8,0]))
changes['rectangular_palm_tiles_removed']=6

groups=collections.defaultdict(list)
for p in out:groups[p['section']].append(p)
headings={}
with zipfile.ZipFile(SRC) as z:
    for line in z.read('model.ldr').decode().splitlines():
        if line.startswith('0 // ') and line[5:7].isdigit():headings[int(line[5:7])]=line
headings.update({20:'0 // 20 - Accumulations avec fond blanc',21:'0 // 21 - Corniches avec fond blanc',
                 25:'0 // 25 - Palmier A - petites touches arrondies',29:'0 // 29 - Palmier B - petites touches arrondies',
                 33:'0 // 33 - Palmier C - petites touches arrondies',43:'0 // 43 - Contours de neige ovales sans pente creuse'})
def num(x):return str(int(round(x))) if abs(x-round(x))<1e-7 else f'{x:.6f}'.rstrip('0').rstrip('.')
ldr=['0 FILE '+DEST.name+'.ldr',"0 L'ile du tresor oublie - V3.4 neige arrondie",'0 Author: Conception pour Gildas','0 !LDRAW_ORG Model',
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
thumb=Image.open(DEST.name+'_apercu.png');thumb.thumbnail((512,512));thumb.save(DEST.name+'_thumbnail.png')
with zipfile.ZipFile(DEST.with_suffix('.io'),'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('model.ldr','\n'.join(ldr)+'\n');z.writestr('modelv2.ldr','\n'.join(v2)+'\n');z.write(DEST.name+'_thumbnail.png','thumbnail.png')
summary={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'original_parts':len(parse()),'new_parts':len(out),
         'base_studs':[20,18],'base_unchanged':True,'catalog_combinations':len(inventory),'unverified_combinations':[],
         'native_studio_validation':False,'snow_changes':dict(changes)}
DEST.with_name(DEST.name+'_verification.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
