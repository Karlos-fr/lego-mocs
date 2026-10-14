# Petite crèche

Ouvrir **[Petite_Creche.io](Petite_Creche.io)** dans BrickLink Studio. Le fichier provient de `Petite_Creche_V2_2.io` : il a été déplacé et renommé **sans modifier son contenu**, ce qui a été vérifié par empreinte SHA-256.

![Aperçu de la crèche](Petite_Creche_apercu.png)

Le modèle contient **329 éléments et 99 combinaisons géométrie/couleur**. L'aperçu représente les **327 éléments visibles** ; le mouton et l'âne sont déjà masqués dans `modelv2.ldr`. L'encombrement des éléments rendus est d'environ **201,5 × 160 × 168,8 mm** (largeur, profondeur, hauteur) ; cette mesure inclut les décors et ne définit pas la taille du socle.

## Contrôle du 14 octobre 2026

- Archive intacte, concordance exacte des 329 références, couleurs, positions et matrices entre `model.ldr` et `modelv2.ldr`.
- Toutes les couleurs LDraw rencontrées ont une correspondance unique dans la table couleur Studio/BrickLink. Cela ne signifie pas que chaque pièce existe dans la couleur choisie.
- Le fichier **ne contient pas de `model2.ldr`**, nécessaire à notre méthode d'export fiable des références et couleurs BrickLink. Aucun export d'achat corrigé n'a été ajouté au modèle lors de ce simple classement et audit.
- Le contrôleur d'inventaire du skill a été exécuté sur une **projection temporaire explicitement limitée à 320 éléments standard / 91 combinaisons**, dotée d'un `model2.ldr` de contrôle. Inventaires et placements concordent, sans doublon sur cette projection. Ce résultat ne valide pas l'import du IO original ni les neuf éléments exclus.
- **80 des 91 combinaisons standard** sont attestées dans la table locale des éléments Studio. Cinq autres sont attestées par le catalogue BrickLink : `973p4n` White, `973p4e` Red, `973pb1139` Dark Brown, `973pb0583` Dark Red et `973px86a` White. Quatre combinaisons sont non répertoriées ; deux demandent encore confirmation, comme détaillé ci-dessous.
- Aperçus avant et arrière inspectés avec la géométrie réelle des éléments visibles. Les collisions, connexions et la stabilité natives Studio, ainsi que la construction physique, n'ont pas été validées.

## Combinaisons à corriger

