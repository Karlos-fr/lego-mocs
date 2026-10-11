"""Verify packaged records, source preservation, dimensions and solid envelopes."""
from pathlib import Path
import collections, hashlib, json, zipfile
import numpy as np
from audit_moc import parse, bounds, SOURCE

import sys
dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path('Ile_du_Tresor_Oublie_V3_3')
ps=parse(dest.with_suffix('.io'))
original=parse(SOURCE)
summary_path=dest.with_name(dest.name+'_verification.json')
summary=json.loads(summary_path.read_text())
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==summary['source_sha256']
def key(p):return (p['ref'],p['color'],tuple(p['p']),tuple(p['m'].ravel()))
if summary.get('original_base_parts_preserved') is False:
    from support_audit import studs
    def base_stud_set(parts):
        return {tuple(np.round(p['p']+p['m']@s,5)) for p in parts if 1<=p['section']<=4 for s in studs(p['ref'])}
    assert base_stud_set(original)==base_stud_set(ps)
else:
    assert [key(p) for p in original if 1<=p['section']<=4]==[key(p) for p in ps if 1<=p['section']<=4]
duplicates=sum(n-1 for n in collections.Counter(map(key,ps)).values() if n>1)
assert duplicates==0
rect_refs={'3020.dat','3021.dat','3022.dat','3023.dat','3024.dat','3031.dat','3034.dat','3460.dat','3710.dat','3623.dat',
           '3035.dat','3036.dat','3001.dat','3002.dat','3003.dat','3004.dat','3005.dat','3010.dat','3622.dat','3068b.dat','3069b.dat','3070b.dat','2431.dat','63864.dat'}
solids=[];overlaps=[]
for p in ps:
    if p['ref'] not in rect_refs or abs(p['m'][1,1]-1)>1e-5:continue
    lo,hi=bounds(p);lo[1]=p['p'][1];solids.append((p,lo,hi))
for i,(a,al,ah) in enumerate(solids):
    for b,bl,bh in solids[i+1:]:
        if np.all(np.minimum(ah,bh)-np.maximum(al,bl)>.2):overlaps.append((a['index'],b['index']))
assert not overlaps,overlaps
roof_interferences=[]
for p in [p for p in ps if p['section']==15]:
    al,ah=bounds(p);al[1]=p['p'][1]
    for q in ps:
        if q['section']==15:continue
        bl,bh=bounds(q);overlap=np.minimum(ah,bh)-np.maximum(al,bl)
        if np.all(overlap>.15) and overlap[1]>4.1:roof_interferences.append(q['index'])
assert not roof_interferences,roof_interferences
z=zipfile.ZipFile(dest.with_suffix('.io'));assert z.testzip() is None
a=z.read('model.ldr').decode().splitlines();b=z.read('modelv2.ldr').decode().splitlines()
assert len(a)==len(b)
for x,y in zip(a,b):
    if x.startswith('1 '):assert x.split()[1:]==y.split()[1:2]+y.split()[5:]
    else:assert x==y
base=[bounds(p) for p in ps if p['section']<=4]
lo=np.min([x[0] for x in base],axis=0);hi=np.max([x[1] for x in base],axis=0)
assert np.allclose((hi-lo)[[0,2]]/20,[20,18],atol=.001)
if summary.get('studio_indexed_geometry'):
    from support_audit import studs,supports
    assert all(c for p,c in supports(ps)), 'A cave part has no stud-plane support'
    checked=0
    for crown_sec,snow_sec in [(24,25),(28,29),(32,33)]:
        parents=[p for p in ps if p['section']==crown_sec]
        for snow in [p for p in ps if p['section']==snow_sec]:
            bottom=snow['p']+snow['m']@np.array([0,8,0])
            assert any(np.linalg.norm(parent['p']+parent['m']@s-bottom)<.0001
                       and np.linalg.norm(parent['m'][:,1]-snow['m'][:,1])<.0001
                       for parent in parents for s in studs(parent['ref'])), snow['index']
            checked+=1
    assert checked==12
    floor=[bounds(p) for p in ps if p['section']==11]
    assert all(any(l[0]<x<h[0] and l[2]<z<h[2] for l,h in floor)
               for x in [160,180,200,220] for z in [180,200,220,240,260])
    summary['palm_snow_stud_contacts_checked']=checked
    summary['cave_floor_covered_studs']=20
summary.update(exact_duplicates=duplicates,rectangular_parts_checked=len(solids),rectangular_solid_overlaps=overlaps,
               roof_envelope_interferences_over_4_1_LDU=roof_interferences,archive_integrity=True,model_records_match=True,
               source_preserved=True,validation_scope='Rectangular bodies and new roof envelopes; not a complete connector or curved-part collision simulation.')
summary_path.write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
