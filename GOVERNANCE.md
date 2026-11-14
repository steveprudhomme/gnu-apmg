# Gouvernance et décisions

## Principes

- Ouverture dès le premier jour ; aucune dépendance à un service propriétaire, ni donnée de photos personnelle dans l'historique Git.
- Décisions publiques, proportionnées au risque et à l'effort de maintenance d'un projet porté initialement par une personne.
- Dépendances entre **contrats**, jamais dépendances circulaires entre modules.
- Droit à la déconnexion des mainteneurs : aucune garantie de délai de réponse.

## Proposition / validation

Petits changements : Pull Request et revue. Architecture, ontologie, licence, export de données, politique de confidentialité : `docs/architecture/adr/` et discussion avant fusion. En l'absence d'équipe de revue, le mainteneur principal documente ses propres décisions et risques. Les modifications de sécurité peuvent être traitées de manière confidentielle avant divulgation.

## Droits d'accès

`main` protégée par PR, revue et checks requis dès que le dépôt est créé ; CODEOWNERS ensuite. Les clés de publication doivent demeurer hors Git. Pas de pouvoir permanent de relicenciation automatique : DCO plutôt que CLA.

## Branches / versions

Tronc principal `main`, branches courtes `feature/*` / `docs/*`, tags `vMAJOR.MINOR.PATCH` seulement pour le logiciel effectivement distribué. Le présent dépôt est un **blueprint**, sans version produit prétendument installable.
