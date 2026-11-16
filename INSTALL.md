# Installation de GNU APMG — Phase 1, Windows 11

## Export XMP sur copies — jalon X

Le [tutoriel illustré d'export](docs/tutorial/export-xmp.md) décrit la simulation, les champs standards, la relecture et l'annulation. Pas de dépendance nouvelle ; utiliser l'environnement Phase 2 et ExifTool déjà installé.

```powershell
& .\scripts\Export-ValidatedKeywords.ps1 -SessionDirectory 'D:\EtatPrive\revue-001' -ImagesDirectory 'D:\Photos\Pilote' -Output 'D:\EtatPrive\plan-xmp.json' -PlanOnly
& .\scripts\Export-ValidatedKeywords.ps1 -SessionDirectory 'D:\EtatPrive\revue-001' -ImagesDirectory 'D:\Photos\Pilote' -Output 'D:\EtatPrive\export-001'
& .\scripts\Undo-KeywordExport.ps1 -ExportDirectory 'D:\EtatPrive\export-001'
```

Ces chemins sont fictifs. Choisir de nouveaux fichiers/dossiers privés, hors Git, de la session et des images sources. L'annulation est optionnelle : ne pas lancer la troisième commande si l'on souhaite conserver les XMP exportés. Les copies restent présentes après annulation. Les images copiées conservent leurs métadonnées intégrées et doivent rester privées.

## Revue des mots-clés — ajout du jalon V

Voir le [tutoriel illustré](docs/tutorial/revue-mots-cles.md). Utiliser l'environnement Phase 2 existant ; aucune installation ni relance de modèle supplémentaire n'est nécessaire.

```powershell
& .\scripts\New-KeywordReview.ps1 -Observations @('D:\EtatPrive\photo-vision.jsonl') -SessionDirectory 'D:\EtatPrive\revue-001'
& .\scripts\Import-KeywordDecisions.ps1 -SessionDirectory 'D:\EtatPrive\revue-001' -DecisionsFile 'C:\Telechargements\decisions.json' -Actor 'moi'
```

Adapter ces chemins fictifs. `-PreparedDirectory` fournit les dérivés à inclure comme aperçus et `-Open` ouvre la page. Choisir un nouveau dossier privé, hors Git et des sources. Les clics dans le navigateur ne modifient pas la base : exporter puis importer le fichier de décisions. Fermer puis rouvrir `review.html` après l'import pour charger la nouvelle révision.

Pour régénérer la page sans modifier les choix, utiliser le Python de `.venv-phase2` avec `-m photosemantique.review render SESSION`. Le sous-ordre `status SESSION` affiche seulement un état agrégé. Aucun serveur HTTP à démarrer.

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


## Validation ExifTool réelle — mise à jour du 15 novembre 2026

ExifTool portable **13.63** est installé dans le dossier frère `../outils-locaux/exiftool-13.63/exiftool-13.63_64/`. Conserver `exiftool_files` à côté de `exiftool.exe`. Aucun binaire n'est distribué par Git et aucun changement global du PATH n'a été effectué. L'état « ExifTool absent » des sections datées précédentes est historique.

Depuis la racine du projet, ouvrir PowerShell et exécuter :

```powershell
& .\scripts\Test-ExifTool.ps1
```

Si votre outil est ailleurs :

```powershell
& .\scripts\Test-ExifTool.ps1 -ExifTool 'C:\Outils\ExifTool\exiftool.exe'
```

Le script lance uniquement les tests synthétiques, utilise le vrai outil et restaure sa variable d'environnement à la sortie. Il ne lance jamais le pilote privé. Il retourne le code de sortie de la suite de tests ; un échec n'est pas masqué. Si PowerShell bloque l'exécution selon votre politique locale, ne changez pas la politique globale ; les commandes Python ci-dessous constituent une alternative :

```powershell
$env:GNU_APMG_EXIFTOOL = 'C:\Outils\ExifTool\exiftool.exe'
python -X utf8 -m unittest discover -s tests -p 'test_*.py' -v
```

Sans exécutable détecté ni variable définie, le test réel est explicitement ignoré. Sur le PC vérifié : 21 tests, 19 réussis, 2 ignorés pour restrictions sur les liens symboliques. Installation du paquet Python et décodage HEIC restent non testés ; utilisation depuis les sources vérifiée.

Distribution et sommes de contrôle : [site officiel](https://exiftool.org/), [checksums 13.63](https://exiftool.org/checksums-13.63.txt). Le ZIP téléchargé doit correspondre à la somme officielle avant extraction. La version locale a été vérifiée avec `-ver`.


## Phase 2 expérimentale — 15 novembre 2026

Les sections précédentes décrivent les états historiques. La préparation HEIC, la vision et l'OCR CPU sont désormais disponibles depuis les sources : [guide détaillé](docs/tutorial/phase-2.md). Elles sont optionnelles et n'ajoutent aucune dépendance obligatoire à la Phase 1.

```powershell
& .\scripts\Setup-Phase2.ps1 -DownloadVisionModel -DownloadOcrModels
& .\scripts\Invoke-Phase2.ps1 -SourceFile 'D:\Photos\essai.heic' -OutputDirectory 'D:\EtatPrive\essai-001' -Vision -Ocr
```

Adapter ces chemins fictifs. Le script d'analyse exige un nouveau dossier privé, hors sources et Git. Sans `-Vision -Ocr`, il effectue uniquement la préparation. Les options d'installation peuvent télécharger plusieurs Go ; vérifier l'espace libre avant de les lancer. Sur ce PC, `.venv-phase2` pointe vers l'environnement du projet sur D:. Ne pas supprimer sa cible en pensant supprimer un simple cache.

Versions observées Windows/CPython 3.13 : Pillow 13.0.0, pillow-heif 1.8.1, jsonschema 4.26.0, PaddleOCR 3.7.0 et PaddlePaddle 3.3.1. `requirements-phase2-windows.lock.txt` liste les versions transitives observées. Ce fichier ne prouve ni compatibilité multiplateforme ni audit complet des licences. La CI installe seulement les dépendances légères de préparation ; les modèles IA/OCR ne sont pas téléchargés en CI.

Tests dans cet environnement :

```powershell
& .\scripts\Test-ExifTool.ps1 -Python '.\.venv-phase2\Scripts\python.exe'
```

29 tests exécutés localement : 27 réussis, 2 ignorés. OCR CPU : `enable_mkldnn=False` contourne l'erreur oneDNN observée. La wheel de développement a été construite avec le schéma embarqué ; aucune release ni installation globale du paquet n'a été effectuée.


## Taxonomie locale — sans modèles ni connexion réseau

Ouvrir `docs/ontology/catalogue.html` par double-clic dans un navigateur. Le catalogue contient seulement les vocabulaires publics ; recherche et filtres fonctionnent hors ligne. La version Markdown est dans `docs/ontology/TAXONOMIE-PERSONNELLE.md`.

```powershell
python -X utf8 -m photosemantique.taxonomy mariage
python -X utf8 -m photosemantique.taxonomy planeur --source getty
python -X utf8 scripts/build_taxonomy.py --check
```

La consultation et la reconstruction utilisent uniquement la bibliothèque standard Python et les sources figées. `rdflib==7.6.0` est optionnel pour valider l’export RDF/SKOS ; il est installé dans l’environnement Phase 2 et dans la CI, et disponible via l’extra `taxonomy-validation`. Les données distribuées conservent leurs licences séparées, expliquées dans `third_party/vocabularies/README.md`.

## Laboratoire digiKam facultatif sous Windows

La distribution portable officielle 9.1.0 Qt6 Windows 64 bits a été préparée hors dépôt sur le poste pilote. Elle n'est ni embarquée ni téléchargée automatiquement par le script du projet. Le [guide illustré](docs/tutorial/digikam-lab.md) précise provenance, empreinte vérifiée, limites d'isolation et procédure sur copies. `scripts/Invoke-DigiKamLab.ps1` propose `Prepare`, `Open` et `Compare` ; son lancement par défaut utilise le laboratoire privé déjà préparé. L'environnement `.venv-phase2` doit exister pour les opérations Python ; la comparaison XML elle-même n'exige aucune bibliothèque supplémentaire.
