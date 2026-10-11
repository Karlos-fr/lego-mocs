from pathlib import Path
from collections import Counter
import csv,json,zipfile,xml.etree.ElementTree as ET,shutil
stem='Ile_du_Tresor_Oublie_V3_6'
rows=list(csv.DictReader(Path(stem+'_pieces.csv').open(encoding='utf-8-sig'),delimiter=';'))
mapping={r['reference_ldraw']:r for r in rows}
source=Path(r'C:\Users\glech\Downloads')
export=next(source.glob('*tr*sors(1).xml'))
shutil.copy2(export,Path(stem+'_wanted_list_export_utilisateur.xml'))
items=[{c.tag:c.text for c in i} for i in ET.parse(export).getroot()]
assert len(items)==58 and sum(int(i['MINQTY']) for i in items)==306
expected_refs={r['reference_ldraw'].removesuffix('.dat'):r['reference'] for r in rows}
omitted=[r for r in rows if r['reference'] not in {i['ITEMID'] for i in items}]
assert len(omitted)==18 and sum(int(r['quantite']) for r in omitted)==85
with zipfile.ZipFile(stem+'.io') as z:
    source_text=z.read('model.ldr').decode('utf-8')
    converted=[]
    converted_counts=Counter()
    old_counts=Counter()
    for line in source_text.splitlines():
        if line.startswith('1 '):
            t=line.split()
            ref=t[14]
            candidates=[r for r in rows if r['reference_ldraw']==ref]
            # Match actual LDraw color against the installed official Studio color map.
            defs=list(csv.DictReader(Path(r'C:\Program Files\Studio 2.0\data\StudioColorDefinition.txt').open(encoding='utf-8-sig'),delimiter='\t'))
            r=next(r for r in candidates if any(d['LDraw Color Code']==t[1] and d['BL Color Code']==r['code_couleur_bricklink'] for d in defs))
            old_counts[(ref,t[1])]+=1
            t[1]=r['code_couleur_bricklink']
            t[14]=r['reference']+'.dat'
            converted_counts[(r['reference'],t[1])]+=1
            line=' '.join(t)
        converted.append(line)
    model2='\n'.join(converted)+'\n'
    target=Path(stem+'_bricklink.io')
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as out:
        for name in z.namelist():
            if name!='model2.ldr':out.writestr(name,z.read(name))
        out.writestr('model2.ldr',model2)
assert converted_counts==Counter({(r['reference'],r['code_couleur_bricklink']):int(r['quantite']) for r in rows})
with zipfile.ZipFile(target) as z,zipfile.ZipFile(stem+'.io') as old:
    assert z.testzip() is None
    assert all(z.read(n)==old.read(n) for n in old.namelist())
    assert len([l for l in z.read('model2.ldr').decode().splitlines() if l.startswith('1 ')])==391
    # Positions, orientations and step metadata match original exactly.
    a=old.read('model.ldr').decode().splitlines()
    b=z.read('model2.ldr').decode().splitlines()
    assert len(a)==len(b)
    for x,y in zip(a,b):
        if x.startswith('1 '):assert x.split()[2:14]==y.split()[2:14]
        else:assert x==y
Path(stem+'_wanted_list_a_coller.txt').write_text(Path(stem+'_wanted_list.xml').read_text(encoding='utf-8'),encoding='utf-8')
report={'source_export':str(export),'export_lots':58,'export_quantity':306,'expected_lots':76,'expected_quantity':391,'missing_lots':18,'missing_quantity':85,'missing_items':omitted,'cause':'Absent model2.ldr in generated IO. Exported colors equal raw LDraw codes rather than BrickLink color codes; omitted items have distinct LDraw and BrickLink IDs.','repair':'Added model2.ldr with BrickLink part IDs and colors, following installed Studio sample structure. Original model.ldr, modelv2.ldr and thumbnail are byte-identical.','checks':{'archive_integrity':True,'geometry_unchanged':True,'converted_inventory_matches_xml':True,'parts':391,'lots':76},'bricklink_actual_upload_tested':False,'warning_61_exact_items_identified':False}
Path(stem+'_diagnostic_import.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Export: 58 lots / 306 parts. Omitted: 18 lots / 85 parts.')
print('Corrected IO: model2.ldr = 76 lots / 391 parts. Geometry unchanged.')

