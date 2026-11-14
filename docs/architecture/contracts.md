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
