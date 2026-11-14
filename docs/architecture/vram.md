# Budget mémoire sur NVIDIA RTX 4070 12 Go

La VRAM est partagée avec Windows, le bureau, les contextes CUDA et les autres programmes. Les poids d'un modèle quantifié ne correspondent pas à l'empreinte mémoire totale : tenir compte du cache KV, des images, du contexte et des allocations de calcul.

Stratégie pilote : analyse **séquentielle**, pas de parallélisme vision + OCR GPU. Modèle candidat Qwen3-VL 8B quantifié sous Ollama (`qwen3-vl:8b`, version/digest épinglés avant test). Préparer une variante 4B si mémoire ou temps excessif. Faire l'OCR sur CPU initialement si cela simplifie la coexistence.

Mesurer pour chaque lot : VRAM avant/après, durée p50/p95 par photo, échecs OOM, consommation RAM et reprise sur interruption. Ne pas déclarer 8B « garanti » sur 12 Go sans mesure réelle ; même une taille de fichier de poids inférieure à 12 Go ne constitue pas une preuve.

Ne lancer ni le moteur facial ni les calculs vectoriels pendant les phases 1/2. Garder des images de test redimensionnées de manière déterministe et conserver le lien vers l'original par son hash.
