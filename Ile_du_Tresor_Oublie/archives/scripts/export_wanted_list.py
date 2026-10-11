"""Create an explicit BrickLink XML and a readable linked inventory."""
from pathlib import Path
import csv,json,html,xml.etree.ElementTree as ET
from audit_moc import parse

stem='Ile_du_Tresor_Oublie_V3_5'
rows=list(csv.DictReader(Path(stem+'_pieces.csv').open(encoding='utf-8-sig'),delimiter=';'))
assert len(rows)==73
assert sum(int(r['quantite']) for r in rows)==len(parse(Path(stem+'.io')))==366
assert len({(r['reference'],r['code_couleur_bricklink']) for r in rows})==len(rows)
root=ET.Element('INVENTORY')
for r in rows:
    item=ET.SubElement(root,'ITEM')
    for key,value in [('ITEMTYPE','P'),('ITEMID',r['reference']),('COLOR',r['code_couleur_bricklink']),('MINQTY',r['quantite'])]:
        ET.SubElement(item,key).text=value
ET.indent(root,space='  ')
xml_path=Path(stem+'_wanted_list.xml')
xml_path.write_text(ET.tostring(root,encoding='unicode')+'\n',encoding='utf-8')
parsed=ET.parse(xml_path).getroot()
assert sum(int(i.findtext('MINQTY')) for i in parsed)==366

colors={'White':'Blanc','Green':'Vert','Blue':'Bleu','Red':'Rouge','Brown':'Brun ancien',
        'Reddish Brown':'Brun rouge','Dark Bluish Gray':'Gris fonce bleute','Light Bluish Gray':'Gris clair bleute',
        'Tan':'Beige','Black':'Noir','Chrome Gold':'Or chrome','Trans-Green':'Vert transparent','Trans-Light Blue':'Bleu clair transparent'}
table=[]
for r in rows:
    link='https://www.bricklink.com/v2/catalog/catalogitem.page?P='+r['reference']+'&C='+r['code_couleur_bricklink']
    cols=[f'<a href="{html.escape(link)}" target="_blank" rel="noopener">{html.escape(r["reference"])}</a>',
          html.escape(colors.get(r['couleur'],r['couleur'])),r['quantite'],html.escape(r['description']),html.escape(r['reference_ldraw'])]
    table.append('<tr>'+''.join('<td>'+c+'</td>' for c in cols)+'</tr>')
page='''<!doctype html><html lang="fr"><meta charset="utf-8"><title>Inventaire V3.5</title>
<style>body{font:16px system-ui;background:#f6f8fa;color:#17222d;max-width:1250px;margin:40px auto;padding:0 20px}h1{font-size:28px}input{padding:12px;width:75%;border:1px solid #aaa;border-radius:6px}table{border-collapse:collapse;width:100%;margin-top:24px;background:white}th,td{padding:10px;border-bottom:1px solid #ddd;text-align:left}th{position:sticky;top:0;background:#dfe9f0}td:nth-child(3){text-align:right}a{color:#175c97}.note{padding:16px;background:#fff3d4}tr[hidden]{display:none}</style>
<h1>Île du Trésor Oublié — inventaire V3.5</h1>
<p>366 pièces · 73 combinaisons référence/couleur · 49 références distinctes.</p>
<p class="note">Ceci est l'inventaire du modèle local, pas la liste des 69 pièces signalées par Easy Buy. La capture ne donne pas leurs références. Les liens ouvrent le catalogue BrickLink pour vérifier chaque pièce et sa couleur. La disponibilité actuelle chez les vendeurs n'a pas été vérifiée.</p>
<p>Le XML fourni utilise les références et couleurs BrickLink. Il accepte les pièces neuves ou d'occasion, sans imposer de prix maximal.</p>
<label>Filtrer : <input id="filter" placeholder="Référence, couleur ou description…"></label>
<table><thead><tr><th>Référence BrickLink</th><th>Couleur</th><th>Quantité</th><th>Description</th><th>Référence du fichier</th></tr></thead><tbody>'''+''.join(table)+'''</tbody></table>
<script>document.getElementById('filter').addEventListener('input',e=>{let s=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(s))})</script></html>'''
Path(stem+'_inventaire_bricklink.html').write_text(page,encoding='utf-8')
Path(stem+'_import_bricklink_controle.json').write_text(json.dumps({'items':73,'quantity':366,'distinct_references':49,'xml_roundtrip':True,'seller_availability_verified':False,'reported_69_items_identified':False},indent=2),encoding='utf-8')
print('XML validated: 73 lots, 366 parts. Linked inventory generated.')
