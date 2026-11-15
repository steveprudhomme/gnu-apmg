# Contrats d'échange v0 — proposition

Un `photo_id` stable est dérivé d'une empreinte SHA-256 des octets, non d'un chemin (mutable). Un `scan_id` est distinct de `photo_id` ; chaque emplacement local reçoit un `file_instance_id`. Le manifeste phase 1 est un flux JSONL UTF-8 avec `photo_id`, `path_private` **local uniquement**, `size`, `sha256`, `mtime`, `exif_raw`, `errors`.

Phase 2 produit des observations immuables séparées : `observation_id`, `photo_id`, `type`, `literal` ou `concept_uri`, `geometry`, `status` (`suggested|validated|rejected|inferred`), `origin` (`human|model|ocr|exif|rule`), `tool_name`, `model_digest`, `created_at`, `evidence`, `confidence` (nullable, seulement si calibrée), `supersedes_id`.

Un changement de modèle produit un nouvel ensemble d'observations ; il ne supprime pas les validations humaines. Les assertions réfutées restent conservées dans l'historique local, avec un mécanisme de suppression réglementaire distinct. Les chemins privés et coordonnées ne font jamais partie des exemples versionnés. Voir `schemas/observation.schema.json`.


## Contrat implémenté de Phase 1 (`0.2.0a1`)

- Entrée CLI : `python -m photosemantique scan SOURCE --db DB [--exiftool EXE] [--jsonl MANIFEST] [--no-exif]`.
- Base SQL version 1 sous `photosemantique/migrations/0001_inventory.sql`. La clé `assets.sha256` représente le contenu, `file_locations.path_local` un emplacement, `scan_items` l'observation d'un balayage donné.
- JSONL facultatif par scan : `path_local`, `asset_sha256`, `status`, `error_code`, `error_detail`. **Privé : non à versionner**. Les tags EXIF sont dans `source_metadata` (`tag`, `value_json`, version ExifTool).
- Les chemins vers les sources et les manifestes sont contrôlés pour empêcher une écriture dans l'arbre source et dans Git. L'intégration ExifTool utilise `-j -G1:4 -a -s` ; l'absence de métadonnées et les erreurs de lecture sont rapportées sans convertir une proposition en fait.
- La CLI renvoie `0` pour scan complet, `2` pour une analyse partielle, `1` pour une erreur fatale.
- Pour reprise, relancer `scan` : nouveaux `scan_items` pour chaque run, sans duplication d'assets ni de chemins. Le scan interrompu par exception capturable devient `interrupted`.

Le présent contrat est implémenté mais n'a été validé que sur des fichiers fictifs ; la compatibilité réelle avec ExifTool sur Windows reste à établir.


## Contrat Phase 2 implémenté, expérimental (15 novembre 2026)

Les paragraphes v0 ci-dessus restent historiques. La Phase 1 a depuis été testée avec ExifTool réel sur 200 copies, dont 100 HEIC ; voir le tutoriel Phase 1.

CLI distincte : `python -m photosemantique.phase2 prepare SOURCE --output DOSSIER`, puis `vision DOSSIER --model MODELE --output FICHIER_JSONL` ou `ocr DOSSIER --detection MODELE_DETECTION_LOCAL --recognition MODELE_RECONNAISSANCE_LOCAL --output FICHIER_JSONL`.

La préparation produit `image.png` et `manifest.json`. Les observations suivent `photosemantique/schemas/phase2-observation.schema.json`, schéma v1 embarqué et strict, distinct du schéma v0 de conception : statut toujours suggested, confidence null, provenance outil/version/digest, identité source SHA-256 et empreinte du dérivé. La vision ajoute model_name/prompt_digest ; l'OCR ajoute raw_score/polygon/coordinate_space (derivative_pixels). Aucun nom ou GPS n'est ajouté au manifeste de préparation.

Sorties privées et nouvelles à chaque run ; fichiers existants refusés. Chaque phase renvoie 0 si son exécution et sa validation technique aboutissent, 1 sinon. Une absence de texte OCR peut être une sortie vide valide ; elle ne prouve pas l'absence de texte dans la photo. Une réponse de vision tronquée est refusée avec incomplete_response. Une réussite technique n'est pas une validation documentaire humaine.

Les observations sont dans des JSONL privés, pas encore dans SQLite. Pas de reprise fine, cache d'inférence, UI de validation ou index vectoriel à ce stade. Relancer dans un nouveau dossier. Les erreurs de backend sont résumées par type sans afficher les textes ou descriptions privés.


## Contrat de consultation du vocabulaire (15 novembre 2026)

`python -m photosemantique.taxonomy QUERY [--source iptc|getty] [--include-retired]` interroge seulement les JSON embarqués. Réponse : identifiant officiel, libellés, définitions et parents conservés. Les traductions Getty de présentation sont dans `editorial_label_fr`, pas dans les libellés officiels.

La recherche n’est pas un moteur d’annotation. Une égalité de mots ne produit pas d’exactMatch et ne convertit aucune observation suggested en validated. Les profils de vie personnelle sont des collections de consultation, sans mutation de la hiérarchie officielle. Getty est un fragment ouvert : une référence à un parent hors sélection n’est pas une erreur ni une racine inventée.
