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
| P2A | Plan et environnement | Commit préalable, dépendances optionnelles isolées, espace disque contrôlé | Fait |
| P2B | Décodage HEIC et préparation | Pillow/pillow-heif ; image principale, orientation appliquée une fois, copie RGB réduite hors sources/Git sans EXIF/GPS ; ICC converti vers sRGB si disponible ; limites HDR/couleurs explicites | Implémenté, 10 HEIC vérifiés |
| P2C | Contrat des observations | Schéma JSON strict, provenance version/prompt/digest, statut suggested, confiance non calibrée null ; stockage privé append-only, pas de promotion humaine automatique | Implémenté, v1 suggested |
| P2D | Vision Ollama locale | Endpoint de boucle locale fixe, pas de redirection/proxy externe, aucun téléchargement implicite ; images réduites ; modèle existant ou choix confirmé ; réponse structurée bornée et validée | Fonctionnel, 1/3 essai HEIC refusé |
| P2E | OCR PaddleOCR CPU | Installation isolée selon wheels disponibles, modèles locaux explicites, pas de téléchargement durant analyse ; texte/boîtes et score brut distinct de confidence ; échec clair si indisponible | Fonctionnel sur CPU |
| P2F | Reprise et protections | Empreinte source avant/après préparation, paramètres de cache versionnés ou nouvelle sortie ; erreurs partielles visibles et aucun média privé publié | Protections testées, nouvelles sorties par run |
| P2G | Tests et petit pilote | Images synthétiques avec texte connu, tests unitaires sans IA et essais réels séparés ; quelques copies HEIC du pilote privé ; mémoire et temps observés ; qualité humaine encore à annoter | Essais techniques faits, qualité humaine à annoter |
| P2H | Scripts utilisateur et documentation | Scripts relançables, tutoriel illustré Phase 2, README/INSTALL/contrats/FAQ/manifestes mis à jour, commits et publication vérifiée | Fait pour ce jalon pré-alpha |

Constats préalables : Ollama 0.40.13 disponible, RTX 4070 12 Go détectée ; Qwen3-VL 8B absent, Qwen3.5 9B déjà présent. Python 3.13 et Pillow 12.0 sont disponibles ; paddleocr/paddlepaddle/pillow-heif absents. Environ 9 Go libres sur C: lors du contrôle. Ne pas déduire la compatibilité GPU ou Python des seuls noms ; tester les paquets exacts. Pas de reconnaissance faciale, géocodage ni export XMP à ce jalon.

La validation de qualité finale exige une vérité terrain privée et une revue humaine. Une réponse JSON valide et un test de fonctionnement ne constituent pas une preuve de précision OCR/vision ni de décodage HDR fidèle. Les photos du pilote ne seront envoyées qu'au service local explicitement vérifié.


### Reprise Phase 2 après arrêt et nettoyage — 15 novembre 2026

- Vérifier l'environnement Python déplacé sur D: et son lien local avant relance : imports Python 3.13.6 / Pillow 13.0.0 / PaddleOCR 3.7.0 réussis. Le code Phase 2 reste non publié à ce stade.
- Reprendre le téléchargement Qwen3-VL 8B explicitement choisi ; le cache partiel a été supprimé pendant le nettoyage, mais le composant complet déjà reçu est conservé.
- Valider d'abord une image synthétique à texte connu avec vision et OCR réels ; observer temps et mémoire, sauvegarder les détails uniquement dans l'état privé.
- Tester ensuite au plus trois dérivés HEIC déjà préparés, sans nouvelle recherche de photos ; vérifier intégrité, absence de métadonnées et validité des propositions.
- Ajouter les régressions nécessaires pour refus des modèles distants, sorties invalides, provenance et non-écrasement. Conserver la validation humaine comme porte de qualité non automatisable.
- Finaliser les scripts PowerShell et leur documentation illustrée, puis publier le code seulement après les tests locaux et contrôles de confidentialité ; suivre la CI.

Ce complément est commité avant la reprise du travail. Environ 18,5 Go libres sur C: au contrôle ; aucun autre nettoyage ni déplacement d'installation n'est prévu.


