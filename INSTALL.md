# Installation de GNU APMG — Phase 1, Windows 11

**Version :** `0.2.0a1` · CLI Python fonctionnelle ; modèles IA et OCR de Phase 2 **non intégrés**.

## 1. Prérequis

- **Python 3.12 ou ultérieur** (sans droits administrateur lorsque déjà installé pour l'utilisateur).
- **ExifTool** depuis https://exiftool.org/ pour lire les métadonnées EXIF/IPTC/XMP. Le mode `--no-exif` permet uniquement de tester l'inventaire sans extraction.
- Espace disque pour une base SQLite contenant les chemins privés et les tags EXIF ; **stockage hors du dossier photo et hors du dépôt Git**.
- Ni Ollama ni GPU ne sont requis pour cette phase ; RTX 4070 et PaddleOCR seront utilisés en Phase 2.

## 2. Utilisation sans installation Python supplémentaire

Ouvrir PowerShell **à la racine du code extrait ou cloné**, puis :

```powershell
py --version
py -m gnu-apmg --version
py -m unittest discover -s tests -p 'test_*.py'
```

Si le dépôt est cloné, utiliser la même racine pour les commandes. Un environnement virtuel est facultatif pour cette version sans dépendance Python externe ; il reste recommandé pour la suite.

## 3. Analyse réelle avec ExifTool local

```powershell
& "C:\Outils\ExifTool\exiftool.exe" -ver
py -m photosemantique scan "C:\Photos\Pilote" `
  --db "C:\PhotoSemantique-Etat\inventaire.sqlite" `
  --jsonl "C:\PhotoSemantique-Etat\inventaire.jsonl" `
  --exiftool "C:\Outils\ExifTool\exiftool.exe"
py -m photosemantique report --db "C:\PhotoSemantique-Etat\inventaire.sqlite"
```

Les chemins sont des exemples fictifs : ne pas les copier tels quels sans les adapter. Le manifeste JSONL contient des **chemins locaux privés** et ne doit jamais être envoyé dans Git.

## 4. Test technique limité sans ExifTool

```powershell
py -m photosemantique scan "C:\Photos\Pilote" `
  --db "C:\PhotoSemantique-Etat\inventaire.sqlite" --no-exif
```

Ce mode ne produit pas de métadonnées EXIF ; il sert à vérifier parcours, hashes, SQLite et reprise. L'absence d'ExifTool en mode normal conduit à une erreur claire, pas à une réussite trompeuse.

## 5. Installation de développement facultative

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
gnu-apmg --version
```

L'installation editable nécessite `setuptools` selon `pyproject.toml`. Elle peut déclencher un téléchargement la première fois ; pour une installation **strictement hors ligne**, préinstaller les outils de construction ou utiliser directement `py -m photosemantique` depuis le répertoire source.

## 6. Validation et confidentialité

```powershell
py scripts/check_repository.py
py scripts/generate_notice.py --check
py -m unittest discover -s tests -p 'test_*.py'
```

- La racine source est explorée en lecture seule, sans suivi de liens symboliques/jonctions par défaut.
- Les originaux ne sont **jamais** modifiés ; la base SQLite et le manifeste doivent être à l'extérieur de la source et de Git.
- Les tags et chemins EXIF peuvent comporter des données personnelles : ne pas partager les fichiers produits.
- Ne pas écrire des métadonnées sur les photos à ce stade : rollback d'export prévu pour une phase ultérieure.

**Tutoriel illustré :** [docs/tutorial/phase-1.md](docs/tutorial/phase-1.md).

## 7. Préparation de la Phase 2 (non livrée)

Ollama local et Qwen3-VL 8B quantifié sont des cibles de conception pour la RTX 4070 (12 Go VRAM). PaddleOCR sera évalué sur CPU puis éventuellement GPU. Les dépendances, modèles et licences devront être épinglés puis vérifiés avant toute diffusion d'un paquet exécutable.


## État vérifié de cette reprise

La distribution Python porte le nom `gnu-apmg`. Après installation, `gnu-apmg` et l'alias historique `photosemantique` utilisent la même CLI. Sans installation, `python -m photosemantique` fonctionne depuis la racine. L'installation du paquet n'a pas été vérifiée lors de cette reprise ; le parcours depuis les sources l'a été.

Sur Windows avec Python 3.13.6 : 19 tests exécutés, 17 réussis et 2 ignorés (liens symboliques). ExifTool n'est pas présent dans le PATH ; son exécutable doit être installé puis indiqué avec `--exiftool` pour le pilote EXIF réel. Aucun téléchargement d'outil ni de modèle n'a été effectué.
