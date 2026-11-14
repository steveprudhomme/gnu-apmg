# Vue d'ensemble des modules à développer (aucun code applicatif ici)

```text
components/
  inventory/           # Découverte en lecture seule, hashing, EXIF
  vision/              # Description et objets via Ollama (local)
  ocr/                 # PaddleOCR local
  faces/               # Futur : identités opt-in
  geo/                 # Futur : référentiel local
  semantic/            # Futur : graphe de connaissances
  export/              # Futur : ExifTool, sidecars XMP
  orchestrator/        # Contrôle des étapes et reprises
```

Le dossier `components/` n'est intentionnellement pas encore créé : il ne contiendrait que des répertoires vides. Chaque composant futur aura un README, une CLI testable, un schéma d'entrée/sortie, une politique de licence et des tests indépendants.