### Bilan Phase 2 pré-alpha — 15 novembre 2026

- Plans préalables `b64dd71` et `0417114`. Environnement isolé déplacé sur D: avec jonction conservant les chemins des scripts ; imports et exécution vérifiés. Installation globale Python inchangée.
- Qwen3-VL 8B téléchargé selon le choix utilisateur. Digest local : `9cf69da2b16d097f7def535917c4b55a95d6c7ee5700eb69ab86b01b3cfca487`. Service Ollama 0.40.13, uniquement boucle locale.
- Préparation : 10/10 copies HEIC décodées ; empreintes source inchangées, dérivés RGB sans métadonnées et grand côté <= 1 600 pixels. Pas de garantie de fidélité HDR ni de revue colorimétrique humaine.
- OCR : le texte attendu de la mire est retrouvé. Trois dérivés HEIC traités, 37 propositions au total. Essai synthétique réussi avec sockets Python bloquées. Désactivation oneDNN nécessaire sur PaddlePaddle 3.3.1 / Windows observé.
- Vision : mire synthétique réussie ; 2/3 dérivés HEIC produisent des observations structurées. Le troisième est refusé car le budget de 2 048 tokens est épuisé sans réponse finale. Ne pas annoncer une réussite complète du pilote de vision. Aucun JSONL d'observations créé pour ce cas.
- Mémoire GPU totale échantillonnée chaque seconde : pic observé de 8 693 MiB, incluant les autres usages GPU. Durées des deux essais privés acceptés : 30,25 et 16,43 secondes ; troisième essai refusé : 32,05 secondes. Pas de benchmark généralisable ni de taux de précision établi.
- Tests locaux : 29 exécutés, 27 réussis, 2 ignorés (permissions liens symboliques). Schéma présent dans la wheel construite ; aucune release publiée. Scripts PowerShell analysés ; préparation du script utilisateur exécutée sur la mire. Les commandes d'analyse sont testées séparément.
- Les données, descriptions, textes OCR, empreintes privées et images restent hors Git. Seuls ces nombres et les versions sont destinés au dépôt public.
- Étape suivante obligatoire : revue humaine privée et vérité terrain pour CER/WER, objets et hallucinations ; ensuite décider du budget/modèle pour les cas tronqués avant élargissement. Pas d'interface de validation, pas de recherche vectorielle ni d'export à ce jalon.

