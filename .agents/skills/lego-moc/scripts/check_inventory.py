"""Check flat Studio/LDraw and BrickLink inventories; never controls the UI."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

def records(text, kind='1'):
    result = []
    for line in text.splitlines():
        t = line.split()
        if not t or t[0] == '0':
            continue
        if t[0] != kind:
            raise ValueError('Unsupported line type: '+t[0])
        size = 15 if kind == '1' else 18
        if len(t) != size or not t[-1].lower().endswith('.dat'):
            raise ValueError('Only flat standard DAT references are supported')
        int(t[1])
        start = 2 if kind == '1' else 5
        tuple(float(v) for v in t[start:-1])
        result.append(t)
    if not result:
        raise ValueError('Empty model')
    return result

def counter(parts):
    return Counter((t[-1].removesuffix('.dat'), t[1]) for t in parts)

def xml_inventory(path, creation=False):
    raw = Path(path).read_text(encoding='utf-8-sig')
    if creation and raw.lstrip().startswith('<?xml'):
        raise ValueError('Upload XML must have no XML declaration')
    root = ET.fromstring(raw)
    if root.tag != 'INVENTORY':
        raise ValueError('Expected INVENTORY XML root')
    out = Counter()
    settings = []
    for item in root:
        if item.tag != 'ITEM' or item.findtext('ITEMTYPE') != 'P':
            raise ValueError('Only part ITEM entries supported')
        ref = item.findtext('ITEMID')
        color = item.findtext('COLOR') or '0'
        qty = int(item.findtext('MINQTY') or '1')
        if not ref or qty <= 0:
            raise ValueError('Invalid XML part or quantity')
        if creation:
            condition = item.findtext('CONDITION')
            price = item.findtext('MAXPRICE')
            if condition not in (None, '', 'N', 'U'):
                raise ValueError('Invalid upload CONDITION')
            if price and float(price) <= 0:
                raise ValueError('Invalid upload MAXPRICE')
        out[(ref, color)] += qty
        settings.append({c.tag:c.text for c in item if c.tag in
                         ('CONDITION','MAXPRICE','QTYFILLED')})
    return out, settings

def delta(expected, actual):
    def items(c):
        return [{'reference':r,'color':c0,'quantity':q}
                for (r,c0),q in sorted(c.items())]
    return {'missing':items(expected-actual), 'extra':items(actual-expected)}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('model', type=Path)
    p.add_argument('--inventory', required=True, type=Path)
    p.add_argument('--xml', type=Path)
    p.add_argument('--wanted-export', type=Path)
    p.add_argument('--studio', type=Path, default=Path('C:/Program Files/Studio 2.0'))
    p.add_argument('--write-io', type=Path)
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    report = {'checks':{}, 'errors':[], 'limitations':
              ['Flat models only; no geometry, collision, stability or seller checks.',
               'Local checks do not prove actual BrickLink import success.']}
    errors = report['errors']
    try:
        rows = list(csv.DictReader(args.inventory.open(encoding='utf-8-sig'),delimiter=';'))
        required = {'reference','reference_ldraw','code_couleur_bricklink','quantite'}
        if not rows or not required.issubset(rows[0]):
            raise ValueError('CSV schema missing required columns')
        colors = list(csv.DictReader((args.studio/'data/StudioColorDefinition.txt')
                                     .open(encoding='utf-8-sig'),delimiter='\t'))
        expected = Counter()
        mapping = {}
        for r in rows:
            key = (r['reference'],r['code_couleur_bricklink'])
            qty = int(r['quantite'])
            if qty <= 0 or key in expected:
                raise ValueError('Duplicate CSV lot or invalid quantity')
            expected[key] = qty
            codes = {d['LDraw Color Code'] for d in colors
                     if d['BL Color Code'] == key[1] and d['LDraw Color Code']}
            if not codes:
                raise ValueError('No LDraw color mapping for '+str(key))
            for code in codes:
                source_key = (r['reference_ldraw'],code)
                if source_key in mapping and mapping[source_key] != key:
                    raise ValueError('Ambiguous inventory mapping')
                mapping[source_key] = key
        with zipfile.ZipFile(args.model) as z:
            bad = z.testzip()
            if bad:
                raise ValueError('Archive corruption: '+bad)
            raw = z.read('model.ldr').decode('utf-8-sig')
            parts = records(raw)
            actual = Counter()
            converted = []
            for t in parts:
                key = mapping.get((t[-1],t[1]))
                if key is None:
                    raise ValueError('Part/color absent from CSV: '+str((t[-1],t[1])))
                actual[key] += 1
                u = t.copy()
                u[1],u[-1] = key[1],key[0]+'.dat'
                converted.append(u)
            report['parts'] = sum(actual.values())
            report['lots'] = len(actual)
            report['checks']['model_vs_csv'] = actual == expected
            if actual != expected:
                errors.append({'model_vs_csv':delta(expected,actual)})
            placements = [tuple(t[1:]) for t in parts]
            report['duplicate_placements'] = len(placements)-len(set(placements))
            if report['duplicate_placements']:
                errors.append('Duplicate exact part placements')
            if 'modelv2.ldr' in z.namelist():
                ext = records(z.read('modelv2.ldr').decode('utf-8-sig'),'11')
                a = [t[1:] for t in parts]
                b = [[t[1]]+t[5:] for t in ext]
                report['checks']['modelv2_matches_geometry'] = a == b
                if a != b:
                    errors.append('modelv2 geometry differs from model.ldr')
            if args.write_io:
                if args.write_io.exists():
                    raise ValueError('Output exists; choose a new version: '+str(args.write_io))
                if errors:
                    raise ValueError('Repair refused because source inventory checks failed')
                it = iter(converted)
                lines = [' '.join(next(it)) if line.startswith('1 ') else line
                         for line in raw.splitlines()]
                data = ('\n'.join(lines)+'\n').encode('utf-8')
                with zipfile.ZipFile(args.write_io,'w',zipfile.ZIP_DEFLATED) as target:
                    for name in z.namelist():
                        if name != 'model2.ldr':
                            target.writestr(name,z.read(name))
                    target.writestr('model2.ldr',data)
                with zipfile.ZipFile(args.write_io) as target:
                    assert target.testzip() is None
                    assert all(target.read(n)==z.read(n) for n in z.namelist()
                               if n != 'model2.ldr')
                report['written_io'] = str(args.write_io)
                blraw = data.decode()
            else:
                blraw = z.read('model2.ldr').decode('utf-8-sig') if 'model2.ldr' in z.namelist() else None
            if blraw is None:
                errors.append('Missing model2.ldr; raw LDraw colors/IDs can be misinterpreted by BrickLink')
            else:
                blparts = records(blraw)
                same = len(blparts)==len(parts) and all(
                    x[2:14]==y[2:14] for x,y in zip(parts,blparts))
                report['checks']['model2_geometry_unchanged'] = same
                report['checks']['model2_vs_csv'] = counter(blparts)==expected
                if not same:
                    errors.append('model2 placements differ')
                if counter(blparts) != expected:
                    errors.append({'model2_vs_csv':delta(expected,counter(blparts))})
        if args.xml:
            xml, _ = xml_inventory(args.xml,creation=True)
            report['checks']['xml_vs_csv'] = xml==expected
            if xml != expected:
                errors.append({'xml_vs_csv':delta(expected,xml)})
        if args.wanted_export:
            exported, settings = xml_inventory(args.wanted_export)
            report['checks']['wanted_export_vs_csv'] = exported==expected
            report['wanted_export'] = {'quantity':sum(exported.values()),
                                      'lots':len(exported),'settings':settings,
                                      'differences':delta(expected,exported)}
            if exported != expected:
                errors.append('Wanted List export differs from expected inventory')
    except (ValueError, KeyError, OSError, ET.ParseError, zipfile.BadZipFile, RuntimeError) as e:
        errors.append(str(e))
    report['ok'] = not errors
    if args.report:
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True,indent=2))
    return 0 if report['ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
