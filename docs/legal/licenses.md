# Inventaire préliminaire des licences (à refaire à chaque verrouillage de version)

| Élément | Licence observée à la source officielle | Compatibilité / portée | Réserve |
|---|---|---|---|
| Code de ce projet | GPL-3.0-only | Licence choisie | Copyright des contributeurs |
| Python 3 récent | PSF License v2 | GPL-compatible (Python moderne) | Vérifier composants embarqués |
| Qwen/Qwen3-VL-8B-Instruct **officiel** | Apache-2.0 | GPLv3 compatible pour le code/modèle sous cette licence | Modèle quantifié exact, distribution et adaptateurs à auditer ; ne pas confondre avec variantes tierces |
| PaddleOCR | Apache-2.0 | GPLv3 compatible | Versions des poids, PaddlePaddle et transitives à vérifier individuellement |
| ExifTool (Phil Harvey) | Au choix, conditions de licence de Perl (Artistic ou GPL) | Utilisation comme outil CLI indépendant privilégiée | Vérifier les conditions précises si redistribution/embarquement |
| SQLite bibliothèque de base | Domaine public | Pas de restriction de licence à cet égard | Extensions tierces à auditer séparément |
| Données OpenStreetMap | ODbL 1.0 (base de données, **pas** licence logicielle) | Usage local possible avec obligations adaptées | Attribution et partage éventuel d'une base dérivée ; ne pas assimiler à « GPL compatible » |
| Nominatim code | Composants sous licences différentes : API/DB Python GPLv3+, configuration Lua Apache-2.0, autres fichiers GPLv2 selon dépôt | Service local à intégrer comme outil séparé | Audit par composant et tarball au moment du choix |
| Ollama | MIT pour le logiciel (modèles séparés) | Habituellement compatible GPLv3 | Poids et distributions distincts |

Références officielles :
- https://www.gnu.org/licenses/gpl-3.0.html
- https://www.gnu.org/licenses/license-list.html#apache2
- https://docs.python.org/3/license.html
- https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct
- https://github.com/PaddlePaddle/PaddleOCR/blob/main/LICENSE
- https://exiftool.org/
- https://github.com/exiftool/exiftool/blob/master/README
- https://www.sqlite.org/copyright.html
- https://www.openstreetmap.org/copyright
- https://github.com/osm-search/Nominatim
- https://operations.osmfoundation.org/policies/nominatim/

## Audit automatisable — limites juridiques

`REUSE`/SPDX vérifie nos notices de copyright ; `pip-licenses`, ScanCode Toolkit/ORT et CycloneDX peuvent aider à inventorier licences et composants. Un script génère `NOTICE` depuis `third_party/manifest.json` **pour le socle de conception seulement**. En release, remplacer ce manifeste statique par un SBOM CycloneDX généré depuis dépendances verrouillées, modèles (repo, révision, poids/digest) et binaires tiers.

Fail closed : licence `UNKNOWN`, famille de copyleft incompatible, poids sans preuve de provenance, texte de licence non livré ou obligation non satisfaite **bloquent la release** jusqu'à revue humaine. Aucun outil ne peut garantir seul une compatibilité juridique complète. Ajouter les licences tierces, notices et sources correspondantes quand elles sont redistribuées, et distinguer outils non embarqués des binaires inclus.