Publication Phase 2 : commit `e96cdd0`. [Contrôles GitHub Windows et Linux réussis](https://github.com/steveprudhomme/gnu-apmg/actions/runs/43691215711), incluant les tests légers de préparation Phase 2. Les modèles OCR/vision réels ne sont testés que localement, pas en CI. Les limites de qualité et le cas tronqué restent ouverts.


## Jalon T — taxonomie de photographies personnelles fondée sur des standards

OBJECTIVE : couvrir les situations de vie en réutilisant un vocabulaire éprouvé plutôt qu'en inventant une ontologie générale. GOAL : base thématique officielle, bilingue, traçable et exploitable localement. OWNER : mainteneur assisté de Codex.

| ID | Sous-étape avant travail | Critère de sortie | État |
| --- | --- | --- | --- |
| T1 | Vérifier sources et réutilisation | IPTC Media Topics officiel, licence/attribution, version et empreinte ; Getty AAT comme complément spécialisé | Fait |
| T2 | Importer la base officielle | Identifiants et hiérarchie d'origine préservés, FR/EN, source figée et conversion locale reproductible | Fait |
| T3 | Organiser la lecture personnelle | Guide par situations de vie et facettes ; distinguer thèmes, objets, activités, événements, lieux et personnes privées | Fait |
| T4 | Précision spécialisée | Examiner animaux/plantes/architecture/transports ; pas de mapping exactMatch inventé ni de fausse identification d'espèce | Fait |
| T5 | Contrôler et expliquer | Tests sur références et relations, tutoriel illustré, catalogue consultable ; aucun étiquetage automatique de photos ni géocodage à ce jalon | Fait |
| T6 | Mettre à jour et publier | ROADMAP/README/ontologie/NOTICE si nécessaire, commits après vérifications, publication et CI | Fait |

SUCCESS CRITERIA : termes officiels identifiables, provenance/version conservées, absence de cycles ou références cassées dans la hiérarchie exploitée, limites de couverture explicites. Les personnes, adresses et événements propres à la famille sont des entités privées, pas des ajouts au vocabulaire public. La liaison automatique des sorties de vision aux concepts et l'export IPTC/XMP restent des travaux ultérieurs. Les identifiants locaux éventuels ne seront pas présentés comme des termes IPTC/Getty.


### Bilan du jalon T — 15 novembre 2026

- Commit préalable `09c2ef5`. IPTC Media Topics version 2026-09-30 : 1 394 concepts, 1 059 actifs, 335 retirés, 17 sommets officiels conservés. Parmi les actifs, 37 n'ont pas de libellé français source : anglais de repli explicite.
- Snapshot multilingue original figé ; export FR/EN et SKOS générés hors ligne, identifiants/parents inchangés. HTTP officiel utilisé après échec HTTPS local, empreinte locale consignée, aucune signature d'éditeur revendiquée.
- Getty : sélection de 22 concepts d'animaux, plantes, paysages, bâtiments et véhicules, après exclusion d'homonymes. Fragment ouvert avec parents extérieurs ; pas de hiérarchie complète ni de statut de retrait Getty vérifié. Présentations françaises éditoriales séparées des libellés officiels.
- 17 collections éditoriales pour la photographie personnelle, sans réécriture de la hiérarchie IPTC. Guide couvrant situations de vie, facettes et règles de précision. Pas d'exactMatch automatique IPTC–Getty, pas d'identification d'espèce ou d'attribution aux photos.
- Livrables : catalogue HTML local filtrable, catalogues Markdown IPTC/Getty, guide personnel, JSON de consultation embarqués, export SKOS/Turtle et tutoriel illustré. Données CC BY 4.0 et ODC-By 1.0 attribuées séparément de la GPL du code.
- Contrôles : tests de hiérarchie, retraits, langues/identifiants, homonymes, parsing RDF réel et reconstruction déterministe ; HTML vérifié pour 1 394 lignes et 17 vues, JavaScript contrôlé syntaxiquement. Aucun test visuel dans un navigateur n'est revendiqué.
- Suite locale : 35 tests exécutés, 33 réussis, 2 ignorés pour permissions de liens symboliques. Aucun média ni donnée privée nécessaire à ce jalon.

Travaux suivants distincts : catalogue biologique plus détaillé, extension contrôlée des objets Getty, liaison des propositions IA aux concepts, interface de validation, géocodage et export IPTC/XMP. Ne pas déclarer ces fonctions déjà implémentées.

Publication du jalon T : commit `76552d3`, [contrôles GitHub Windows et Linux réussis](https://github.com/steveprudhomme/gnu-apmg/actions/runs/43694140453). Les snapshots externes sont préservés octet pour octet par les attributs Git ; les cinq empreintes des fichiers indexés ont été confrontées à la provenance avant publication.


## Jalon V — rapprochement et validation humaine des mots-clés

OBJECTIVE : transformer les observations existantes en propositions de concepts vérifiables, puis conserver les décisions humaines sans modifier les analyses ni les photos. GOAL : session de revue privée utilisable hors ligne, aucune relance IA. OWNER : mainteneur assisté de Codex.

| ID | Sous-étape avant implémentation | Critère de sortie | État |
| --- | --- | --- | --- |
| V1 | Contrats et protections | Commit préalable ; entrées JSONL validées et identités stables ; sorties privées hors sources/Git ; aucune approbation automatique | Fait |
| V2 | Candidats déterministes | Correspondances lexicales bornées, quelques alias explicites révisés, termes IPTC retirés exclus ; homonymes et absence de candidat visibles | Fait |
| V3 | Présentation humaine | Rapport HTML local privé : aperçu réduit si fourni, texte source, concepts/définitions/provenance ; accepter/corriger/rejeter avec recherche manuelle | Fait |
| V4 | Journal des décisions | Export JSON depuis navigateur puis import explicite ; identifiant de session, révision anti-écrasement, acteur déclaré, horodatage et historique append-only SQLite | Fait |
| V5 | Reprise et tests | Rejet des modifications d'identité, concepts inconnus/retirés, décisions contradictoires ou obsolètes ; transaction atomique, rejouabilité contrôlée ; tests synthétiques | Fait |
| V6 | Pilote privé existant | Construire une session depuis les analyses déjà présentes, aucune identité/personne/GPS publiée ; aucune décision humaine prise à la place de l'utilisateur | Fait |
| V7 | Documentation et livraison | Tutoriel illustré, README/INSTALL/contrats/ROADMAP à jour, scripts utilisateur, commits et contrôles GitHub | Fait |

Les descriptions et textes OCR sont du contexte de revue ; seules les observations d'objets déclenchent le rapprochement lexical automatique initial. Les thèmes sensibles restent en choix manuel. Une similarité lexicale n'est pas une probabilité et ne crée pas d'exactMatch entre vocabulaires. La validation humaine porte sur le lien photo–concept proposé, pas sur une réécriture du texte d'origine. Les résultats validés restent dans l'état privé ; aucun export dans les images ou sidecars à ce jalon. Le HTML n'héberge pas de serveur, ne charge aucun CDN et ne transmet aucun média ; le transfert des décisions passe par un fichier choisi explicitement par l'utilisateur.


### Bilan V — 15 novembre 2026

- Plan préalable `c1a5ba4`. Rapprochement lexical sans IA : libellés bornés, alias explicites, exclusion des retirés et branches sensibles, recherche manuelle du snapshot.
- Revue HTML privée avec aperçus vérifiés, définitions et provenance. Sélections multiples, correction et rejet ; aucune confirmation par défaut. Les modifications d'un brouillon confirmé exigent une nouvelle confirmation.
- Export JSON puis import explicite : transaction atomique, acteur déclaré, révision, empreinte du catalogue, historique append-only via l'application. Rejeu identique idempotent ; lots contradictoires/obsolètes et concepts inconnus/retirés refusés.
- Session réelle créée depuis deux analyses existantes : 47 observations, 15 objets, 3 avec candidats, 2 aperçus. Révision 0, zéro décision ; aucune acceptation au nom de l'utilisateur. Modèles non relancés.
- Session synthétique distincte : interactions testées en DOM simulé (sélection, invalidation, acceptation/rejet, recherche/correction/export), puis import réel du seul lot fictif via le script PowerShell. La session réelle est restée intacte.
- Navigateur de test indisponible au lancement ; aucune inspection visuelle réelle n'est revendiquée. jsdom est seulement un outil de test hors dépôt.
- Suite locale : 47 tests, 45 réussis, 2 ignorés pour permissions de liens symboliques. Scripts de création/import exécutés, modèle HTML embarqué et vérifié dans la wheel construite (aucune release publiée).
- Limites : pas d'export vers photos/XMP, pas de migration inter-catalogues, pas de reprise de brouillons non exportés après fermeture du navigateur, pas d'authentification ni d'inaltérabilité cryptographique de l'acteur/journal.

Publication du jalon V : commit `acca1b7`, [contrôles GitHub Windows et Linux réussis](https://github.com/steveprudhomme/gnu-apmg/actions/runs/43696176557). La page de revue réelle, ses aperçus, la base et les décisions restent hors Git ; zéro décision réelle enregistrée lors de la livraison.


## Jalon X — export XMP réversible sur copies

OBJECTIVE : rendre les mots-clés humainement validés portables sans écrire les originaux. GOAL : lot privé autonome comprenant copies inchangées, sidecars et journal d'annulation. OWNER : mainteneur assisté de Codex.

| ID | Sous-étape avant travail | Critère de sortie | État |
| --- | --- | --- | --- |
| X1 | Contrat et commit préalable | Décisions courantes accept/correct uniquement ; aucune description/OCR/note/GPS ajouté ; sorties hors sources/Git | Fait |
| X2 | Simulation privée | Plan lisible avec photos résolues par SHA-256, concepts et champs futurs ; aucune écriture source | Fait |
| X3 | Correspondances standards | dc:subject pour libellés ; lr:hierarchicalSubject pour navigation (extension Adobe), AboutCvTerm IPTC pour URI/schéma/nom ; pas de faux SubjectCode | Fait |
| X4 | Écriture sur copies | Nouveau lot exclusif, copies identiques, nom image.ext.xmp, XML valide ; préserver les champs d'un sidecar existant et sauvegarder ses octets ; refuser ambiguïtés/collisions | Fait |
| X5 | Vérification et annulation | Journal avec empreintes, source/révision/vocabulaire ; relecture réelle ExifTool, intégrité avant/après ; rollback seulement des sidecars de ce lot et refus si modifiés depuis | Fait |
| X6 | Tests et pilote HEIC | Tests synthétiques déduplication/fusion/XML/annulation ; copie des deux photos validées ; digiKam seulement si disponible, jamais prétendre à une validation GUI absente | Fait |
| X7 | Documentation et publication | Tutoriel illustré, scripts, README/INSTALL/contrats/ROADMAP ; aucune image, XMP ou décision privée dans Git ; commits puis CI | Fait |

Les huit décisions importées sont la source humaine ; elles concernent des liens photo–concept, pas les phrases du modèle. Le lot exporté peut être supprimé manuellement mais le rollback applicatif n'efface pas les copies de photos : il retire les sidecars neufs ou restaure les sidecars antérieurs dans ce lot privé. Aucune annulation sur les sources originales. Les lieux/GPS et identités ne font pas partie de cet export. Un sidecar peut ne pas être lu automatiquement par tous les logiciels : relecture ExifTool distincte du test digiKam. Les hiérarchies Getty incomplètes restent limitées au fragment connu, sans parents inventés.


### Bilan X — 15 novembre 2026

- Plan préalable `0c9b4be`, avant implémentation. Export limité aux derniers concepts acceptés/corrigés de la revue, regroupés par SHA-256 et sans doublon d'identifiant.
- XML : dc:subject, lr:hierarchicalSubject (extension Adobe) et IPTC AboutCvTerm/CvId/CvTermId/CvTermName. Pas de faux SubjectCode, pas de nouveaux GPS/noms/notes/OCR/descriptions.
- Plan privé puis lot nouveau : copies byte-identiques, image.ext.xmp, sauvegardes et journal. Un XML existant est préservé sémantiquement et sauvegardé exactement ; ambiguïtés, liens, DTD et conflits refusés. Zone de construction temporaire vérifiée puis renommée, aucun original écrit.
- Relecture réelle ExifTool 13.63 : deux copies HEIC et deux XMP ; 4 concepts pour une photo et 3 pour l'autre, libellés/hiérarchies/URI conformes au plan. Empreintes source/copie inchangées. Les fichiers privés restent hors Git.
- Annulation testée seulement sur synthétique : compagnon nouveau retiré ou ancien restauré octet pour octet, copies retenues, refus si empreinte modifiée, reprise après interruption. Le lot réel est conservé pour l'utilisateur.
- digiKam non trouvé dans le PATH et les deux emplacements courants vérifiés ; aucun test GUI ou garantie d'aller-retour digiKam revendiqué.
- Suite locale : 56 tests exécutés, 54 réussis, 2 ignorés (permissions liens symboliques). Les copies conservent leurs métadonnées intégrées et restent privées ; le journal n'est pas cryptographiquement inviolable.

Prochaine porte distincte : test manuel sur copies dans digiKam si installé, puis décision de convention d'export/de fusion avant toute écriture auprès des originaux. Ce jalon n'autorise pas une écriture intégrée dans les photos.

Publication X : commit `6da22a7`, [contrôles GitHub Windows et Linux réussis](https://github.com/steveprudhomme/gnu-apmg/actions/runs/43764456464). Les deux copies, XMP, sauvegardes éventuelles et journaux restent privés ; aucune écriture sur les originaux. Le test digiKam reste ouvert.
