---
name: lego-moc
description: Créer, modifier et vérifier des MOC LEGO dans BrickLink Studio, leurs fichiers IO/LDraw et leurs inventaires d'achat BrickLink. Utiliser pour les modèles LEGO concrets, la structure, les pièces et les conversions de Wanted List.
---

# MOC LEGO et BrickLink Studio

Travailler à partir du modèle réel et des contraintes de l'utilisateur. Préserver les originaux et versionner les modifications. Préférer l'édition de fichiers lorsque demandée ; ne pas transformer une autorisation d'édition locale en achat ou publication.

## Conception
Identifier la version de référence, l'encombrement et les usages (exposition, jeu, accès aux cavités). Déterminer les appuis et connexions réels des pièces modifiées. Examiner plusieurs angles pour les trous, intersections et pièces suspendues. Pour la neige et les rochers, varier les formes tout en conservant des fixations constructibles et un budget raisonnable de pièces.

Utiliser les bibliothèques Studio effectivement indexées lorsqu'elles sont disponibles : des variantes officielles et non officielles du même nom peuvent avoir des points de connexion différents. Des boîtes englobantes ne prouvent ni une collision réelle, ni un emboîtement. Distinguer rendu, analyse approximative, vérification native Studio et construction physique.

## Fichiers et achat
Lire [references/studio-bricklink.md](references/studio-bricklink.md) pour générer un IO, un inventaire, ou diagnostiquer un import BrickLink. La séparation LDraw/BrickLink des couleurs et identifiants est essentielle.

Le script [scripts/check_inventory.py](scripts/check_inventory.py) vérifie les modèles **plats** sans pièce flexible/personnalisée et compare les inventaires. Il peut ajouter le fichier interne BrickLink à une nouvelle archive sans modifier les fichiers géométriques d'origine. Il utilise Python standard et les tables Studio installées, sans commander l'interface.

Exemple PowerShell depuis le projet :
```powershell
python "C:/Users/glech/.codex/skills/lego-moc/scripts/check_inventory.py" "modele.io" --inventory "modele_pieces.csv" --xml "modele_wanted_list.xml" --report "modele_controle_import.json"
```
Si `model2.ldr` manque, ajouter `--write-io "modele_bricklink.io"` : ne pas remplacer l'original. Pour une Wanted List exportée, ajouter `--wanted-export "export.xml"`. Une erreur donne un code de sortie non nul et doit être traitée avant livraison. Les écarts de l'export utilisateur sont distincts de la conformité du fichier local.

Ce script ne vérifie pas les collisions, la stabilité, le catalogue ou les vendeurs. Pour un modèle comportant des sous-modèles ou données avancées, utiliser un parseur adapté ou Studio ; ne pas aplatir ou supprimer ces éléments sans préserver leur géométrie et leur inventaire.

## Disponibilité et livraison
Pour une demande de disponibilité, consulter les offres du couple exact pièce/couleur et noter la date et la fraîcheur des sources. Vérifier les quantités et la destination quand accessibles. Si seules des pages catalogue en cache sont lisibles, dire « offres affichées », pas « toutes les pièces commandables ».

Après import réel ou réception d'un export, comparer les couples et quantités attendus. Ne pas expliquer un avertissement Easy Buy par une cause supposée quand les identifiants ne sont pas connus. Livrer les fichiers vérifiés et signaler précisément les validations restantes.
