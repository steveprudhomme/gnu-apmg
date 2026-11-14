# Géocodage 100 % local — module de phase 3

L’API publique Nominatim n’est pas compatible avec l’objectif de non-divulgation des coordonnées privées. Sa politique limite aussi l’usage de masse. Utiliser au début un référentiel OSM local pour ville/province/pays. Un Nominatim auto-hébergé, avec PostgreSQL/PostGIS et import de données, pourra être évalué ultérieurement pour les adresses fines. Installer cette infrastructure serait disproportionné au stade de 150 photos.

Le GPS EXIF indique une position estimée de prise de vue ; il ne décrit pas nécessairement les lieux visibles. Une adresse déduite du voisin le plus proche n’est pas une adresse civile certaine. Conserver incertitude, précision, source et date du jeu de données.

Références : https://operations.osmfoundation.org/policies/nominatim/ ; https://github.com/osm-search/Nominatim .
