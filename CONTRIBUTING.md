# Contribuer à GNU APMG

Bienvenue aux contributions en **développement**, **documentation**, **traduction FR/EN** et **tests**. Communauté bienveillante, bénévolat durable, vie privée respectée.

## En cinq gestes : Goal / Produce / Submit / Wait / Repeat

1. **Goal** : trouver une tâche étiquetée `good first issue` ou `bite-size`, décrire le résultat attendu et vérifier s'il existe déjà une discussion.
2. **Produce** : préparer une petite modification locale accompagnée d'un test ou d'une justification ; ne jamais introduire de vraies photos, visages, EXIF GPS, secrets ou modèles propriétaires.
3. **Submit** : ouvrir une Pull Request vers `main` avec objectif, modifications, tests et impact sur les données personnelles ; signer les commits ou ajouter le `Signed-off-by` DCO.
4. **Wait** : laisser le temps aux mainteneurs bénévoles de faire la revue ; suivre le retour de la CI et répondre courtoisement.
5. **Repeat** : corriger ou poursuivre sur une autre petite contribution, sans pression.

**Idées de petites tâches** : test sur chemins Unicode et longues arborescences Windows ; documentation des erreurs EXIF ; traduction des étiquettes SKOS ; validation d'un exemple purement synthétique ; revue du schéma `observation`.

## Stratégie de contribution et droit d'auteur

Nous retenons le **Developer Certificate of Origin (DCO 1.1)** plutôt qu'un CLA. La signature de contribution atteste notamment que son auteur a le droit de soumettre le travail sous la licence du projet : `git commit -s`. Le DCO ne transfère pas le copyright, et ne donne **pas** à lui seul la faculté de passer plus tard sous une licence différente. Un changement de licence global peut exiger l'accord de tous les ayants droit ou une réécriture licite.

Pas de contribution dérivée de code ou de poids de modèles dont la licence est inconnue. Inclure les notices et la provenance de tout matériau tiers. Si un contributeur souhaite rester anonyme publiquement, utiliser une identité de contribution autorisée et demander conseil avant de partager des données personnelles.

## Revue et entrée sur `main`

Tous les changements non triviaux passent par PR. Les mainteneurs vérifient tests, licences, confidentialité et documentation. La CI est une condition nécessaire mais non suffisante ; aucune fusion automatique sur la seule base d'un statut vert.
