# FAQ

**Pourquoi pas directement digiKam ou Immich ?** Nous souhaitons un moteur modulaire de métadonnées documentaires et de provenance interopérable, pas une galerie alternative. Étudier et réutiliser leurs standards lorsqu'ils conviennent.

**Pourquoi le projet ne contient-il aucune photo ?** Les archives incluent souvent des visages, des coordonnées GPS et des informations familiales. Le pilote privé reste exclusivement hors Git.

**Tout fonctionne-t-il sur 12 Go de VRAM ?** Non démontré. La vision 8B quantifiée est une hypothèse à mesurer ; OCR et vision ne devront pas monopoliser simultanément le GPU.

**Pourquoi SQLite et non un graphe RDF natif ?** SQLite facilite un pilote solo ; exporter plus tard un graphe RDF normalisé n'exige pas d'emblée une infrastructure de serveur.

**Les résultats IA sont-ils vrais ?** Non, ce sont des observations avec provenance et état de vérification. Seul un contrôle humain approprié transforme un candidat en donnée confirmée.

**Puis-je distribuer commercialement ?** La GPL 3 l'autorise, sous réserve de respecter ses obligations et celles des tiers. Une analyse juridique reste nécessaire pour un paquet binaire final.
