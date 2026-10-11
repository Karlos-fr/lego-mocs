"""Create V3.3 from V3.2 without launching or controlling Studio."""
from pathlib import Path
import csv, json, zipfile, collections, hashlib
import numpy as np
from audit_moc import parse, bounds, vertices, ROOT, SOURCE
from render_moc import render

DEST=Path('Ile_du_Tresor_Oublie_V3_3')
I=np.eye(3)
R=np.array([[0,0,1],[0,1,0],[-1,0,0]])
parts=parse()
original_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
sections=collections.defaultdict(list)
for p in parts: sections[p['section']].append(p.copy())

def add(section,ref,color,pos,m=I):
    p=dict(section=section,ref=ref,color=color,p=np.array(pos,float),m=np.array(m,float))
    sections[section].append(p)
    return p

# Replace the old mould, retaining the same exterior and connection position.
for ps in sections.values():
    for p in ps:
        if p['ref']=='3660a.dat':p['ref']='3660b.dat'
        if p['ref']=='2530.dat':p['color']=72
        # Bottle bottom was 4 LDU above the supporting plate surface.
        if p['ref']=='95228.dat':p['p'][1]-=4

# Three full-width lower roof plates close the holes; upper plates cross seams.
sections[15]=[]
for z in [210,250,290]:add(15,'3034.dat',72,[190,-104,z])
for x in [150,230]:
    add(15,'3031.dat',72,[x,-112,230])
    add(15,'3020.dat',72,[x,-112,290])

# Lift decorations that sat on the old lower roof to the new upper surface.
for p in sections[19]:
    if p['ref']=='54200.dat':p['p'][1]-=8
for p in sections[21]:
    if p['ref']=='11477.dat' and p['p'][0] in (130,210):p['p'][1]-=8
    if p['ref']=='25269.dat' and p['p'][0]==180:p['p'][1]-=8
    if p['ref']=='25269.dat' and p['p'][0]==260:p['p']=np.array([260,-120,240.])

# Lighter snow on the palms, anchored on the two actual studs of each leaf.
for crown_sec,snow_sec in [(24,25),(28,29),(32,33)]:
    sections[snow_sec]=[]
    leaves=[p for p in sections[crown_sec] if p['ref']=='10884.dat']
    for p in [leaves[0],leaves[2]]:
        add(snow_sec,'3069b.dat',15,p['p']+p['m']@np.array([0,-8,0]),p['m']@R)
    crown=next(p for p in sections[crown_sec] if p['ref']=='2566.dat')
    add(snow_sec,'98138.dat',15,crown['p']+crown['m']@np.array([0,-8,0]),crown['m'])

# Replace the scattered beach decoration with one coherent surface.
for s in [43,44,45,46]:sections[s]=[]

plate_refs={'3020.dat','3021.dat','3022.dat','3023.dat','3024.dat','3031.dat','3034.dat','3460.dat','3710.dat','3623.dat'}
def footprint(p):
    lo,hi=bounds(p)
    return {(x,z) for x in range(0,381,20) for z in range(0,341,20)
            if lo[0]+.05<x<hi[0]-.05 and lo[2]+.05<z<hi[2]-.05}

beach=set()
for s in [5,6]:
    for p in sections[s]:
        if p['ref'] in plate_refs and p['color']==15:beach |= footprint(p)

# Reserve the actual envelopes of accessories, dock, palm bases, and rocks.
blocked=set()
for s in range(7,43):
    for p in sections[s]:
        lo,hi=bounds(p)
        if lo[1]<-24.05 and hi[1]>-45:
            for x,z in beach:
                if lo[0]<x+9.95 and hi[0]>x-9.95 and lo[2]<z+9.95 and hi[2]>z-9.95:
                    blocked.add((x,z))
free=beach-blocked
cap_cells=set()

def cover(section,ref,points,pos,m=I):
    points=set(points)
    assert points <= free
    add(section,ref,15,pos,m)
    free.difference_update(points);cap_cells.update(points)

