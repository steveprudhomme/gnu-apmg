# GNU APMG — feuille de route

Nom complet : GNU Automatic Picture Metadata generator. Ancien nom : GNU APMG. Dépôt public créé : `steveprudhomme/gnu-apmg`. Les commits documentaires initiaux ont été publiés sur main.

État vérifié le 14 novembre 2026 : sources Phase 1 restaurées et adaptées à GNU APMG ; validation synthétique Windows réussie. ExifTool réel et pilote privé restent à valider.

## 0. Reprendre le projet avant toute modification du code

- [x] Examiner le dossier Windows de développement : vide à la première inspection.
- [x] Examiner le second dossier de travail OneDrive : vide à la première inspection.
- [x] Consulter la conversation référencée : cinq échanges accessibles, aucune pièce jointe et aucun curseur vers les échanges antérieurs.
- [x] Interroger GitHub : réponse 404 pour steveprudhomme/photosemantique. L'absence du dépôt ne peut pas être distinguée d'un défaut d'accès.
- [x] Vérifier les outils : Git 2.50.1, GitHub CLI 2.103.3, Python 3.13.6.
- [x] Vérifier l'authentification locale GitHub : jeton signalé invalide, sans lecture ni copie de sa valeur.
- [x] Rechercher les sources dans les deux espaces de travail et les archives à la racine de Téléchargements : aucun livrable correspondant trouvé. La recherche récursive générale dans Téléchargements a été interrompue ; elle ne constitue pas un inventaire complet du PC.
- [x] Créer et vérifier le commit documentaire distinct contenant cette feuille de route avant tout changement du code : `84cc913`.

## 1. Récupérer et contrôler les livrables

- [ ] Obtenir l'archive source Phase 1 et, si disponible, photosemantique-phase1-v0.2.0a1-history.bundle, ou leur emplacement exact.
- [ ] Inspecter la liste des fichiers de l'archive avant extraction ; refuser les chemins sortant du dossier cible.
- [ ] Vérifier le bundle avec git bundle verify dans un dépôt temporaire ; examiner les branches, les commits et les fichiers suivis.
- [ ] Restaurer l'historique récupéré en préservant le présent commit documentaire.
- [ ] Lire les instructions du projet et le cahier des charges ; relever l'architecture, les dépendances et les critères d'acceptation réels.
- [ ] Détailler ici les sous-étapes fonctionnelles confirmées, puis effectuer un nouveau commit documentaire avant de coder.

## 2. Développer et tester la Phase 1

Le contenu fonctionnel de cette phase n'est pas présent dans les échanges récupérés. Ne pas reconstruire arbitrairement les exigences à partir du seul nom du projet.

- [ ] Installer les dépendances déclarées dans un environnement local isolé.
- [ ] Exécuter les tests existants et noter leur résultat de départ.
- [ ] Développer chaque fonction confirmée et ses tests pertinents avec des données synthétiques.
- [ ] Vérifier les entrées invalides, les erreurs d'accès, les formats pris en charge et la préservation des originaux selon le cahier des charges.
- [ ] Exécuter les contrôles prescrits et un parcours complet sur un exemple synthétique.
- [ ] Consigner les commandes, versions, résultats et limites effectivement observés.

## 3. Documenter et livrer

- [ ] Mettre à jour README, cette feuille de route et le tutoriel après chaque étape.
- [ ] Illustrer les parcours avec des exemples synthétiques ; exclure photos privées et données biométriques.
- [ ] Vérifier les fichiers et l'historique destinés à la publication : aucun secret ni contenu privé.
- [ ] Effectuer les commits de développement et documentation avec une sélection explicite des fichiers.
- [ ] Rétablir l'accès GitHub, vérifier le dépôt cible et l'autorisation de publication, puis publier et contrôler le commit distant.

Les « 17 tests réussis » évoqués dans l'ancienne conversation ne sont pas des tests exécutés dans cet espace.


## Reprise depuis les archives — 14 novembre 2026

Les deux archives fournies ont été inventoriées avant extraction : chemins relatifs vérifiés, aucune traversée de répertoire ni lien symbolique. Les deux prompts fondateurs servent de référence aux exigences ; leurs anciennes demandes de réponse ne remplacent pas la tâche actuelle. Aucun bundle Git fourni : les anciens commits ne sont pas récupérables depuis ces ZIP.

