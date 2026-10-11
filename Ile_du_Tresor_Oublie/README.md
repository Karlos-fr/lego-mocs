# Île du Trésor Oublié

Ouvrir **[Ile_du_Tresor_Oublie.io](Ile_du_Tresor_Oublie.io)** dans BrickLink Studio. Le modèle contient 391 pièces et 76 combinaisons pièce/couleur, sur une base de 20 × 18 tenons.

![Rendu Studio original](Ile_du_Tresor_Oublie.png)

`Ile_du_Tresor_Oublie.png` est le rendu Studio original restauré depuis l'historique. `Ile_du_Tresor_Oublie_apercu.png` est l'aperçu du IO actuel produit par le script, sans texte ajouté. Le rendu original peut représenter une version antérieure du modèle.

Pour alimenter une Wanted List, importer directement ce IO sur BrickLink. Le fichier comprend les correspondances BrickLink dans `model2.ldr`. Aucun inventaire séparé n'est nécessaire pour cet usage.

## Outils partagés

Les outils de géométrie, de rendu et d'analyse des appuis sont partagés dans `../.agents/skills/lego-moc/scripts/`. Ils nécessitent Python, `numpy`, `Pillow` et la bibliothèque locale de Studio.

Depuis ce dossier, régénérer l'aperçu :

```powershell
python ../.agents/skills/lego-moc/scripts/render_moc.py Ile_du_Tresor_Oublie.io
```

Le script lit le modèle fourni en argument et écrit `Ile_du_Tresor_Oublie_apercu.png` à côté. Options : `--view front|back|bottom`, `--output chemin.png`, `--size 1100` et `--studio "chemin/vers/Studio 2.0"`. Le rendu simplifie l'éclairage et les matériaux et ne constitue pas une validation native des collisions ou de la stabilité.

Les archives, anciens aperçus, inventaires séparés et rapports ont été retirés du dossier de travail. Leur historique versionné reste disponible dans Git. La validation native Studio et la construction physique restent à confirmer.
