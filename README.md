# Mes MOC LEGO

Modèles personnels créés avec BrickLink Studio, aperçus et outils de vérification.

## Modèles

- [Île du Trésor Oublié](Ile_du_Tresor_Oublie/README.md) : petite île enneigée pour une ville de Noël.
- [Mariah Noël](Mariah_Noel_V2_7_spots_fins_robe_restauree.io)
- [Petite crèche](Petite_Creche_V2_2.io)
- [Portail Nether](Portail_Nether_V4_Centre_Transparent.io)
- [Wagon tombereau](Wagon_Tombereau_V2_1_Fond_Brun_Lisse.io)

Les fichiers des quatre derniers modèles sont conservés tels quels ; leurs inventaires et leur constructibilité n'ont pas été audités ici.

## Île du Trésor

Ouvrir [Ile_du_Tresor_Oublie.io](Ile_du_Tresor_Oublie/Ile_du_Tresor_Oublie.io). Le modèle comprend **391 pièces et 76 combinaisons référence/couleur**, sur une base de 20 × 18 tenons. Ce IO comporte les correspondances BrickLink nécessaires à son import en Wanted List.

![Rendu Studio original de l'île](Ile_du_Tresor_Oublie/Ile_du_Tresor_Oublie.png)

Le dossier conserve le modèle, cet aperçu, son guide ; les scripts utiles sont partag?s dans le skill. L'historique des versions précédentes et des anciens documents est disponible dans Git.

Les contrôles locaux ont validé la cohérence des inventaires et fichiers internes avant le retrait des inventaires séparés. La validation native de stabilité/collision et la construction physique restent à confirmer.

## Règles et outils

- [AGENTS.md](AGENTS.md) fixe les règles de travail communes.
- [Skill lego-moc](.agents/skills/lego-moc/SKILL.md) contient la méthode et le vérificateur réutilisable.
- Le [guide de l'île](Ile_du_Tresor_Oublie/README.md) explique l'utilisation du modèle et la génération de son aperçu.

Le vérificateur du skill reste disponible pour les futures modifications, avec un inventaire de travail si nécessaire ; il n'est pas requis pour importer le IO actuel sur BrickLink.

## Outils réutilisables pour les MOC

```powershell
python .agents/skills/lego-moc/scripts/render_moc.py chemin/modele.io --view front
python .agents/skills/lego-moc/scripts/audit_moc.py chemin/modele.io
python .agents/skills/lego-moc/scripts/support_audit.py chemin/modele.io
```

Les outils de géométrie lisent les IO/LDR/MPD et leurs sous-modèles. Les archives IO chiffrées et les pièces personnalisées absentes de la bibliothèque nécessitent un export compatible. Le contrôle d'inventaire BrickLink reste limité aux modèles plats. L'analyse des appuis est une aide à l'inspection, pas une validation native Studio.