| ID | Sous-étape supplémentaire | Critère de sortie | État |
| --- | --- | --- | --- |
| R1 | Examiner archives et exigences | Liste des fichiers, contrôle des chemins et empreintes des ZIP | Fait |
| R2 | Importer Phase 1 sans écraser les documents de reprise | Conserver l'historique local et les documents initiaux ; archiver la feuille de route précédente comme référence | Fait |
| R3 | Adapter l'identité GNU APMG | README, installation, CLI et distribution cohérents ; conserver le module Python photosemantique pour compatibilité | Fait |
| R4 | Exécuter la validation de départ Windows | Tests synthétiques, contrôles de structure et notices ; résultats mesurés | Fait |
| R5 | Corriger les défauts constatés | Régressions pertinentes ; vérifier notamment les collisions entre sorties et l'intégrité source | Fait |
| R6 | Vérifier un parcours CLI synthétique | Trois fichiers, deux contenus, un groupe de doublons ; hash avant/après identique ; deuxième scan idempotent | Fait |
| R7 | Synchroniser les documents et publier | Journal réel, limites ExifTool/pilote explicites, sélection de fichiers sans données privées, commit puis vérification distante | Fait |

OBJECTIVE : rendre le socle Phase 1 récupéré utilisable sous GNU APMG. GOAL : inventaire local en lecture seule et résultats reproductibles. SUCCESS CRITERIA : contrôles automatisés réussis et intégrité synthétique conservée. IMPLEMENTATION PLAN : R1 à R7 dans cet ordre. OWNER : mainteneur du projet, assisté par Codex.

Le pilote privé 100–200 photos et l'extraction via un véritable ExifTool restent des validations distinctes. Aucun lancement de l'IA, OCR ou reconnaissance faciale durant cette reprise.

- SHA-256 `PhotoSemantique-Architecture.zip` : `bad8019dd1c9ad5a4f4ea2734e3ca1f295a2502b3a05993018ff91f9d94478d6`.

- SHA-256 `PhotoSemantique-Phase1.zip` : `6b68dc9949ec381fd16cbf3286a5575a4dde05fabbfe4adbbb1ab20767ad17fe`.


### Résultats de la reprise

- Plan préalable enregistré dans le commit `2df59b6`, avant import et modification du code.
- Phase 1 importée ; documents initiaux conservés dans `docs/archive/`. L'archive Architecture a été inventoriée comme référence antérieure, sans écraser les versions plus récentes de Phase 1.
- Distribution nommée `gnu-apmg`, commande installable `gnu-apmg` ; ancienne commande et module Python `photosemantique` conservés. Aucun rattachement officiel au projet GNU n'est revendiqué par le nom.
- 19 tests exécutés : 17 réussis, 2 ignorés (création de liens symboliques non autorisée). Corrections Windows : fermeture explicite des connexions dans les tests et encodage UTF-8 des sous-processus.
- Protections supplémentaires : refus d'une base ayant des liens physiques et des manifestes visant la base ou ses fichiers SQLite de journalisation.
- Deux scans CLI synthétiques : trois fichiers, deux contenus, un groupe de doublons, zéro erreur, empreintes source inchangées.
- ExifTool absent du PATH : extraction réelle non exécutée. Les tests ExifTool utilisent un processus simulé. Pas de test GPU, IA, reconnaissance faciale ou pilote privé.
- Audit des licences transitives, verrouillage des actions CI, couverture, signatures et empaquetage de release restent à réaliser ; NOTICE est une liste des composants envisagés, pas un audit de distribution.

La feuille de route historique détaillée des phases est conservée dans [docs/archive/phase1-roadmap.md](docs/archive/phase1-roadmap.md). Ses résultats antérieurs ne remplacent pas le présent journal.


## Jalon E — ExifTool réel et préparation du pilote privé (14 novembre 2026)

OBJECTIVE : valider la lecture documentaire réelle avant tout pilote privé. GOAL : extraction UTF-8 reproductible, originaux intacts, données privées hors Git. SUCCESS CRITERIA : images synthétiques valides avec tags connus, erreurs explicites sur corruption, deuxième scan stable, tests locaux et CI réussis. OWNER : mainteneur avec assistance Codex.