# Rounded slopes form selected shore edges, with their low ends toward water.
for z in [40,60,80,100,120,140,160,180,200,220,240,260,280,300]:
    row=sorted(x for x,zz in beach if zz==z)
    if not row:continue
    for side in ['left','right']:
        x=row[0] if side=='left' else row[-1]
        for dz in [20,-20]:
            cells={(x,z),(x,z+dz)}
            if cells <= free and all((x+(-20 if side=='left' else 20),zz) not in beach for xx,zz in cells):
                # Curve runs along z; rotation only chooses its lower shoreline end.
                cover(43,'11477.dat',cells,[x,-24,z+dz/2],I if dz==20 else R@R)
                break

# Broad flat snow fields. Prefer 2x2 tiles, then 1x2, then isolated 1x1 tiles.
for z in range(0,341,20):
    for x in range(0,381,20):
        points={(x,z),(x+20,z),(x,z+20),(x+20,z+20)}
        if points<=free:cover(44,'3068b.dat',points,[x+10,-32,z+10])
for z in range(0,341,20):
    for x in range(0,381,20):
        if {(x,z),(x+20,z)}<=free:
            cover(44,'3069b.dat',{(x,z),(x+20,z)},[x+10,-32,z])
        elif {(x,z),(x,z+20)}<=free:
            cover(44,'3069b.dat',{(x,z),(x,z+20)},[x,-32,z+10],R)
for x,z in sorted(free.copy()):
    # Quarter-round tiles on exposed corners; square tiles complete inner gaps.
    edge=sum((x+dx,z+dz) not in beach for dx,dz in [(20,0),(-20,0),(0,20),(0,-20)])
    ref='25269.dat' if edge>=2 else '3070b.dat'
    cover(45,ref,{(x,z)},[x,-32,z])

# A soft ridge closes the visual gap between the snowy rock crests.
add(20,'11477.dat',15,[190,-112,260],R)

HEADINGS={
1:'Eau - avant',2:'Eau - arriere',3:'Liaisons du socle - gauche',4:'Liaisons du socle - droite',
5:'Plage - avant',6:'Plage - arriere',7:'Pilotis',8:'Tablier du ponton',9:'Planches et bornes',10:'Neige du ponton',
11:'Fond de grotte',12:'Rochers - niveau 1',13:'Rochers - niveau 2',14:'Rochers - niveau 3',15:'Toit continu et liaisons croisees',
16:'Rochers - gauche',17:'Rochers - droite',18:'Facettes',19:'Sommets',20:'Neige sur les sommets',21:'Neige sur les corniches',
22:'Palmier A - pied',23:'Palmier A - tronc',24:'Palmier A - feuilles',25:'Palmier A - neige sur tenons',
26:'Palmier B - pied',27:'Palmier B - tronc',28:'Palmier B - feuilles',29:'Palmier B - neige sur tenons',
30:'Palmier C - pied',31:'Palmier C - tronc',32:'Palmier C - feuilles',33:'Palmier C - neige sur tenons',
34:'Sable',35:'Coffre',36:'Monnaies dans le coffre',37:'Squelette',38:'Bandana et pavillon',39:'Crabe bouteille et sabre',
40:'Monnaies eparses',41:'Glace et ecume',42:'Vegetation',43:'Bords doux de la neige',44:'Nappes de neige lisse',45:'Finition des contours'}

def number(x):return str(int(round(x))) if abs(x-round(x))<1e-7 else f'{x:.6f}'.rstrip('0').rstrip('.')
allparts=[]
ldr=['0 FILE '+DEST.name+'.ldr',"0 L'ile du tresor oublie - V3.3 compacte",'0 Author: Conception pour Gildas',
     '0 !LDRAW_ORG Model','0 // Script geometry checks only; native Studio collision/stability validation remains necessary.']
v2=ldr.copy()
for s in sorted(sections):
    if not sections[s]:continue
    header=f'0 // {s:02d} - {HEADINGS[s]}'
    ldr.append(header);v2.append(header)
    for p in sections[s]:
        p['index']=len(allparts)+1;allparts.append(p)
        payload=' '.join(number(v) for v in np.r_[p['p'],p['m'].ravel()])+' '+p['ref']
        ldr.append(f"1 {p['color']} {payload}")
        v2.append(f"11 {p['color']} {p['index']} False 0 {payload}")
    ldr.append('0 STEP');v2.append('0 STEP')
