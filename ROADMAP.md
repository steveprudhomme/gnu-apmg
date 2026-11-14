# GNU APMG — feuille de route

Nom complet : GNU Automatic Picture Metadata generator. Ancien nom : PhotoSémantique. Dépôt cible demandé : `steveprudhomme/gnu-apmg` ; sa création reste à vérifier.

État vérifié le 13 novembre 2026 : reprise documentaire, développement en attente des sources.

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