| ID | Nouvelle sous-étape | Critère de sortie | État |
| --- | --- | --- | --- |
| E1 | Enregistrer ce plan avant travail | Commit documentaire préalable | Fait |
| E2 | Vérifier la distribution officielle Windows ExifTool | URL officielle, version et SHA-256 local consignés ; distinguer empreinte locale et signature officielle | Fait |
| E3 | Installer sans privilèges administrateur | Outil portable dans un espace local exclu de Git ; exécuter -ver ; aucun changement global du PATH | Fait |
| E4 | Générer un corpus synthétique valide | PNG contenant des champs documentaires connus, noms Unicode, copie exacte, fichier corrompu ; aucun média privé | Fait |
| E5 | Tester l'extraction réelle | Tags attendus retrouvés dans SQLite, erreurs de corruption séparées, SHA-256 source avant/après identiques ; scan répété stable | Fait |
| E6 | Corriger les défauts réels | Régression automatisée si défaut ; ne pas masquer les erreurs ni altérer les originaux | Fait |
| E7 | Préparer le pilote 100–200 photos | Procédure explicite, source fournie par l'utilisateur, sorties privées hors Git, contrôle indépendant avant/après et seuils d'arrêt | Fait |
| E8 | Documenter et publier | Tutoriel illustré avec schéma honnête, INSTALL/README/ROADMAP synchronisés, rapport agrégé sans chemins privés, commits et contrôles CI | Fait |

Le traitement des photos privées attend leur emplacement précis. Il ne sera pas lancé sur un dossier choisi arbitrairement. Les binaires téléchargés, images synthétiques générées et bases restent hors des fichiers versionnés. Le test ExifTool doit être facultatif en CI si aucun outil réel n'y est installé, avec indication explicite du saut.


### Complément E6/E7 — HEIC et avertissements ExifTool

Avant correction du lecteur et lancement privé :

- Distinguer explicitement un avertissement ExifTool (parfois code retour 0) d'une extraction complète. Politique conservatrice de cette phase : résultat metadata_failed avec diagnostic générique si un tag Warning est retourné, tout en conservant le SHA-256 et en poursuivant les autres fichiers.
- Ajouter une régression simulée et le cas réel JPEG tronqué ; un simple texte avec extension JPG n'est pas nécessairement reconnu comme corrompu par ExifTool.
- Le dossier proposé contient 2 118 images éligibles, au-delà du pilote prévu. Constituer un échantillon déterministe d'au plus 200 copies privées, en incluant HEIC/HEIF et les autres formats présents ; conserver la liste des sources uniquement dans l'état privé.
- Contrôler empreintes originales avant copie, copies avant/après scan et originaux après scan. Vérifier les tags et les statuts HEIC séparément ; ne pas confondre lecture de métadonnées et décodage des pixels pour l'IA.
- Les indicateurs OneDrive signalent des fichiers potentiellement dématérialisés : leur lecture peut entraîner un téléchargement par OneDrive. Le programme n'envoie aucun média à une API ; aucune garantie d'absence de trafic du client de synchronisation n'est revendiquée.
- Consigner uniquement des métriques agrégées dans Git ; conserver noms, chemins, empreintes, GPS et diagnostics détaillés hors Git.

Le manque de place initial a été résolu par l'utilisateur. ExifTool portable 13.63 a ensuite été extrait et sa version exécutée avec succès. Le test de corruption reste à corriger avant le pilote.


### Bilan E — 15 novembre 2026

- Plans préalables : `136e287`, puis complément HEIC `940289a`, tous deux avant les modifications correspondantes.
- ExifTool portable 13.63 installé hors Git et sans changement du PATH. ZIP Windows 64 bits : SHA-256 `7a4bff4b1d6ee15adef882837847f76c0ed23228d294feed285939b6c9b293bd`, identique au fichier officiel de sommes de contrôle. Aucune signature numérique indépendante vérifiée.
- Les premières adresses SourceForge ont renvoyé du HTML, rejeté ; le lien direct fourni par la page a permis le téléchargement vérifié. Extraction initiale interrompue par disque plein, puis fichiers incomplets nettoyés ; l'utilisateur a libéré l'espace avant installation complète.
- Lecture des noms Unicode corrigée avec un fichier d'arguments UTF-8 sur stdin (`-charset filename=UTF8 -@ -`). Aucun fichier temporaire d'arguments dans les sources. Les noms contenant un saut de ligne sont refusés explicitement.
- Les tags Warning sont traités prudemment en échec de métadonnées, même avec un code ExifTool 0 ; le hachage reste conservé. Cela peut inclure des avertissements bénins : diagnostic humain nécessaire, pas preuve automatique de corruption.
- Tests par `scripts/Test-ExifTool.ps1` : 21 exécutés, 19 réussis, 2 ignorés (liens symboliques interdits). Test réel : PNG valides avec titres et descriptions UTF-8, doublons, JPEG tronqué, deux scans et empreintes inchangées.
- Pilote privé : 200 copies (100 HEIC, 50 JPG, 50 PNG), deux scans, 200 indexées à chaque scan, zéro erreur, 200 contenus uniques, 24 035 tags stockés au total. Cent valeurs FileType HEIC confirmées. SQLite intègre et aucune violation de clé étrangère.
- Empreintes des 200 sources et des copies vérifiées avant/après : zéro changement. Sélection ordonnée par format, non aléatoire ; résultat limité à ces fichiers, sans garantie sur tous les HEIC/HEIF.
- Durée de la partie deux scans et vérification finale : 79,7 secondes, hors préparation des copies ; pas une mesure de débit généralisable.
- État privé conservé hors Git : copies, correspondances source/copie, empreintes, base et manifeste. La documentation publique ne contient que des nombres agrégés.
- HEIC : lecture des métadonnées et hachage validés ; décodage des pixels, miniatures, conversion, OCR, vision et export encore non validés. Aucun traitement IA ou écriture documentaire sur les sources.

