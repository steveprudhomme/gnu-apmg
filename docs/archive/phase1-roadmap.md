# Feuille de route — objectifs vérifiables

| OBJECTIVE | GOAL | SUCCESS CRITERIA | IMPLEMENTATION PLAN | OWNER |
|---|---|---|---|---|
| Phase 0 — fondations | Publier un socle libre et sans données personnelles | Licence intégrale, gouvernance, CI et contrôles de confidentialité présents | Repo public, PR templates, règles de branches, revue initiale | Mainteneur principal |
| Phase 1 — inventaire | Balayer 100 à 200 photos récursivement sans modifier les originaux | 100 % des fichiers éligibles détectés, SHA-256 stable, doublons exacts repérés, EXIF exploité, 0 écriture sur source | Scanner Python en lecture seule, manifest JSONL, journal d'erreurs, tests de reprise | Équipe Python (à désigner) |
| Phase 2 — analyse | Décrire scènes et extraire texte localement | 0 requête externe, concordance des sorties au schéma, métriques qualité et temps sur pilote, taux d'erreurs documenté | Qwen3-VL via Ollama en file d'attente, PaddleOCR, contrôles de sortie et échantillonnage humain | Équipe IA/OCR (à désigner) |
| Phase 3 — personnes / lieux | Reconnaissance faciale contrôlée et géocodage offline | Pas d'identification non confirmée exportée comme fait ; 0 données biométriques vers réseau | Modules distincts, bibliothèque locale, référentiel local | Non attribué |
| Phase 4 — interopérabilité | Export XMP/IPTC sûr | Aller-retour digiKam/ExifTool sans perte des champs ciblés ; rollback possible | Exporter contrôlé, test sur copies uniquement | Non attribué |
| Phase 5 — ontologie | Relations de provenance et d'événements | Chaque assertion possède une origine, un statut et une trace de validation | SKOS / RDF / PROV-O, tests d'inférence et révocation | Non attribué |

La qualité prime sur les dates. Aucun seuil arbitraire de « précision IA » ne sera déclaré acceptable sans validation sur le corpus pilote.


## Décomposition opérationnelle — Phase 1 (jalon `v0.2.0-alpha.1`)

> Statut : **plan approuvé pour implémentation, non encore validé sur le corpus privé**. Les sous-étapes ci-dessous sont ordonnées, testables et indépendantes des modules IA. Aucun média privé ni chemin personnel n'entre dans Git.

| ID | Sous-étape | Livrable / tâche | Critères de sortie | État |
|---|---|---|---|---|
| P1.0 | Protection avant traitement | Contrat d'interface, règles sur chemins sources/sorties et répertoires interdits ; tests et données synthétiques uniquement | Aucune écriture dans l'arbre source ; aucune donnée sensible dans le dépôt | Implémenté (tests synthétiques) |
| P1.1 | Environnement Windows | Installation sans privilèges admin, Python standard, ExifTool optionnel explicité et version relevée | Commandes documentées pour PowerShell ; échec clair si ExifTool indisponible | Documentation fournie, Windows non testé |
| P1.2 | Exploration récursive | Fichiers photographiques candidats, Unicode, chemins imbriqués, pas de suivi des liens symboliques ; erreurs individuelles journalisées | Couverture complète de l'échantillon ; aucune boucle sur liens | Implémenté (tests synthétiques) |
| P1.3 | Empreintes et doublons exacts | SHA-256 par flux, contrôle de modification entre ouverture et fin de lecture ; distinction contenu et emplacement | Même contenu = même asset ; chemins multiples préservés ; scans répétés idempotents | Implémenté (tests synthétiques) |
| P1.4 | Extraction documentaire | Lecture ExifTool en JSON sans modifier la source ; sauvegarde des tags bruts qualifiés (namespace), version et diagnostics | Métadonnées absentes ou illisibles représentées honnêtement ; aucune conversion silencieuse des dates/GPS | Implémenté, ExifTool réel à valider |
| P1.5 | SQLite et migrations | Tables assets, file_locations, metadata, scans/scan_items, erreurs ; contraintes, transactions, version de schéma | Réouverture/relance sans doublons et intégrité relationnelle préservée | Implémenté (tests synthétiques) |
| P1.6 | CLI et reprise | Commandes `scan` et `report`, codes de sortie stables, journal local minimal ; ré-exécution sûre après interruption | Analyse répétée idempotente ; erreurs partielles visibles | Implémenté (tests synthétiques) |
| P1.7 | Validation automatisée | Tests fonctionnels générant des faux fichiers, corruption, EXIF absent, chemins Unicode, doublons, ré-exécution | Tests exécutables sans photographies personnelles ; CI adaptée | Implémenté (tests synthétiques) |
| P1.8 | Tutoriel illustré et documentation | Tutoriel Windows étape par étape avec figures schématiques SVG et sorties vérifiées ; README/INSTALL/architecture synchronisés | Figures non trompeuses, commandes reproduites en local | Documenté, images SVG intégrées |
| P1.9 | Porte pilote 100–200 | Procédure privée de vérité terrain, hash avant/après, diagnostic d'échecs et autorisation formelle avant Phase 2 | 0 modification d'originaux ; couverture complète ou erreur explicite ; rapport local de pilote | À faire sur photos réelles |

