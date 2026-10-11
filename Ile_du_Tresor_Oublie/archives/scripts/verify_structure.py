"""Check foundation connectivity and palm mounting surfaces in V3.6."""
from pathlib import Path
import collections,json
import numpy as np
from audit_moc import parse,bounds
from support_audit import studs

stem='Ile_du_Tresor_Oublie_V3_6'
ps=parse(Path(stem+'.io'))
base=[p for p in ps if p['section']<=4]
graph=[set() for p in base]
bridges=[]
for i,p in enumerate(base):
    lo,hi=bounds(p)
    support=[]
    for j,q in enumerate(base):
        if i==j:continue
        if any(abs(s[1]-hi[1])<.01 and lo[0]+.1<s[0]<hi[0]-.1 and lo[2]+.1<s[2]<hi[2]-.1
               for s in [q['p']+q['m']@v for v in studs(q['ref'])]):
            graph[i].add(j);graph[j].add(i)
        if p['section']==0 and q['section'] in [1,2]:
            a,b=bounds(q)
            if np.all(np.minimum(hi[[0,2]],b[[0,2]])-np.maximum(lo[[0,2]],a[[0,2]])>.1):support.append(q['index'])
    if p['section']==0:bridges.append({'part':p['ref'],'water_plates_linked':len(support)})
seen=set();components=0
for i in range(len(base)):
    if i in seen:continue
    components+=1;queue=[i];seen.add(i)
    while queue:
        for j in graph[queue.pop()]:
            if j not in seen:seen.add(j);queue.append(j)
assert components==1,components
mounts=[]
for sec in [22,26,30]:
    foot=next(p for p in ps if p['section']==sec and p['ref']=='2563.dat')
    mounting=next(p for p in ps if p['section']==sec and p['ref'] in ['3022.dat','3020.dat'])
    lo,hi=bounds(foot);a,b=bounds(mounting)
    assert abs(hi[1]-mounting['p'][1])<.01
    assert np.all(lo[[0,2]]>=a[[0,2]]) and np.all(hi[[0,2]]<=b[[0,2]])
    mounts.append(sec)
path=Path(stem+'_verification.json');report=json.loads(path.read_text())
report.update(foundation_connected_components=components,foundation_bridges=bridges,palm_mounts_checked=mounts)
path.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'foundation_connected_components':components,'foundation_plates':len(bridges),
                  'plates_crossing_multiple_water_parts':sum(b['water_plates_linked']>1 for b in bridges),
                  'palm_mounts_checked':len(mounts)},indent=2))
