# Île du Trésor Oublié

Le modèle actuel est **[Ile_du_Tresor_Oublie_V3_6_bricklink.io](Ile_du_Tresor_Oublie_V3_6_bricklink.io)** : 391 pièces, 76 combinaisons pièce/couleur, base de 20 × 18 tenons. C'est le seul IO dans le dossier principal.

- `apercus/` : vues avant, arrière et dessous du socle.
- `inventaires/` : liste des pièces et XML BrickLink. Coller le XML dans « Upload BrickLink XML format » ; le TXT contient le même texte prêt à copier.
- `rapports/` : contrôles et relevés de disponibilité. Les notes historiques décrivent parfois le fichier avant sa correction d'import ; le contrôle d'inventaire porte sur le IO corrigé.
- `scripts/` : outils de rendu, géométrie et appuis, avec dépendances Python `numpy` et `Pillow` et bibliothèque Studio installée.
- `archives/` : anciennes versions, IO V3.6 avant correction, diagnostics et scripts de transformation conservés pour référence.

Les scripts archivés utilisent les noms et emplacements de leur époque. Ils ne doivent pas être lancés tels quels depuis le dossier principal ; adapter leurs chemins dans une copie de travail avant de les réutiliser.

## Vérifier l'inventaire

Depuis ce dossier :

```powershell
python ../.agents/skills/lego-moc/scripts/check_inventory.py Ile_du_Tresor_Oublie_V3_6_bricklink.io --inventory inventaires/Ile_du_Tresor_Oublie_V3_6_pieces.csv --xml inventaires/Ile_du_Tresor_Oublie_V3_6_wanted_list.xml
```

## Générer un aperçu

```powershell
python scripts/render_moc.py
```

Sans argument, le script lit le IO actuel et écrit `Ile_du_Tresor_Oublie_V3_6_bricklink_apercu.png` à côté. Un chemin IO peut aussi être fourni en argument. Ce rendu simplifie l'éclairage et les matériaux ; il ne valide pas les connexions ni les collisions dans Studio.

L'import effectif sur BrickLink, la validation native Studio et la construction physique restent à confirmer.
