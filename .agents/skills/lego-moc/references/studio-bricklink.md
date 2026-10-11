# Formats et conversions

## Archive Studio
Les exemples installés dans `C:/Program Files/Studio 2.0/Sample` permettent de contrôler les conventions réelles. L'exemple Banana.io observé contient :
- `model.ldr` : lignes LDraw, identifiants géométriques et couleurs LDraw ;
- `modelv2.ldr` : lignes Studio étendues, notamment type 11, conservant les mêmes couleurs et références géométriques ;
- `model2.ldr` : lignes de type 1 avec références et couleurs BrickLink, destinées à l'échange catalogue.

Cette convention a été constatée localement, pas supposée universelle pour toutes les versions. Ne pas convertir les couleurs de model.ldr pour corriger un import : cela modifierait son interprétation géométrique. Ajouter ou régénérer model2.ldr et comparer les positions, matrices et étapes.

Les tables `data/StudioColorDefinition.txt` distinguent Studio Color Code, BL Color Code et LDraw Color Code. `data/StudioPartDefinition2.txt` fournit les correspondances de pièces ; inspecter son en-tête avant de l'utiliser. Une conversion absente ou ambiguë doit produire une erreur, pas une substitution approximative.

Exemples de couleurs différentes : blanc LDraw 15 / BrickLink 1, bleu LDraw 1 / BrickLink 7, vert LDraw 2 / BrickLink 6. Exemples de références différentes rencontrées : 2536.dat / 2536b, 2543.dat / x70, 6141.dat / 4073.

## CSV attendu par le script
UTF-8, séparateur point-virgule, colonnes :
`reference;couleur;code_couleur_bricklink;quantite;description;reference_ldraw`.
Une ligne par combinaison référence BrickLink/couleur, quantités strictement positives. La colonne reference_ldraw identifie la géométrie ; les codes LDraw sont dérivés de la table couleur installée.

## Wanted List XML
Racine INVENTORY, éléments ITEM avec ITEMTYPE=P, ITEMID, COLOR, MINQTY. Sans déclaration XML. Omettre CONDITION pour accepter neuf et occasion ; omettre MAXPRICE lorsqu'aucun plafond n'est demandé. Ne pas copier aveuglément les sentinelles d'un export (CONDITION=X, MAXPRICE=-1) dans un fichier de création.

Pour importer : ouvrir Upload to Wanted List, sélectionner « Upload BrickLink XML format », coller le contenu, puis vérifier l'aperçu avant la création. Une nouvelle liste vide évite d'additionner des quantités à celles d'une liste existante. Un IO peut être sélectionné dans « Upload a file from your computer ».

Sources à consulter pour les règles actuelles :
- https://www.bricklink.com/help.asp?helpID=207
- https://studiohelp.bricklink.com/hc/en-us/articles/43767995846935-Part-IDs-and-Alternate-Numbers
- https://www.bricklink.com/help.asp?helpID=2457

## Contrôle d'import
Comparer les couples référence/couleur et chaque quantité, puis les totaux. Relever séparément QTYFILLED, CONDITION et MAXPRICE qui peuvent modifier la recherche d'achat. Une référence manquante et une quantité déjà possédée n'ont pas la même signification.

Incident constaté dans Île du Trésor V3.6 : archive générée sans model2.ldr. Export BrickLink de 306 pièces/58 lignes contre 391/76 attendues ; 85 pièces avec IDs différents omises et couleurs LDraw reprises comme couleurs BrickLink. La correction locale ajoute model2.ldr ; elle ne constitue pas une preuve d'import effectif sur le site.
