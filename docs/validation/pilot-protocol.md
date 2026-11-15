# Protocole de validation — 100 à 200 photos (local et confidentiel)

## Constitution du pilote

Construire un ensemble **privé** représentatif (cible 150 photos) : prises récentes/anciennes, JPEG/PNG/HEIC/RAW si disponibles, EXIF complets/absents, GPS présent/absent, faces (uniquement avec autorisation), texte net/flou, petits/grands fichiers, objets aériens/terrestres, images corrompues, copies exactes, images visuellement proches, noms Unicode et chemins longs. **Ne pas publier les photos ni leurs métadonnées.**

Créer un tableau local de vérité terrain avec 1 ligne/photo, ID pseudonyme, liste d'objets, texte OCR vérifié, personnes *seulement si consenties*, lieu confirmé ou inconnu. Revue humaine, double annotation sur sous-échantillon si possible ; distinguer absence de preuve et erreur.

## Phase 1 — attentes et critères de sortie

| Mesure | Méthode | Critère de validation |
|---|---|---|
| Couverture d'inventaire | Comparer à une liste indépendante des fichiers du répertoire | 100 % des fichiers éligibles représentés ou erreur explicitée |
| Intégrité | SHA-256 avant/après sur tous les originaux | 0 différence |
| Doublons exacts | Déposer des copies octet pour octet | Tous les doublons exacts identifiés ; pas d'inférence visuelle |
| EXIF | Échantillon des tags confrontés à ExifTool direct | Aucune corruption silencieuse ; tags absents marqués absents |
| Résilience | Fichiers illisibles, interruption et reprise | Aucune perte silencieuse ; aucune boucle infinie |

## Phase 2 — métriques, sans imposer des chiffres inventés

- **Vision :** exactitude des catégories par type d'objet (précision, rappel, F1) ; qualité des descriptions sur grille de relecture et taux d'hallucinations factuelles.
- **OCR :** CER/WER sur texte transcrit et rappel des inscriptions visibles ; distinguer détection et transcription.
- **Performances :** durée médiane et p95/photo, VRAM maximale, OOM, RAM, coût en énergie si mesurable.
- **Privacité :** traitement possible avec réseau désactivé ; aucune requête sortante, aucune photo personnelle dans logs et archives.
- **Reproductibilité :** figer versions, prompts, dimensions d'entrée et empreintes de modèle. Documenter les sorties non déterministes.

## Portes de sortie

Validation exige un rapport des erreurs, une revue qualitative représentative, une procédure de rollback et la signature du mainteneur. Les seuils de précision seront établis à partir de l'usage réel et des résultats du pilote, pas inventés à l'avance.


## État de mise en œuvre Phase 1 au 13 novembre 2026

- CLI `scan` et `report` implémentées, source en lecture seule et base hors source.
- Tests synthétiques automatisés dans `tests/test_inventory_phase1.py` (SHA-256, doublons, Unicode, liens, erreurs, ExifTool simulé, interruption et relance).
- **Tests pilotes réels encore non effectués.** L'outil ExifTool réel n'était pas installé dans l'environnement de construction ; effectuer la validation Windows 11 avant tout avis d'interopérabilité EXIF/IPTC/XMP.
- Avant/après du SHA-256 à faire indépendamment avec la procédure PowerShell du [tutoriel illustré](../tutorial/phase-1.md).
- Critère de sortie P1.9 : revue d'erreurs, comparaison d'empreintes et validation du mainteneur. Tant que cela n'est pas fait, la Phase 1 reste **pré-alpha**.


## État au 15 novembre 2026

Les assertions « encore non effectué » ci-dessus décrivent le 13 novembre. La Phase 1 a depuis été testée sur 200 copies, dont 100 HEIC, sans erreur et avec empreintes inchangées. La Phase 2 pré-alpha prépare 10 HEIC et teste OCR/vision sur 3 dérivés ; vision acceptée sur 2/3 et réponse tronquée refusée sur 1/3. Cela ne valide pas la qualité sémantique. La vérité terrain humaine, CER/WER, hallucinations et métriques sur un corpus représentatif restent à établir avant élargissement. Voir les deux tutoriels.
