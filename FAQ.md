# FAQ

**Pourquoi pas directement digiKam ou Immich ?** Nous souhaitons un moteur modulaire de métadonnées documentaires et de provenance interopérable, pas une galerie alternative. Étudier et réutiliser leurs standards lorsqu'ils conviennent.

**Pourquoi le projet ne contient-il aucune photo ?** Les archives incluent souvent des visages, des coordonnées GPS et des informations familiales. Le pilote privé reste exclusivement hors Git.

**Tout fonctionne-t-il sur 12 Go de VRAM ?** Non démontré. La vision 8B quantifiée est une hypothèse à mesurer ; OCR et vision ne devront pas monopoliser simultanément le GPU.

**Pourquoi SQLite et non un graphe RDF natif ?** SQLite facilite un pilote solo ; exporter plus tard un graphe RDF normalisé n'exige pas d'emblée une infrastructure de serveur.

**Les résultats IA sont-ils vrais ?** Non, ce sont des observations avec provenance et état de vérification. Seul un contrôle humain approprié transforme un candidat en donnée confirmée.

**Puis-je distribuer commercialement ?** La GPL 3 l'autorise, sous réserve de respecter ses obligations et celles des tiers. Une analyse juridique reste nécessaire pour un paquet binaire final.


## Les HEIC sont-ils compatibles ?

La Phase 1 inventorie et extrait les métadonnées des HEIC via ExifTool. Le pilote a validé 100 HEIC avec empreintes originales inchangées. Cela ne garantit pas encore le décodage pour affichage, miniatures, OCR ou vision, ni tous les fichiers HEIC/HEIF possibles. Voir le tutoriel Phase 1 pour les résultats et limites.


## Les HEIC peuvent-ils servir à la Phase 2 ?

Dix copies ont été décodées en dérivés RGB réduits sans métadonnées. Trois ont servi aux essais OCR et vision ; une réponse de vision tronquée a été refusée. HDR, couleur et qualité sémantique nécessitent encore une validation humaine. Voir le tutoriel Phase 2.
## Comment valider les mots-clés proposés ?

Créer une session de revue privée et ouvrir review.html. Choisir des concepts puis valider, corriger ou rejeter. Exporter le lot JSON et l'importer explicitement avec le script fourni. Les clics seuls ne modifient pas la base ; les mots-clés ne sont pas encore écrits dans les images. Voir le [tutoriel de revue](docs/tutorial/revue-mots-cles.md).
