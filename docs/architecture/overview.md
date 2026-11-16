# Architecture — philosophie Unix et contrats découplés

## Flux unidirectionnel

`inventory -> exif-normalizer -> media-observation -> review -> export`. Les modules lisent des manifestes stables (JSON Lines ou SQLite en lecture explicitement contractuelle) et écrivent leurs propres résultats. Le module `review` arbitre ; `export` ne reçoit que des assertions validées ou des propositions explicitement marquées.

## Responsabilités

| Module | Entrée | Sortie | Dépendance extérieure |
|---|---|---|---|
| `inventory` | Chemin local, mode lecture seule | Manifest JSONL, hash SHA-256, erreurs | Python, ExifTool en sous-processus local |
| `vision` | Photo locale + prompt/version | Objets, scènes, description, provenance | Ollama localhost, modèle Qwen3-VL officiel |
| `ocr` | Photo locale | Texte brut, quadrilatères, orientation, provenance | PaddleOCR local |
| `faces` (futur) | Photo et bibliothèque opt-in | Vecteurs, identités candidates | Moteur facial dédié et contrôlé |
| `geo` (futur) | GPS EXIF | Coordonnées validées, région et adresse approximative | Référentiel OSM local ; Nominatim auto-hébergé facultatif |
| `semantic` (futur) | Observations + confirmations | Relations versionnées et graphe RDF | SKOS/PROV-O, stockage local |
| `xmp_export` | Concepts acceptés/corrigés | Copies identiques, sidecars XMP, journal réversible | Python ; relecture ExifTool séparée |
| `digikam_lab` | Lot exporté privé | Nouvelles copies, empreintes, comparaison XML | Python ; observation digiKam manuelle séparée |

Éviter les imports directs entre modules de haut niveau. Fournir à chacun une CLI ou un adaptateur de processus ; contrats versionnés dans `schemas/`. L'orchestrateur gère files d'attente, limitation de la mémoire, retries et persistance d'état ; il ne contient pas d'algorithmes IA.

## Règles des phases 1 et 2

1. **Lecture seule des images originales.** Ne jamais exécuter `exiftool -overwrite_original` pendant ce pilote.
2. Parcours récursif sans suivre par défaut les liens symboliques ou jonctions ; résister aux boucles et aux permissions partielles ; chemin Unicode, longues paths, photos corrompues.
3. SHA-256 du contenu pour les doublons **exacts** ; ne pas confondre avec doublons visuels.
4. Inventaire déterministe et reprenable : même fichier, même empreinte, même identifiant, extraction EXIF conservée séparément.
5. Passer par un sérialiseur JSON avec validation de schéma, limites de taille et journal sans secrets.
6. Ollama `http://127.0.0.1:11434` seulement ; vérifier que le modèle est local, désactiver tout fallback réseau et documenter un test réseau hors ligne.
7. OCR dédié pour lire le texte ; le modèle de vision peut aider à comprendre le contexte mais ne remplace pas le moteur de reconnaissance de caractères.
8. Chaque modèle reçoit une version, un digest ou identifiant reproductible, paramètres, horodatage et provenance.

## Frontières et plugins futurs

Les interfaces HTTP internes ne sont pas obligatoires : sous Windows, un processus Python qui appelle Ollama en localhost et des exécutables OCR peut suffire. « Indépendant » signifie contrats et cycles de vie séparés ; ne pas déployer huit services pour un pilote de 150 photos.

Références : https://www.iptc.org/std/photometadata/specification/ ; https://www.w3.org/TR/prov-o/ ; https://www.w3.org/TR/skos-reference/


## État implémenté du noyau Phase 1

L'orchestrateur de l'inventaire réside actuellement dans `photosemantique/inventory.py` et n'utilise aucun serveur réseau. Le service ExifTool est un sous-processus local et `photosemantique/storage.py` possède la persistance SQLite. Ce monolithe modulaire est intentionnel pour limiter la charge de maintenance au début. Voir le [tutoriel illustré](../tutorial/phase-1.md).

**Phase 2 expérimentale :** préparation HEIC, vision locale et OCR sont disponibles dans `phase2.py`. La revue humaine et l'export XMP sur copies sont implémentés ; le laboratoire d'interopérabilité prépare les preuves de fichiers sans certifier une validation visuelle. Les modules faces/geo et le graphe sémantique restent futurs. Voir les tutoriels [Phase 2](../tutorial/phase-2.md), [revue](../tutorial/revue-mots-cles.md), [export](../tutorial/export-xmp.md) et [digiKam](../tutorial/digikam-lab.md).
