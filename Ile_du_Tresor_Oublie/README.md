# Île du Trésor Oublié

Ouvrir **[Ile_du_Tresor_Oublie.io](Ile_du_Tresor_Oublie.io)** dans BrickLink Studio. Le modèle contient 391 pièces et 76 combinaisons pièce/couleur, sur une base de 20 × 18 tenons.

![Aperçu du modèle](Ile_du_Tresor_Oublie_apercu.png)

Pour alimenter une Wanted List, importer directement ce IO sur BrickLink. Le fichier comprend les correspondances BrickLink dans `model2.ldr`. Aucun inventaire séparé n'est nécessaire pour cet usage.

## Scripts utiles

`scripts/` conserve les outils de géométrie, de rendu et d'analyse des appuis. Ils nécessitent Python, `numpy`, `Pillow` et la bibliothèque locale de Studio.

Depuis ce dossier, régénérer l'aperçu :

```powershell
python scripts/render_moc.py
```

Le script lit le IO ci-dessus et écrit `Ile_du_Tresor_Oublie_apercu.png` à côté. Un autre chemin IO peut être fourni en argument. Le rendu simplifie l'éclairage et les matériaux et ne constitue pas une validation native des collisions ou de la stabilité.

Les archives, anciens aperçus, inventaires séparés et rapports ont été retirés du dossier de travail. Leur historique versionné reste disponible dans Git. La validation native Studio et la construction physique restent à confirmer.
