# Génération du fichier NOTICE

Le manifeste `third_party/manifest.json` renseigne provisoirement les technologies étudiées et si elles sont incluses ou non. `python scripts/generate_notice.py` reconstruit `NOTICE` de façon déterministe, `--check` garantit qu'il n'est pas obsolète. **Ce n'est pas encore une détection automatique des dépendances installées.** À la première release exécutable, intégrer ScanCode/ORT + CycloneDX, verrouiller les versions et interdire les licences inconnues.
