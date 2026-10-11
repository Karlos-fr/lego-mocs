# Projets MOC LEGO

Ces règles s'appliquent aux projets de ce dossier. Les demandes explicites de l'utilisateur priment. Pour créer ou modifier un MOC Studio, utiliser le skill du dépôt `.agents/skills/lego-moc/SKILL.md` (également installé localement dans `C:/Users/glech/.codex/skills/lego-moc/SKILL.md`).

## Modèle et versions
- Identifier le modèle de référence, les dimensions autorisées et les éléments à conserver avant de modifier. Une base plus grande nécessite une demande ou un accord explicite.
- Conserver les originaux et livrer une nouvelle version identifiable. Garder la cohérence entre modèle, aperçus, inventaire et fichier d'achat.
- Préférer les scripts et les fichiers. Pour cet utilisateur, ne pas piloter Studio par souris ou clavier sans une nouvelle demande explicite.
- Vérifier appuis, connexions, collisions, sol des cavités et accès de jeu selon la modification. La neige doit être fixée et soutenue ; vérifier les surfaces réelles, pas seulement les boîtes englobantes.
- Inspecter les vues pertinentes avec la géométrie des pièces. Un rendu généré par IA n'est pas une preuve du modèle.

## Studio et BrickLink
- Ne jamais confondre identifiants de pièces et couleurs LDraw, Studio et BrickLink. Utiliser les tables de correspondance installées ; ne pas déduire une conversion de la seule ressemblance du numéro.
- Pour les archives IO générées, conserver les modèles géométriques LDraw et inclure un `model2.ldr` converti en identifiants/couleurs BrickLink. Vérifier le format contre un exemple Studio installé si celui-ci change.
- Avant livraison, comparer exactement les couples référence/couleur et les quantités du modèle, du modèle interne BrickLink, du CSV et du XML. Un total égal ne suffit pas.
- Quand un export de Wanted List est fourni, le comparer à l'inventaire attendu. Expliquer les écarts de références, couleurs, quantités et paramètres sans déduire les références depuis une vignette seule.
- Le XML d'achat se colle dans « Upload BrickLink XML format ». L'onglet d'import de fichiers accepte notamment IO/LDR/BSX/LXF, pas ce XML.
- Distinguer existence au catalogue, offres affichées, stocks commandables et livraison à destination. Rechercher les offres actuelles quand demandé et noter la date/ancienneté des sources.
- Ne pas présenter les contrôles géométriques partiels comme une validation native de collision/stabilité, ni les offres catalogue comme un succès d'Easy Buy.
- Les achats et publications restent hors du périmètre d'une simple modification locale.

## Vérification
Utiliser le script d'inventaire du skill avant de livrer un IO généré. Les sous-modèles, pièces flexibles et pièces personnalisées exigent une prise en charge explicite : ne pas les ignorer pour obtenir un contrôle vert.
Rapporter ce qui a été vérifié, les erreurs restantes et les contrôles natifs ou physiques non réalisés.
