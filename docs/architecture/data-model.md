# Trois niveaux de persistance

| Niveau | Nature | Ce qu'on y met | Quand |
|---|---|---|---|
| 1 — fichier original | EXIF/IPTC/XMP intégrés, lorsque le format le permet | Valeurs d'origine, puis **uniquement** champs explicitement confirmés | Phases 1/2 : lecture seule ; écriture en phase ultérieure sur copies testées |
| 2 — compagnon `.xmp` | Métadonnées portables indépendantes | Description, mots-clés, personnes consenties, lieux, champs IPTC reconnus | Export ultérieur et après validation |
| 3 — SQLite + index vectoriel | Données locales structurées et historique | Observations, bbox OCR, empreintes, graphes, versions, sources, confiance calibrée, relations | Phases 1/2 : manifeste et observations ; extension sémantique ultérieure |

## Schéma relationnel cible (spécification, pas migration)

`assets(id, sha256, mime, width, height)`, `file_instances(id, asset_id, path_local, stat)`, `exif_facts(id, asset_id, tag, raw_value)`, `observations(id, asset_id, kind, value, bbox, source_id, status, confidence, supersedes_id)`, `sources(id, software, version, digest, parameters)`, `identities(id, label_local, consent_status)`, `entities(id, uri, type)`, `relations(id, subject, predicate, object, provenance_id)`, `events(id, start, end, place_id)`, `validation_log(id, observation_id, action, actor_local, timestamp)`, `embedding_index(asset_id, model_digest, vector)`.

Chaque relation doit être rétractable et sourcée. Les vecteurs de visages sont des données biométriques ; chiffrement du stockage et permission explicite à prévoir.

## Correspondances standards (cibles, vérifier au test d'interopérabilité)

| Concept | IPTC/XMP cible | SQLite |
|---|---|---|
| Description | `dc:description` | `observations(kind='description')` |
| Mots-clés | `dc:subject` et éventuellement IPTC `SubjectCode` | `entities` et relations |
| Personnes représentées | `Iptc4xmpExt:PersonInImage` / détails selon outil | `identities` + observations validées |
| Lieu de prise de vue | `Iptc4xmpExt:LocationCreated` et GPS EXIF d'origine | `exif_facts` + géocodage dérivé |
| Lieu visible dans la photo | `Iptc4xmpExt:LocationShown` | `observations` avec provenance |
| OCR intégral + positions | Extension XMP propriétaire **optionnelle** (à documenter) ; ne pas surcharger les mots-clés | `observations` (texte + bbox + langue) |
| Inference et modèle | Aucun champ IPTC standard universel imposé | `sources`, `observations`, `validation_log` et export RDF PROV-O |

Les tags exacts pris en charge et la sérialisation sidecar doivent être testés avec les versions installées d'ExifTool et digiKam. Ne jamais faire croire qu'un champ personnalisé sera interopérable partout.


## Tables réellement créées dans la migration Phase 1

Le diagramme de la base initiale est disponible dans le [tutoriel illustré](../tutorial/phase-1.md). Il ne faut pas confondre le schéma **cible** ci-dessus avec la migration **implémentée**.

| Table implantée | Clé | Usage |
|---|---|---|
| `schema_migrations` | `version` | Version de migration appliquée |
| `assets` | `sha256` | Un contenu de fichier |
| `file_locations` | `path_local` | Plusieurs chemins possibles pour un contenu |
| `scans` | `scan_id` | Historique des traitements |
| `scan_items` | (`scan_id`, `path_local`) | État/erreur pour chaque fichier de chaque scan |
| `source_metadata` | (`asset_sha256`, `tag`) | Tags ExifTool JSON conservés, groupés et versionnés |

**Non implémentés :** vecteurs, ontologie RDF/OWL, validations humaines, régions OCR, personnes, lieux résolus, sidecars XMP, export/rollback. Le modèle documentaire à trois niveaux demeure une cible ; **seul le niveau SQLite existe pour les observations de Phase 1**.
