# Contrat préliminaire : export

**Statut : export de mots-clés implémenté sur copies privées.** `photosemantique.xmp_export` prépare un plan, résout les contenus par SHA-256 et écrit dc:subject, lr:hierarchicalSubject et IPTC AboutCvTerm dans des sidecars image.ext.xmp. Aucun original ni décision modifié. Fusion conservatrice d'un compagnon existant, sauvegarde et journal d'annulation avec reprise après interruption.

Relecture réelle ExifTool 13.63 vérifiée sur deux copies HEIC ; test GUI digiKam non effectué. Pas d'export des descriptions/OCR/noms/GPS, pas d'écriture intégrée dans les photos. Voir le [tutoriel](../../docs/tutorial/export-xmp.md).

- Entrée prévue : Métadonnées autorisées et confirmées.
- Sortie prévue : Sidecars et copies explicitement demandées.
- Aucun appel réseau externe, aucune donnée du pilote dans Git.
- Les schémas sont documentés dans `schemas/` et `docs/architecture/contracts.md`.
- Contrats de CLI et tests indépendants à rédiger avant implémentation.
