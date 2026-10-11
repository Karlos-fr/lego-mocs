# Mariah Carey — scène de Noël

Ouvrir **[Mariah_Carey.io](Mariah_Carey.io)** dans BrickLink Studio.

![Aperçu du modèle](Mariah_Carey_apercu.png)

La scène comprend **187 pièces et 61 combinaisons référence/couleur**. La base de **12 × 12 tenons, soit 96 × 96 mm**, est conservée. La hauteur totale reste d'environ **96,5 mm**.

## Améliorations du 11 octobre 2026

- Visage féminin souriant avec lèvres dessinées, cheveux blonds et tête légèrement tournée vers le public.
- Bras relevés pour une pose de chant. Les rotations suivent les axes des épaules et conservent les assemblages bras/mains.
- Micro rapproché du visage ; une plaque à tenon décentré 1 × 2 fixe son pied sur les tenons de la scène.
- Deux projecteurs hauts à l'arrière et deux projecteurs plus bas à l'avant, orientés vers la chanteuse. Les ensembles clip/support/tête restent assemblés.
- Arche rouge ouverte, bordée de tuiles dorées, avec deux pieds fixés sur des plaques de liaison. Elle laisse la figurine visible.
- Cadeaux regroupés à gauche ; petit arbuste enneigé et feuillage à droite. Les éléments de neige déplacés restent fixés sur la base.
- Torse LEGO imprimé existant et jupe rouge conservée, sans décor personnalisé à fabriquer.

## Figurine et couleurs

| Élément | Référence BrickLink | Couleur BrickLink | Géométrie / couleur LDraw |
|---|---|---|---|
| Tête | 3626pb0635 | Light Nougat (90) | 3626cp0i.dat / 78 |
| Cheveux | 85974 | Tan (2) | 85974.dat / 19 |
| Torse | 973pb1243 | Red (5) | 973p5o.dat / 4 |

La [tête 3626pb0635](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3626pb0635) est répertoriée en Light Nougat ; les [cheveux 85974](https://www.bricklink.com/catalogItemIn.asp?P=85974&colorID=2&in=A) existent en Tan. Le [torse 973pb1243](https://www.bricklink.com/v2/catalog/catalogitem.page?P=973pb1243) représente une veste de Noël avec fourrure et ceinture : associé à la jupe, il suggère une tenue festive plutôt qu'une reproduction exacte d'une robe de Mariah.

Ces sources ont été consultées le 11 octobre 2026. Les pages de tête et de cheveux étaient indexées depuis moins d'une semaine ; la page du torse depuis environ trois mois. Elles attestent les combinaisons catalogue et affichent des offres, sans garantir les stocks, une livraison en France ou le résultat d'Easy Buy.

## Contrôles réalisés

- Les **32 placements constituant la base** sont identiques à ceux du modèle précédent.
- Archive vérifiée ; concordance exacte des références, couleurs, quantités, positions et matrices entre `model.ldr`, `modelv2.ldr`, `model2.ldr` et l'inventaire de travail temporaire. Aucun placement dupliqué.
- Contrôleur d'inventaire du skill exécuté sur **tout le modèle**, désormais composé de pièces standard sans DAT personnalisé.
- **60 des 61 combinaisons** sont attestées dans la table locale des éléments Studio. La dernière, le torse rouge 973pb1243, est attestée par la fiche BrickLink ci-dessus.
- Contrôle des appuis sur les tenons pour les ajouts et les éléments déplacés, conservation géométrique des assemblages articulés, inspection des vues avant et arrière. Les chevauchements de boîtes des nouveaux décors dépassant l'insertion habituelle des tenons ont été corrigés ; ce contrôle partiel ne remplace pas une analyse native des collisions.

La validation native Studio des connexions, collisions et de la stabilité, la construction physique et l'import effectif dans une Wanted List restent à confirmer. L'arche est un décor léger : éviter de saisir le modèle par sa traverse ou les projecteurs.

L'ancien modèle est conservé dans l'historique Git, notamment au commit `fdb29e8`. Les inventaires et vues de contrôle intermédiaires ne sont pas ajoutés au dossier.

## Régénérer l'aperçu

Depuis ce dossier :

```powershell
python ../.agents/skills/lego-moc/scripts/render_moc.py Mariah_Carey.io
```

Le rendu utilise la géométrie réelle et les décors géométriques des pièces, sans texte ajouté. Les matériaux et transparences restent simplifiés. Les scripts communs sont dans le skill `$lego-moc`.