### Sous-étapes complémentaires préparant la Phase 2

| ID | Sous-étape | Livrable | Dépendance |
|---|---|---|---|
| P2.0 | Contrat des observations | Schéma validé, versions de prompts et modèles, statuts distincts | P1.5 |
| P2.1 | Préparation locale | Modèle Qwen3-VL 8B quantifié, OCR PaddleOCR et contrôle de l'absence de sortie réseau | P1.9 |
| P2.2 | Exécution GPU maîtrisée | Une image à la fois, mesures de VRAM, tentative de repli et diagnostic | P2.1 |
| P2.3 | Qualité et reprise | Échantillon annoté, métriques OCR/objets, idempotence et invalidation de cache | P2.0–P2.2 |
| P2.4 | Interface de validation | Consultation locale, corrections humaines et historique | P2.3 |

### Politique de commit et de documentation

1. Faire un **commit distinct de cette feuille de route avant de modifier le code**.
2. Documenter toute étape livrée dans `docs/tutorial/phase-1.md`, avec diagrammes SVG en appui ; ne jamais présenter une illustration comme une capture réelle.
3. Mettre à jour `README.md`, `INSTALL.md`, contrats et protocole pilote lorsqu'un comportement change.
4. Chaque commit de code doit être vérifiable ; ne pas déclarer une étape pilote terminée sans données de test représentatives.
5. Éviter de versionner photographies, GPS privés, chemins locaux, journalisations et bases SQLite. Avant publication GitHub, auditer les fichiers suivis et l'historique.

### Journal d'avancement — pré-alpha `0.2.0a1`

- **Commits de préparation** : import initial, puis **commit ROADMAP distinct avant le premier code**.
- **Code implémenté** : noyau Python sans dépendances externes, migration SQLite 0001, CLI de scan/rapport, lecture ExifTool par sous-processus local, statuts d'erreur et reprise idempotente.
- **Documentation** : `docs/tutorial/phase-1.md` et trois figures SVG, README/INSTALL/contrats/modèle de données mis à jour.
- **Validation effectuée** : tests automatisés sur des octets synthétiques ; un essai CLI avec trois faux fichiers a inventorié deux contenus distincts et un groupe de copies.
- **Non validé** : outil ExifTool réel sur Windows, corpus personnel 100–200 images, véritable protection OS lecture seule, interruption par coupure électrique, conformité de toutes les variantes RAW et HEIC.
- **Phase 2** : aucun module IA/OCR implémenté ; ne pas présenter les schémas futurs comme une implémentation.
