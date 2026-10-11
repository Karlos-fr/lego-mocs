"""Stud-plane support checks using the same indexed geometry as Studio."""
from functools import lru_cache
from pathlib import Path
import numpy as np
from audit_moc import resolve,parse,bounds

@lru_cache(None)
def studs(ref):
    out=[]
    for l in resolve(ref).read_text(errors='replace').splitlines():
        t=l.split()
        if not t or t[0]!='1':continue
        m=np.array(t[5:14],float).reshape(3,3);p=np.array(t[2:5],float);r=' '.join(t[14:])
        name=r.lower().replace('\\','/').split('/')[-1]
        if name in ['stud.dat','stud2.dat','stud2a.dat','stud6.dat','stud10.dat']:
            if m[1,1]>.9:out.append(p)
        elif not name.startswith('stud'):
            out.extend([m@s+p for s in studs(r)])
    return out

def supports(ps):
    world=[[(q['m']@s+q['p']) for s in studs(q['ref'])] for q in ps]
    result=[]
    for i,p in enumerate(ps):
        lo,hi=bounds(p);bottom=hi[1]
        contacts=[]
        for j,ss in enumerate(world):
            if i==j:continue
            for s in ss:
                if abs(s[1]-bottom)<.05 and lo[0]+.1<s[0]<hi[0]-.1 and lo[2]+.1<s[2]<hi[2]-.1:
                    contacts.append((ps[j]['index'],s.tolist()))
        result.append((p,contacts))
    return result

if __name__=='__main__':
    import argparse
    import audit_moc
    parser=argparse.ArgumentParser(description='Approximate vertical stud contacts; absence is not proof of a floating part.')
    parser.add_argument('model',type=Path)
    parser.add_argument('--studio',type=Path,default=audit_moc.DEFAULT_STUDIO)
    args=parser.parse_args()
    audit_moc.configure(args.studio)
    ps=parse(args.model)
    print('Heuristic only: misses clips, side connections, angled parts and unsupported stud variants; includes base parts.')
    for p,c in supports(ps):
        if not c:print('NO_VERTICAL_STUD_CONTACT',p['index'],p['ref'],p['p'])
