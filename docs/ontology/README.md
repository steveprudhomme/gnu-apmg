# Vocabulaire et ontologie — premier cadrage

SKOS organise une taxonomie bilingue évolutive : concepts `transport`, `transport aérien`, `avion`, `planeur`, avec `skos:prefLabel` FR/EN et des liens `skos:broader`/`skos:narrower`. Un concept stable conserve son URI même si son libellé change.

RDF/OWL sert aux liens entre photos, objets, lieux, événements et personnes, **après** avoir établi la provenance et la révocabilité. PROV-O relie assertion (`prov:Entity`), activité d'analyse (`prov:Activity`) et moteur/humain responsable (`prov:Agent`).

Propagation interimages : une immatriculation OCR validée sur photo A peut donner une **hypothèse** sur la photo B prise au même lieu et au même moment. Jamais copier la chaîne de A vers B comme « fait validé » sans critère d'identité ou revue. Toute hypothèse conserve l'identifiant des observations qui la justifient.

Attention : ne pas inventer d'URI institutionnelle. Les IRIs locales du vocabulaire pilote restent `urn:photosemantique:...` jusqu'à décision de namespace pérenne.
