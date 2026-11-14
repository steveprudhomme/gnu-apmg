# Politique de sécurité

Pré-alpha sans déploiement disponible. Par défaut : pas de télémétrie, pas d'API cloud, aucun téléversement photo, aucun port exposé à l'extérieur, aucune authentification distante, aucun modèle téléchargé au lancement sans consentement explicite.

Ne publiez pas de signalement contenant des photos, des visages, des coordonnées, des empreintes faciales ou des secrets dans GitHub Issues. Lors de l'ouverture du dépôt, activer GitHub Private Vulnerability Reporting et publier le canal vérifié ; jusque-là, suspendre les rapports privés plutôt que demander des informations sensibles dans un canal public.

Mesures planifiées : analyse de secrets sur PR et historique, contrôles de dépendances et hashes, détection d'archives suspectes, chemins canonisés, extraction EXIF isolée, limites de taille, lecture seule par défaut, contrôle d'accès aux embeddings, interdiction de logging de données biométriques, sauvegardes chiffrées, suppression vérifiable des données dérivées.

Incident d'exemple **hypothétique** : une photo de démonstration anodine conserve des coordonnées GPS EXIF de domicile. Une fois poussée sur un dépôt public, la suppression du dernier commit est insuffisante : forks et caches peuvent exister. La règle est de n'ajouter que des données synthétiques et de vérifier **avant** le premier commit.
