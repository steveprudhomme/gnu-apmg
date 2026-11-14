# Composant `inventory` — Phase 1

**État :** implémenté et testé sur données synthétiques dans le paquet `photosemantique/` ; validation sur 100–200 photographies réelles encore à faire.

## Fonctions existantes

- Exploration récursive en lecture seule, extensions photo connues, pas de suivi des liens symboliques/jonctions.
- SHA-256 en flux avec détection d'une modification du fichier pendant le hachage.
- Lecture ExifTool en JSON (`-j -G1:4 -a -s`) lorsqu'un exécutable local est indiqué ; aucune écriture ExifTool.
- Base SQLite avec migrations, `assets`, `file_locations`, `scan_items`, `scans`, `source_metadata`.
- Manifest JSONL privé facultatif et commandes `scan` / `report`.
- Scans répétés idempotents pour les identités de contenus et d'emplacements ; nouvel historique de scan à chaque exécution.

## Contrat CLI

```text
python -m photosemantique scan SOURCE --db DB [--exiftool EXE] [--jsonl MANIFEST] [--no-exif]
python -m photosemantique report --db DB
```

Codes de sortie : `0` sans erreur de fichier, `2` si erreurs partielles, `1` erreur fatale. `--no-exif` signale explicitement l'absence d'extraction.

## Limites

Les fichiers sont *candidats* selon leur extension : aucun décodeur d'image ne confirme leur validité. L'intégration avec ExifTool réel sous Windows et les formats RAW/HEIC n'est pas testée dans le présent environnement. Les liens suivis dans des chemins parents, la concurrence entre plusieurs scans et la récupération après coupure brutale du système demandent des tests additionnels. Les métadonnées privées sont stockées seulement dans la base locale.

Voir [tutoriel illustré](../../docs/tutorial/phase-1.md) et [tests](../../tests/test_inventory_phase1.py).
