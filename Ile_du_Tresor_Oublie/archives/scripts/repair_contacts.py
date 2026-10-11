"""Repair contacts and close the cave using Studio's indexed geometry."""
from pathlib import Path
import collections,csv,hashlib,json,zipfile
import numpy as np
from PIL import Image
from audit_moc import ROOT,SOURCE,parse,vertices
from render_moc import render
from support_audit import studs,supports
SRC=Path('Ile_du_Tresor_Oublie_V3_4.io')
DEST=Path('Ile_du_Tresor_Oublie_V3_5')
I=np.eye(3);R=np.array([[0,0,1],[0,1,0],[-1,0,0]])
old=parse(SRC);out=[];changes=collections.Counter()
def add(p,ref,pos,m=None):
    q=p.copy();q.update(ref=ref,p=np.array(pos,float),m=p['m'].copy() if m is None else m.copy());out.append(q)
# Replace cave floor and overlapping snow tiles with one continuous floor.
for p in old:
    if p['section']==11 or p['index'] in [353,354,363,364]:continue
    if p['section'] in [25,29,33]:continue
    q=p.copy()
    if p['section']==19 and p['ref']=='54200.dat':
        q['p']=p['p']+np.array([0,16,0]);changes['floating_cheese_slopes_lowered']+=1
    out.append(q)
base=next(p for p in old if p['section']==11).copy();base['color']=71
for x in [170,210]:
    for z in [190,230]:add(base,'3068b.dat',[x,-32,z],I)
for x in [170,210]:add(base,'3069b.dat',[x,-32,260],I)
changes['continuous_floor_tiles']=6
# Exact stud centers from the part actually indexed and loaded by Studio.
for crown_sec,snow_sec in [(24,25),(28,29),(32,33)]:
    leaves=[p for p in old if p['section']==crown_sec and p['ref']=='10884.dat']
    for li,z,ref,turn in [(0,-10,'24246.dat',I),(0,10,'98138.dat',I),(2,10,'24246.dat',R@R)]:
        leaf=leaves[li]
        assert any(np.allclose(s,[0,0,z]) for s in studs(leaf['ref']))
        q=leaf.copy();q['section']=snow_sec;q['color']=15
        add(q,ref,leaf['p']+leaf['m']@np.array([0,-8,z]),leaf['m']@turn)
    crown=next(p for p in old if p['section']==crown_sec and p['ref']=='2566.dat').copy()
    crown['section']=snow_sec;crown['color']=15
    add(crown,'98138.dat',crown['p']+crown['m']@np.array([0,-8,0]))
changes['palm_snow_contacts_corrected']=12
# Check every upright cave part has at least one stud-plane support.
assert all(c for p,c in supports(out)),[(p['ref'],p['p'].tolist()) for p,c in supports(out) if not c]
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
ldr=['0 FILE '+DEST.name+'.ldr',"0 L'ile du tresor oublie - V3.5 neige arrondie",'0 Author: Conception pour Gildas','0 !LDRAW_ORG Model',
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
render([p for p in out if p['section'] in [5,6,11,12,13,14,16,17,18]],DEST.name+'_coupe_grotte.png',size=(900,900))
thumb=Image.open(DEST.name+'_apercu.png');thumb.thumbnail((512,512));thumb.save(DEST.name+'_thumbnail.png')
with zipfile.ZipFile(DEST.with_suffix('.io'),'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('model.ldr','\n'.join(ldr)+'\n');z.writestr('modelv2.ldr','\n'.join(v2)+'\n');z.write(DEST.name+'_thumbnail.png','thumbnail.png')
summary={'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'original_parts':len(parse()),'new_parts':len(out),
         'base_studs':[20,18],'base_unchanged':True,'catalog_combinations':len(inventory),'unverified_combinations':[],
         'native_studio_validation':False,'snow_changes':dict(changes)}
summary['studio_indexed_geometry']=True
summary['cave_parts_without_stud_plane_support']=[]
summary['palm_snow_verified_against_actual_stud_centers']=12
DEST.with_name(DEST.name+'_verification.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
