# ADR-0002 — Pas de service externe pour des images privées

**Statut : proposé.** Toute photographie, tout visage, toute coordonnée GPS et tout texte OCR sont traités localement. Aucun géocodage externe ; la base OSM est locale si et quand la phase 3 la requiert. Les modèles sont acquis par choix conscient, avant l'analyse et sans téléversement de l'échantillon.

Conséquence : installation moins immédiate et occupation disque plus élevée, mais principe de confidentialité vérifiable en coupant le réseau pendant les tests.