| Géométrie LDraw | Référence BrickLink | Couleur utilisée | Quantité | Constat catalogue |
|---|---|---|---:|---|
| 3034.dat | 3034 | Dark Brown (120) | 2 | Couleur absente des couleurs connues et des offres affichées sur la [fiche Plate 2 × 8](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3034). Une ancienne entrée de guide de prix ne suffit pas à attester cette combinaison. |
| 3626bp84.dat | 3626pb0628 | Reddish Brown (88) | 1 | Impression répertoriée en Yellow uniquement : [fiche tête](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3626pb0628). |
| 3626cp8q.dat | 3626pb1571 | Light Nougat (90) | 1 | Impression répertoriée en Yellow uniquement : [fiche tête féminine](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3626pb1571). |
| 24581p01.dat | 24581pb01 | Light Nougat (90) | 1 | Cette tête de bébé est répertoriée en Yellow uniquement : [fiche bébé](https://www.bricklink.com/v2/catalog/catalogitem.page?P=24581pb01). Une autre référence sera nécessaire pour une tête couleur chair. |

Aucune substitution n'est appliquée : les personnages et la palette de référence sont conservés pour une éventuelle amélioration ultérieure.

## Incertitudes restantes

- **Couronne 71015 en Pearl Gold (115)** : absente de la table locale et des couleurs connues de la [fiche couronne](https://www.bricklink.com/v2/catalog/catalogitem.page?P=71015&ccName=4100457&lang=Eng), malgré quelques offres affichées sous cette couleur. Une offre isolée ne prouve pas la combinaison ; variante ou couleur à confirmer.
- **Torse 973pa2 en Black (11)** : non attesté dans la table locale ; la fiche détaillée BrickLink renvoie une erreur lors de ce contrôle. La référence existe au catalogue, mais sa couleur n'est pas validée ici.
- **Quatre capes `50231c01.dat`**, en Blue, Dark Red (deux exemplaires) et Dark Tan : géométrie textile formée disponible, mais correspondance automatique BrickLink absente. Elles sont rendues et restent explicitement hors de la projection standard vérifiée.
- **Deux hanches `3815.dat`**, en Red et Black : géométrie disponible, mais pas de référence BrickLink dans l'entrée locale exacte. L'alias de moule et la correspondance doivent être confirmés.
- **Corps de bébé `25126.dat` blanc** : géométrie locale marquée « Needs Work », sans correspondance exacte dans la table. Les références décorées de corps de bébé existantes ne peuvent pas être substituées automatiquement.
- **Mouton `74188pb01.dat` blanc et âne `106470pb01.dat` Light Bluish Gray** : deux placements masqués dans le fichier Studio ; leurs noms DAT ne se résolvent pas dans la bibliothèque utilisée. Le mouton possède un alias local `bl_74188pb01.dat`, mais aucune correction de référence ou de visibilité n'a été effectuée. L'[âne 106470pb01](https://www.bricklink.com/v2/catalog/catalogitem.page?ccName=6481725&id=241438&idColor=86) existe au catalogue ; cela ne fournit pas sa géométrie manquante.

Les confirmations complémentaires de torses proviennent des fiches [973p4n](https://www.bricklink.com/v2/catalog/catalogitem.page?P=973p4n), [973p4e](https://www.bricklink.com/catalogItemIn.asp?P=973p4e), [973pb1139](https://www.bricklink.com/v2/catalog/catalogitem.page?P=973pb1139), [973pb0583](https://www.bricklink.com/v2/catalog/catalogitem.page?P=973pb0583) et [973px86a](https://www.bricklink.com/v2/catalog/catalogitem.page?P=973px86a).

Sources consultées le 14 octobre 2026, avec des indexations allant du jour même à plusieurs mois selon les fiches. Le contrôle porte sur les correspondances et couleurs catalogue, sans vérifier stocks commandables, quantités par vendeur, livraison en France ou résultat d'Easy Buy. Le modèle ne peut pas être déclaré entièrement achetable en l'état.

## Régénérer l'aperçu

Les scripts communs se trouvent dans `../.agents/skills/lego-moc/scripts/`. Pour ce modèle, le lecteur géométrique seul n'interprète pas les masques Studio : filtrer explicitement les deux éléments masqués avant le rendu, sans les supprimer du IO.

Depuis ce dossier, avec Python, NumPy, Pillow et Studio installés :

```powershell
@'
import sys, zipfile
from pathlib import Path
sys.path.insert(0, '../.agents/skills/lego-moc/scripts')
import audit_moc as a, render_moc as r
source = Path('Petite_Creche.io')
a.configure(); a.mount_embedded(source)
parts = a.parse(source)
with zipfile.ZipFile(source) as archive:
    rows = [line.split() for line in archive.read('modelv2.ldr').decode('utf-8-sig').splitlines() if line.startswith('11 ')]
assert len(rows) == len(parts)
assert all(row[-1] == part['ref'] for row, part in zip(rows, parts))
visible = [part for row, part in zip(rows, parts) if row[3] != 'True']
r.render(visible, Path('Petite_Creche_apercu.png'))
'@ | python -
```

Le rendu simplifie les matériaux et l'éclairage, et n'ajoute aucun texte. Les inventaires de travail, vues arrière et projections de contrôle restent temporaires ; aucun script propre à ce projet n'est ajouté.