ldr.append('0 NOFILE');v2.append('0 NOFILE')
DEST.with_suffix('.ldr').write_text('\n'.join(ldr)+'\n',encoding='utf-8')

# Native-format archive with matching model/modelv2 records and a fresh preview.
render(allparts,DEST.name+'_apercu.png')
render(allparts,DEST.name+'_arriere.png',view='back')
from PIL import Image
thumb=Image.open(DEST.name+'_apercu.png');thumb.thumbnail((512,512));thumb.save(DEST.name+'_thumbnail.png')
with zipfile.ZipFile(DEST.with_suffix('.io'),'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('model.ldr','\n'.join(ldr)+'\n')
    z.writestr('modelv2.ldr','\n'.join(v2)+'\n')
    z.write(DEST.name+'_thumbnail.png','thumbnail.png')

# Verify invariants and catalog combinations against Studio's installed data.
before_base=[p['line'] for p in parts if p['section']<=4]
after_base=[l for l in ldr if l.startswith('1 ')][:len(before_base)]
assert before_base==after_base, 'Base must remain byte-for-byte geometrically unchanged'
assert len(parse(DEST.with_suffix('.io')))==len(allparts)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==original_hash
for p in allparts:
    assert len(vertices(p['ref']))>0
    assert abs(np.linalg.det(p['m'])-1)<5e-5
    assert np.max(np.abs(p['m'].T@p['m']-I))<5e-5
assert not free

data=ROOT.parent/'data'
rows=list(csv.DictReader((data/'StudioPartDefinition2.txt').open(encoding='utf-8-sig'),delimiter='\t'))
colorrows=list(csv.DictReader((data/'StudioColorDefinition.txt').open(encoding='utf-8-sig'),delimiter='\t'))
colors={int(c['LDraw Color Code']):c for c in colorrows if c.get('BL Color Code') and c['LDraw Color Code']}
catalog=collections.defaultdict(list)
for row in rows:catalog[row['LDraw ItemNo']].append(row)
elements=json.loads((data/'elementInfoList.json').read_text());pairs={(e['blItemNo'],e['blColorCode']) for e in elements}
# Older parts absent from element IDs, verified on BrickLink in this task.
confirmed={('2536b','8'),('70501a','21'),('3957a','11')}
inventory=[];unverified=[]
for (ref,color),qty in sorted(collections.Counter((p['ref'],p['color']) for p in allparts).items()):
    opts=catalog[ref]
    if ref=='3957a.dat':opts=[{'BL ItemNo':'3957a','Description':'Antenna 4H - Round Top'}]
    colorrow=colors[color];blcolor=colorrow['BL Color Code']
    good=next((o for o in opts if (o['BL ItemNo'],blcolor) in pairs|confirmed),None)
    if good is None:unverified.append((ref,color,qty));good=opts[0] if opts else {'BL ItemNo':ref[:-4],'Description':ref}
    inventory.append(dict(reference=good['BL ItemNo'],couleur=colorrow['BL Color Name'],code_couleur_bricklink=blcolor,
                          quantite=qty,description=good['Description'],reference_ldraw=ref,
                          verification='element LEGO' if (good['BL ItemNo'],blcolor) in pairs else 'catalogue BrickLink'))
assert not unverified,unverified
with DEST.with_name(DEST.name+'_pieces.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=inventory[0].keys(),delimiter=';');w.writeheader();w.writerows(inventory)
summary={'source_sha256':original_hash,'original_parts':len(parts),'new_parts':len(allparts),
         'base_studs':[20,18],'base_unchanged':True,'snow_covered_studs':len(cap_cells),
         'catalog_combinations':len(inventory),'unverified_combinations':unverified,'native_studio_validation':False}
DEST.with_name(DEST.name+'_verification.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
