# Vocabulaire contrôlé — GNU APMG

Le cadrage initial ci-dessous est désormais complété par un import réel de référentiels.

- [Guide des photographies personnelles](TAXONOMIE-PERSONNELLE.md) : facettes, situations de vie et règles de précision.
- [Catalogue HTML hors ligne](catalogue.html) : recherche FR/EN, 17 vues éditoriales, parents et identifiants officiels.
- [Catalogue IPTC complet](IPTC-CATALOGUE.md) : actifs et retirés séparés.
- [Complément Getty AAT](GETTY-SELECTION.md) : objets et nature, homonymes exclus.
- [IPTC en SKOS/Turtle](iptc-mediatopics.fr-en.ttl) et JSON embarqués dans `photosemantique/taxonomies/`.
- [Sources et licences propres aux données](../../third_party/vocabularies/README.md).

Version IPTC du 30 septembre 2026 : 1 394 concepts, dont 1 059 actifs, 335 retirés ; 37 actifs sans traduction française dans la source affichent l’anglais. Getty : 22 concepts sélectionnés, pas le thesaurus complet ; traductions françaises de présentation GNU APMG séparées des libellés officiels.

SKOS sert de modèle de représentation ; ce n’est pas une liste universelle de tous les sujets. La hiérarchie IPTC originale et ses identifiants sont conservés. Les vues « vie personnelle » sont des collections de consultation locales, pas de nouveaux parents SKOS. Les liens entre IPTC et Getty ne sont pas déclarés exactMatch.

Le fichier historique `transport.ttl` reste un exemple local de conception, non une extension normative intégrée à la nouvelle base. Aucun de ses URNs n’est présenté comme un identifiant IPTC ou Getty.

Reconstruction : `python scripts/build_taxonomy.py`, contrôle `--check`. Consultation : `python -m photosemantique.taxonomy mariage` ou `python -m photosemantique.taxonomy planeur --source getty`. Aucun de ces appels ne lit de photos, ne contacte un serveur ou n’attribue des mots-clés.

Les personnes, événements familiaux, adresses et coordonnées sont des entités privées distinctes. Le graphe RDF/OWL de relations, PROV-O complet, la correspondance automatique des observations aux concepts, la validation humaine et l’export XMP restent à implémenter.
