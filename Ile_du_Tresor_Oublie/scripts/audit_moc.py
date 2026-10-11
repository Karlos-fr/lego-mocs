"""Read-only geometry and catalog audit using the installed Studio library."""
from pathlib import Path
from functools import lru_cache
import zipfile
import numpy as np

ROOT = Path(r'C:\Program Files\Studio 2.0\ldraw')
SOURCE = Path(__file__).resolve().parent.parent / 'Ile_du_Tresor_Oublie_V3_6_bricklink.io'
LIBRARY_PATHS = {}
for line in (ROOT/'cachedLibraryPath_0.txt').read_text(encoding='utf-8-sig').splitlines():
    fields=line.split('\t')
    if len(fields)>=2:LIBRARY_PATHS[fields[0].lower()]=ROOT/fields[1]

def resolve(ref):
    ref=ref.replace('\\','/')
    indexed=LIBRARY_PATHS.get(ref.lower())
    if indexed is not None and indexed.is_file():return indexed
    paths=[ROOT/'parts'/ref,ROOT/'p'/ref,ROOT/'UnOfficial/parts'/ref,ROOT/'UnOfficial/p'/ref]
    path=next((p for p in paths if p.is_file()),None)
    if path is None:raise FileNotFoundError(ref)
    return path

@lru_cache(None)
def vertices(ref):
    ref = ref.replace('\\', '/')
    path = resolve(ref)
    out = []
    for line in path.read_text(errors='replace').splitlines():
        t = line.split()
        if not t: continue
        if t[0] == '1':
            m = np.array(t[5:14], float).reshape(3, 3)
            v = np.array(t[2:5], float)
            out.append(vertices(' '.join(t[14:])) @ m.T + v)
        elif t[0] in ('3', '4'):
            out.append(np.array(t[2:], float).reshape(-1, 3))
    return np.concatenate(out) if out else np.empty((0, 3))

def parse(source=SOURCE):
    text = zipfile.ZipFile(source).read('model.ldr').decode('utf-8', errors='replace')
    section = 0
    out = []
    for line in text.splitlines():
        if line.startswith('0 // ') and line[5:7].isdigit(): section = int(line[5:7])
        if line.startswith('1 '):
            t = line.split()
            out.append(dict(index=len(out)+1, section=section, color=int(t[1]),
                            p=np.array(t[2:5], float), m=np.array(t[5:14], float).reshape(3,3),
                            ref=' '.join(t[14:]), line=line))
    return out

def bounds(part):
    pts = vertices(part['ref']) @ part['m'].T + part['p']
    return pts.min(axis=0), pts.max(axis=0)

if __name__ == '__main__':
    parts = parse()
    base = [bounds(p) for p in parts if p['section'] <= 4]
    low = np.min([b[0] for b in base], axis=0)
    high = np.max([b[1] for b in base], axis=0)
    print('Base bounds', low, high, 'studs', (high-low)[[0,2]]/20)
    for ref in ['11477.dat','15068.dat','25269.dat','10884.dat','2566.dat','2536.dat','3660a.dat','3660b.dat']:
        pts=vertices(ref); print(ref, pts.min(axis=0),pts.max(axis=0))
    # Exact overlapping envelopes for rectangular plates/bricks only.
    refs={'3020.dat','3021.dat','3022.dat','3023.dat','3024.dat','3031.dat','3034.dat','3460.dat','3710.dat','3623.dat','3001.dat','3002.dat','3003.dat','3005.dat','3622.dat'}
    solids=[]
    for p in parts:
        if p['ref'] not in refs: continue
        lo,hi=bounds(p); lo[1]=p['p'][1] # Exclude studs; top plane at origin.
        solids.append((p,lo,hi))
    for i,(a,al,ah) in enumerate(solids):
        for b,bl,bh in solids[i+1:]:
            overlap=np.minimum(ah,bh)-np.maximum(al,bl)
            if np.all(overlap>0.2): print('SOLID OVERLAP',a['index'],a['section'],a['ref'],b['index'],b['section'],b['ref'],overlap)
