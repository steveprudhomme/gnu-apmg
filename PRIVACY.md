# Confidentialité et données sensibles

- Traitement sur poste local ; toutes les connexions vers des modèles externes et vers des serveurs de géocodage publics sont **désactivées par conception**.
- Conservation des originaux sans modification pendant les phases 1/2 ; sortie de travail à l'extérieur du dépôt.
- Empreintes faciales, identités, GPS et adresse : données sensibles, stockage restreint et effacement possible ; jamais incluses aux logs ou au corpus public.
- Minimisation des données : ne conserver que le nécessaire ; consentement et droits des personnes photographiées à étudier selon la juridiction et l'usage.
- Modèles : distinguer l'utilisation de Qwen3-VL pour les scènes et l'utilisation d'un moteur facial spécialisé ; aucune inférence de caractéristiques sensibles.
- Export : n'inscrire les noms, positions précises et assertions que si l'utilisateur le demande ; masquer les métadonnées privées dans tout export public.
- Nominatim public : interdit pour les données privées et non conforme au mode 100 % local ; préparer un référentiel local OSM et un service local si nécessaire.

Ce document exprime une politique d'architecture, pas une certification réglementaire. Une analyse de protection des données pourra être requise avant usage sur les archives d'autrui.
