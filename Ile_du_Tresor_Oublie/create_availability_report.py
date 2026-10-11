from pathlib import Path
import json, csv, html
import xml.etree.ElementTree as ET
stem = 'Ile_du_Tresor_Oublie_V3_6'
data = json.loads(Path(stem+'_disponibilite_bricklink.json').read_text(encoding='utf-8'))
rows = data['inventaire']
assert len(rows)==76 and sum(int(r['quantite']) for r in rows)==391
assert all(r['lots_en_vente']>0 for r in rows)
with Path(stem+'_disponibilite_bricklink.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';')
    w.writeheader()
    w.writerows(rows)
table=[]
for r in rows:
    fields=[f'<a href="{html.escape(r["url"])}">{html.escape(r["reference"])}</a>',html.escape(r['couleur']),r['quantite'],str(r['lots_en_vente']),html.escape(r['anciennete_page']),html.escape(r['description'])]
    table.append('<tr>'+''.join('<td>'+v+'</td>' for v in fields)+'</tr>')
page='''<!doctype html><html lang="fr"><meta charset="utf-8"><title>Disponibilité BrickLink V3.6</title>
<style>body{font:16px system-ui;max-width:1250px;margin:35px auto;padding:0 20px;color:#203040;background:#f7f9fb}table{border-collapse:collapse;width:100%;background:white}th,td{padding:10px;border-bottom:1px solid #ddd;text-align:left}th{background:#e2edf4;position:sticky;top:0}.note{padding:18px;background:#fff1d5}input{padding:10px;margin:15px 0;width:75%}a{color:#1763a0}tr[hidden]{display:none}</style>
<h1>Île du Trésor Oublié — disponibilité BrickLink V3.6</h1>
<p>Vérification du 11 octobre 2026 : <b>76 combinaisons pièce/couleur sur 76 ont des offres affichées</b>, pour un modèle de 391 pièces.</p>
<p class="note">Les nombres ci-dessous correspondent à la rubrique « Lots For Sale » des pages publiques BrickLink consultées via recherche web. Ce sont des lots proposés à la vente, pas des quantités de pièces ni des vendeurs distincts. Les pages peuvent être mises en cache : leur ancienneté figure dans le tableau. Les stocks instantanés, les quantités commandables, les prix et la livraison en France n'ont pas été vérifiés. Aucune ligne sans offre n'a été trouvée. Ce contrôle ne permet pas d'identifier les 69 pièces signalées sur votre ancienne capture Easy Buy.</p>
<p>L'inventaire XML associé utilise les identifiants BrickLink et accepte le neuf ou l'occasion, sans prix maximal.</p>
<label>Rechercher <input id="filter" placeholder="Référence, couleur, description…"></label>
<table><thead><tr><th>Référence</th><th>Couleur</th><th>Quantité nécessaire</th><th>Lots en vente affichés</th><th>Ancienneté de la page</th><th>Description</th></tr></thead><tbody>'''+''.join(table)+'''</tbody></table>
<script>document.getElementById('filter').addEventListener('input',e=>{const q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))})</script></html>'''
Path(stem+'_disponibilite_bricklink.html').write_text(page,encoding='utf-8')
root=ET.Element('INVENTORY')
for r in rows:
    item=ET.SubElement(root,'ITEM')
    for key,value in [('ITEMTYPE','P'),('ITEMID',r['reference']),('COLOR',r['code_couleur_bricklink']),('MINQTY',r['quantite'])]:
        ET.SubElement(item,key).text=value
ET.indent(root,space='  ')
Path(stem+'_wanted_list.xml').write_text(ET.tostring(root,encoding='unicode')+'\n',encoding='utf-8')
check=ET.parse(stem+'_wanted_list.xml').getroot()
assert len(check)==76 and sum(int(i.findtext('MINQTY')) for i in check)==391
print('Rapport : 76/76 avec offres. XML : 76 lots, 391 pièces.')