Voir [le tutoriel](docs/tutorial/phase-1.md#11-exiftool-réel-et-pilote-heic--bilan-du-15-novembre-2026) et [le protocole de relance privée](docs/validation/pilot-runbook.md).

Publication vérifiée : commit de code `56bc201`. [Contrôles GitHub Windows et Linux réussis](https://github.com/steveprudhomme/gnu-apmg/actions/runs/43687539029). Le présent complément est exclusivement documentaire ; les tests ExifTool réels restent vérifiés localement, et peuvent être ignorés en CI lorsque l’exécutable est absent.


## Phase 2 — préparation HEIC, vision locale et OCR (15 novembre 2026)

OBJECTIVE : produire des propositions documentaires locales traçables, sans changer les originaux. GOAL : préparation HEIC vérifiée puis premiers essais vision/OCR séparés. OWNER : mainteneur assisté de Codex. SUCCESS CRITERIA : tests synthétiques, intégrité privée, provenance de modèle, sorties explicitement suggested et bilan honnête de qualité.

| ID | Sous-étape avant implémentation | Critère de sortie | État |
| --- | --- | --- | --- |
| P2A | Plan et environnement | Commit préalable, dépendances optionnelles isolées, espace disque contrôlé | Planifié |
| P2B | Décodage HEIC et préparation | Pillow/pillow-heif ; image principale, orientation appliquée une fois, copie RGB réduite hors sources/Git sans EXIF/GPS ; ICC converti vers sRGB si disponible ; limites HDR/couleurs explicites | Planifié |
| P2C | Contrat des observations | Schéma JSON strict, provenance version/prompt/digest, statut suggested, confiance non calibrée null ; stockage privé append-only, pas de promotion humaine automatique | Planifié |
| P2D | Vision Ollama locale | Endpoint de boucle locale fixe, pas de redirection/proxy externe, aucun téléchargement implicite ; images réduites ; modèle existant ou choix confirmé ; réponse structurée bornée et validée | Planifié |
| P2E | OCR PaddleOCR CPU | Installation isolée selon wheels disponibles, modèles locaux explicites, pas de téléchargement durant analyse ; texte/boîtes et score brut distinct de confidence ; échec clair si indisponible | Planifié |
| P2F | Reprise et protections | Empreinte source avant/après préparation, paramètres de cache versionnés ou nouvelle sortie ; erreurs partielles visibles et aucun média privé publié | Planifié |
| P2G | Tests et petit pilote | Images synthétiques avec texte connu, tests unitaires sans IA et essais réels séparés ; quelques copies HEIC du pilote privé ; mémoire et temps observés ; qualité humaine encore à annoter | Planifié |
| P2H | Scripts utilisateur et documentation | Scripts relançables, tutoriel illustré Phase 2, README/INSTALL/contrats/FAQ/manifestes mis à jour, commits et publication vérifiée | Planifié |

Constats préalables : Ollama 0.40.13 disponible, RTX 4070 12 Go détectée ; Qwen3-VL 8B absent, Qwen3.5 9B déjà présent. Python 3.13 et Pillow 12.0 sont disponibles ; paddleocr/paddlepaddle/pillow-heif absents. Environ 9 Go libres sur C: lors du contrôle. Ne pas déduire la compatibilité GPU ou Python des seuls noms ; tester les paquets exacts. Pas de reconnaissance faciale, géocodage ni export XMP à ce jalon.

La validation de qualité finale exige une vérité terrain privée et une revue humaine. Une réponse JSON valide et un test de fonctionnement ne constituent pas une preuve de précision OCR/vision ni de décodage HDR fidèle. Les photos du pilote ne seront envoyées qu'au service local explicitement vérifié.
