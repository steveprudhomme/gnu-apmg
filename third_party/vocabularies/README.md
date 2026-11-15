# Sources publiques des vocabulaires

Ces fichiers sont des données de référence, pas des photos ni des observations privées. Ils conservent leurs licences propres ; la GPL du code GNU APMG ne les remplace pas.

- **IPTC Media Topics** : Copyright IPTC, International Press Telecommunications Council. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Source : [serveur officiel](https://cv.iptc.org/newscodes/mediatopic/). Version annoncée par les données : 30 septembre 2026. Le JSON multilingue original est conservé. Le serveur HTTPS a fermé les connexions locales ; l'endpoint HTTP officiel a été utilisé, puis son contenu figé par SHA-256. Cette empreinte locale n'est pas une signature de l'éditeur.
- **Getty Art & Architecture Thesaurus** : Contains information from the J. Paul Getty Trust, Getty Research Institute, Art & Architecture Thesaurus, which is made available under the ODC Attribution License. [ODC-By 1.0](https://opendatacommons.org/licenses/by/1-0/), [conditions et citation Getty](https://www.getty.edu/research-conservation/tools-databases/vocabularies/data-services/). Requêtes SPARQL et réponses de sélection conservées ; aucune prétention d'exhaustivité.

`provenance.json` donne URL, licence, date de récupération et empreinte SHA-256 de chaque source. Les réponses incomplètes ou non valides ont été rejetées avant import.

Transformations GNU APMG : sélection des langues FR/EN pour IPTC, conversion JSON/SKOS et présentations Markdown/HTML ; sous-ensemble d'objets Getty choisi après examen des homonymes. Les noms français de présentation Getty sont des traductions éditoriales séparées, pas des libellés préférés officiels. Aucune équivalence IPTC–Getty n'est inventée.

Reconstruction hors ligne : `python scripts/build_taxonomy.py`. Vérification : `python scripts/build_taxonomy.py --check`. Une mise à jour des fichiers sources exige une revue de leur licence, date, contenu et empreinte ; ne pas remplacer silencieusement le snapshot.
