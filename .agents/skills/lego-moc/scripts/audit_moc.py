"""Reusable IO/LDR/MPD geometry reader; uses the actual indexed Studio library."""
from pathlib import Path
from functools import lru_cache
import argparse
import json
import zipfile
import tempfile
from pathlib import PurePosixPath
import numpy as np

DEFAULT_STUDIO = Path('C:/Program Files/Studio 2.0')
ROOT = DEFAULT_STUDIO / 'ldraw'
LIBRARY_PATHS = {}
CUSTOM_PATHS = {}
_CUSTOM_TEMP = None

def mount_embedded(source):
    """Read DAT geometry bundled in a Studio archive without installing it."""
    global _CUSTOM_TEMP, CUSTOM_PATHS
    CUSTOM_PATHS = {}
    if _CUSTOM_TEMP is not None: _CUSTOM_TEMP.cleanup()
    _CUSTOM_TEMP = None
    vertices.cache_clear()
    if Path(source).suffix.lower() != '.io': return
    with zipfile.ZipFile(source) as archive:
        files = [i for i in archive.infolist() if i.filename.startswith('CustomParts/') and i.filename.lower().endswith('.dat')]
        if not files: return
        _CUSTOM_TEMP = tempfile.TemporaryDirectory(prefix='lego-custom-')
        aliases = {}
        for item in files:
            relative = PurePosixPath(item.filename[len('CustomParts/'):])
            if relative.is_absolute() or '..' in relative.parts or ':' in str(relative):
                raise ValueError('Unsafe embedded geometry path')
            path = Path(_CUSTOM_TEMP.name).joinpath(*relative.parts)
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(archive.read(item))
            CUSTOM_PATHS[str(relative).lower()] = path
            if relative.parts[0] in ('p','s'):
                CUSTOM_PATHS[str(PurePosixPath(*relative.parts[1:])).lower()] = path
            aliases.setdefault(relative.name.lower(),[]).append(path)
        for name, paths in aliases.items():
            if len(paths)==1: CUSTOM_PATHS.setdefault(name,paths[0])

def configure(studio=DEFAULT_STUDIO):
    global ROOT, LIBRARY_PATHS
    ROOT = Path(studio) / 'ldraw'
    if not ROOT.is_dir():
        raise FileNotFoundError('Studio library missing: '+str(ROOT))
    LIBRARY_PATHS = {}
    cache = ROOT/'cachedLibraryPath_0.txt'
    if cache.is_file():
        for line in cache.read_text(encoding='utf-8-sig').splitlines():
            fields = line.split('\t')
            if len(fields)>=2:
                LIBRARY_PATHS[fields[0].lower()] = ROOT/fields[1]
    vertices.cache_clear()

def resolve(ref):
    ref = ref.replace('\\','/')
    custom = CUSTOM_PATHS.get(ref.lower())
    if custom is not None: return custom
    indexed = LIBRARY_PATHS.get(ref.lower())
    if indexed is not None and indexed.is_file():
        return indexed
    paths = [ROOT/'parts'/ref, ROOT/'p'/ref,
             ROOT/'UnOfficial/parts'/ref, ROOT/'UnOfficial/p'/ref]
    path = next((p for p in paths if p.is_file()),None)
    if path is None:
        raise FileNotFoundError('Unsupported or missing geometry: '+ref)
    return path

@lru_cache(None)
def vertices(ref):
    out = []
    for line in resolve(ref).read_text(errors='replace').splitlines():
        t = line.split()
        if not t: continue
        if t[0]=='1':
            m = np.array(t[5:14],float).reshape(3,3)
            out.append(vertices(' '.join(t[14:]))@m.T+np.array(t[2:5],float))
        elif t[0] in ('3','4'):
            out.append(np.array(t[2:],float).reshape(-1,3))
    return np.concatenate(out) if out else np.empty((0,3))

def parse(source):
    source = Path(source)
    if source.suffix.lower()=='.io':
        with zipfile.ZipFile(source) as z:
            text = z.read('model.ldr').decode('utf-8-sig')
    elif source.suffix.lower() in ('.ldr','.mpd'):
        text = source.read_text(encoding='utf-8-sig')
    else:
        raise ValueError('Supported formats: .io, .ldr, .mpd')
    models = {}
    current = None
    for line in text.splitlines():
        if line.startswith('0 FILE '):
            if list(models)==['__main__'] and not any(l.startswith('1 ') for l in models['__main__']):
                models.clear()
            current = line[7:].strip().replace('\\','/').lower()
            if current in models: raise ValueError('Duplicate submodel: '+current)
            models[current] = []
        elif line.startswith('0 NOFILE'):
            current = None
        elif current is not None:
            models[current].append(line)
        elif not models:
            models.setdefault('__main__',[]).append(line)
            current = '__main__'
    if not models: raise ValueError('Empty model')
    out = []
    def expand(name,matrix,position,inherited,stack):
        if name in stack: raise ValueError('Cyclic submodel: '+name)
        section = 0
        for line in models[name]:
            if line.startswith('0 // ') and line[5:7].isdigit():
                section = int(line[5:7])
            if not line.startswith('1 '): continue
            t = line.split()
            if len(t)<15: raise ValueError('Malformed part line')
            color = int(t[1])
            if color==16: color=inherited
            m = matrix@np.array(t[5:14],float).reshape(3,3)
            p = matrix@np.array(t[2:5],float)+position
            ref = ' '.join(t[14:]).replace('\\','/')
            key = ref.lower()
            if key in models:
                expand(key,m,p,color,stack+[name])
            else:
                if not key.endswith('.dat'):
                    raise ValueError('Unresolved submodel: '+ref)
                if color in (16,24):
                    raise ValueError('Unresolved inherited part color: '+ref)
                out.append(dict(index=len(out)+1,section=section,color=color,
                                p=p,m=m,ref=ref,line=line))
    expand(next(iter(models)),np.eye(3),np.zeros(3),16,[])
    if not out: raise ValueError('No parts in model')
    return out

def bounds(part):
    pts = vertices(part['ref'])@part['m'].T+part['p']
    if not len(pts): raise ValueError('Empty geometry: '+part['ref'])
    return pts.min(axis=0),pts.max(axis=0)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model',type=Path)
    parser.add_argument('--studio',type=Path,default=DEFAULT_STUDIO)
    args=parser.parse_args()
    configure(args.studio)
    mount_embedded(args.model)
    parts=parse(args.model)
    boxes=[bounds(p) for p in parts]
    lo=np.min([b[0] for b in boxes],axis=0)
    hi=np.max([b[1] for b in boxes],axis=0)
    print(json.dumps({'parts':len(parts),'references':len({p['ref'] for p in parts}),
                      'bounds_ldu':[lo.tolist(),hi.tolist()],
                      'extent_studs':((hi-lo)/20).tolist(),
                      'limitations':'Bounds are not a collision or stability validation.'},indent=2))

if __name__=='__main__':
    main()
