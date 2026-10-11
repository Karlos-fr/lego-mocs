# Mariah Carey — scène de Noël

Ouvrir **[Mariah_Carey.io](Mariah_Carey.io)** dans BrickLink Studio. Le fichier provient de `Mariah_Noel_V2_7_spots_fins_robe_restauree.io` ; il a été déplacé et renommé sans modifier son contenu.

![Aperçu du modèle](Mariah_Carey_apercu.png)

Le modèle comprend **154 éléments**, répartis en **51 combinaisons géométrie/couleur**, dont un torse avec décor personnalisé. L'encombrement géométrique est d'environ **96 × 96 × 96,5 mm** (largeur, profondeur, hauteur).

## Vérification du 11 octobre 2026

- Archive intacte, 154 placements cohérents entre `model.ldr` et la racine de `model2.ldr` ; conversion des couleurs LDraw/BrickLink vérifiée pour les 154 éléments.
- Identifiants et quantités des **153 pièces standard / 50 combinaisons** vérifiés via le contrôleur du skill, sur une projection temporaire explicitement limitée aux pièces standard. Les alias internes `rename_…` ont été résolus depuis leurs métadonnées `BL_Item_No`.
- **48 des 50 combinaisons standard** sont attestées dans la table locale des éléments Studio. Ce contrôle ne prouve pas une disponibilité actuelle à la vente.
- **Tête `3626pb1352` en Light Nougat** : la [fiche BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3626pb1352&idColor=3) consultée répertorie cette impression en **Yellow** uniquement. La combinaison utilisée doit être remplacée pour une construction avec pièces catalogue.
- **Cheveux `85974` en Sienna** : cette couleur n'est pas répertoriée parmi les couleurs connues de la [fiche BrickLink](https://www.bricklink.com/v2/catalog/catalogitem.page?P=85974&ccName=4549990&id=85586&idColor=103) consultée. Des versions Tan, Medium Nougat ou Bright Light Yellow sont répertoriées, mais aucune substitution n'a été appliquée.
- **Torse `mc_torso_noel_decor_personnalise.dat`** : décor personnel embarqué dans le IO, sans référence BrickLink. Il est conservé dans l'aperçu ; il exige une réalisation personnalisée ou un remplacement par un torse existant. Ses fichiers de collision et de connexion embarqués sont vides.

La cohérence de conversion est vérifiée ; le modèle ne peut pas être déclaré entièrement achetable tel quel. Les collisions, connexions complètes, stabilité native Studio, import effectif sur BrickLink et construction physique restent à confirmer.

## Régénérer l'aperçu

Depuis ce dossier :

```powershell
python ../.agents/skills/lego-moc/scripts/render_moc.py Mariah_Carey.io
```

Le rendu utilise la géométrie réelle, y compris les DAT personnalisés embarqués, sans texte ajouté. Les matériaux et transparences restent simplifiés. Les outils communs sont dans le skill `$lego-moc` ; aucun script propre au projet n'est nécessaire.
