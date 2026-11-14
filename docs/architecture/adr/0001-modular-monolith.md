# ADR-0001 — Monolithe modulaire, contrats Unix

**Statut : proposé.** Contexte : un mainteneur solo doit pouvoir tester les traitements et les réutiliser sans administrer une constellation de microservices.

Décision : dépôt unique, modules au périmètre strict, CLI et contrats JSONL, orchestrateur unidirectionnel. Ollama tourne déjà comme processus distinct. Les modules futurs sont des plugins, non des services obligatoires.

Conséquences : installation simple et meilleure testabilité, risque de couplage si les contrats ne sont pas documentés. Migration possible vers processus séparés sans changer le format des observations.
