# Taxonomie des photographies personnelles — GNU APMG

**Mise à jour jalon V :** la [revue privée des mots-clés](../tutorial/revue-mots-cles.md) propose des correspondances lexicales et conserve les décisions humaines. Les limites d'interface décrites plus bas sont historiques ; reconnaissance fine, attribution sans contrôle humain et export restent non livrés.

## Choix : référentiels éprouvés et facettes complémentaires

Version de travail 1.0, 15 novembre 2026. Cette base réutilise **IPTC Media Topics** pour les thèmes, événements et contextes ; **Getty AAT** pour une première sélection d'objets/nature ; **SKOS** pour les identifiants, libellés et relations. Elle ne prétend pas qu'une taxonomie de presse remplace une classification exhaustive de tous les objets ou de toutes les espèces.

**Ouvrir [le catalogue local filtrable](catalogue.html)** dans un navigateur : recherche FR/EN, 17 vues de vie personnelle, parents et liens officiels. Les vues sont une organisation éditoriale GNU APMG, pas une nouvelle hiérarchie officielle. Elles peuvent se recouper. Le fichier reste utilisable sans réseau ; les liens externes s'ouvrent uniquement à la demande.

- [Tous les concepts IPTC](IPTC-CATALOGUE.md) : 1 394 enregistrements, **1 059 actifs**, 335 retirés pour historique.
- [Sélection Getty AAT](GETTY-SELECTION.md) : 22 concepts vérifiés, non exhaustifs, parents extérieurs conservés.
- [Export SKOS bilingue IPTC](iptc-mediatopics.fr-en.ttl).
- [Sources, attributions et transformations](../../third_party/vocabularies/README.md).

Les 37 concepts actifs sans libellé français dans la source sont affichés en anglais, sans traduction inventée présentée comme officielle. Les traductions françaises d'affichage Getty sont propres à GNU APMG et explicitement séparées des libellés source.

## Ce qu'une photo peut recevoir

Une seule photo peut associer plusieurs angles de description, sans tout mélanger dans un arbre unique :

| Facette | Ce qu'elle exprime | Exemple et règle |
| --- | --- | --- |
| Sujets visibles | Objets, êtres vivants, constructions, paysages | Oiseau, arbre, bâtiment, avion ; rester au niveau identifiable |
| Activité | Action effectivement visible ou contexte confirmé | Cuisiner, jardiner, jouer, marcher, travailler ; ne pas confondre instrument et pratique |
| Événement et situation | Thème ou événement confirmé | Mariage, anniversaire, diplôme, voyage ; un gâteau ne prouve pas un anniversaire |
| Lieu | Prise de vue et lieu représenté, séparément | Ville/province/pays et coordonnées privés ; module géographique encore à développer |
| Personnes et relations | Identités et rôles familiaux confirmés | Identifiant local, prénom, parenté ; jamais publier les noms dans ce vocabulaire |
| Temps et étapes de vie | Date source, période et contexte humain | Naissance, scolarité, retraite ; pas de date précise inventée depuis l'image |
| Forme de prise de vue | Façon de photographier | Portrait, groupe, autoportrait, macro, panorama, aérien, sous-marin, nuit ; facette descriptive à développer séparément |
| Rôle documentaire | Pourquoi l'image est conservée | Souvenir, œuvre, archive numérisée, document, constat, inventaire, capture d'écran ; ne pas confondre sujet et format HEIC/JPEG |

Les quatre dernières facettes ne sont pas déjà des listes de concepts importées dans ce jalon. Elles constituent le modèle de description et les points d'extension ; leurs entités privées ne doivent pas entrer dans la taxonomie publique.

## Vues couvrant les situations de vie

Chaque vue donne accès aux concepts actifs des branches officielles indiquées, y compris leurs descendants. Les intitulés de vues et exemples sont éditoriaux ; les liens pointent vers les concepts IPTC originaux.

### Famille, enfants et étapes de vie

Naissance, grossesse, anniversaires, mariage, départ à la retraite et commémorations : contexte à confirmer, jamais déduit de la seule apparence.

Branches de référence : [Famille](http://cv.iptc.org/newscodes/mediatopic/20000780), [Cérémonie](http://cv.iptc.org/newscodes/mediatopic/20000501), [Anniversaire (jour de naissance)](http://cv.iptc.org/newscodes/mediatopic/20001238), [Anniversaire](http://cv.iptc.org/newscodes/mediatopic/20001237).

### École, études et apprentissage

Rentrée, classe, activités scolaires, remise de diplôme et apprentissages.

Branches de référence : [Éducation](http://cv.iptc.org/newscodes/mediatopic/05000000), [Remise de diplôme](http://cv.iptc.org/newscodes/mediatopic/20001234).

### Travail, métiers et bénévolat

Vie professionnelle ; distinguer objet visible, métier confirmé et thème social.

Branches de référence : [Social](http://cv.iptc.org/newscodes/mediatopic/09000000).

### Maison, décoration et jardin

Habitat, rénovation, aménagement et jardinage ; pas une classification des types de bâtiments.

Branches de référence : [Maison et décoration](http://cv.iptc.org/newscodes/mediatopic/20000570), [Travaux de rénovation](http://cv.iptc.org/newscodes/mediatopic/20001255), [Jardinage](http://cv.iptc.org/newscodes/mediatopic/20001257).

### Repas, cuisine et découvertes culinaires

Repas familiaux, cuisine, pâtisserie, dégustation et gastronomie ; ne pas inférer un régime médical.

Branches de référence : [Gastronomie](http://cv.iptc.org/newscodes/mediatopic/20000568), [Cuisine (loisir)](http://cv.iptc.org/newscodes/mediatopic/20001253).

### Voyages, vacances et sorties

Voyages et tourisme ; ville et pays restent des champs géographiques distincts.

Branches de référence : [Voyages](http://cv.iptc.org/newscodes/mediatopic/20000563).

### Animaux, plantes et nature

Nature et écosystèmes ; identifications d’espèces à confirmer dans un référentiel taxonomique spécialisé.

Branches de référence : [Nature](http://cv.iptc.org/newscodes/mediatopic/20000441).

### Sports, activités physiques et compétitions

Distinguer pratique, compétition, résultat, équipement et simple présence à un événement.

Branches de référence : [Sport](http://cv.iptc.org/newscodes/mediatopic/15000000).

### Loisirs, jeux, collections et artisanat

Loisirs et créations ; les types d’objets nécessitent parfois un vocabulaire complémentaire.

Branches de référence : [Passe-temps](http://cv.iptc.org/newscodes/mediatopic/20000550), [Artisanat](http://cv.iptc.org/newscodes/mediatopic/20001160), [Jeux pour enfants](http://cv.iptc.org/newscodes/mediatopic/20000543).

### Arts, musique, spectacles et patrimoine

Concerts, théâtre, danse, musée, patrimoine et architecture ; sujet artistique distinct de l’identité des personnes.

Branches de référence : [Arts, culture, divertissement et médias](http://cv.iptc.org/newscodes/mediatopic/01000000).

### Sciences, astronomie et technologie

Observations du ciel, musées scientifiques, expériences et appareils ; types d’objets à préciser séparément.

Branches de référence : [Science et technologie](http://cv.iptc.org/newscodes/mediatopic/13000000).

### Fêtes, cérémonies et souvenirs

Anniversaire, mariage, diplôme, fête et commémoration ; l’événement familial précis est une entité privée.

Branches de référence : [Cérémonie](http://cv.iptc.org/newscodes/mediatopic/20000501), [Anniversaire](http://cv.iptc.org/newscodes/mediatopic/20001237), [Anniversaire (jour de naissance)](http://cv.iptc.org/newscodes/mediatopic/20001238), [Festival](http://cv.iptc.org/newscodes/mediatopic/20001181).

### Spiritualité, traditions et rites

Thèmes à attribuer volontairement ; voir un bâtiment religieux ne prouve jamais la croyance des personnes.

Branches de référence : [Religion et croyance](http://cv.iptc.org/newscodes/mediatopic/12000000).

### Santé, soins et étapes sensibles

Attribution manuelle privilégiée ; ne pas diagnostiquer une maladie ni déduire une situation intime depuis une photo.

Branches de référence : [Santé](http://cv.iptc.org/newscodes/mediatopic/07000000).

### Accidents, incidents et documents de constat

Souvenirs d’incident et constats ; conserver les détails privés localement.

Branches de référence : [Désastres et accidents](http://cv.iptc.org/newscodes/mediatopic/03000000).

### Déplacements et transports

Thèmes de transport ; le secteur économique du transport n’est pas synonyme d’un avion ou d’un véhicule visible.

Branches de référence : [Transports](http://cv.iptc.org/newscodes/mediatopic/20000337).

### Météo, saisons et phénomènes naturels

Phénomènes visibles et nature ; saison et date ne doivent pas être déduites avec certitude de l’image seule.

Branches de référence : [Météo](http://cv.iptc.org/newscodes/mediatopic/17000000), [Nature](http://cv.iptc.org/newscodes/mediatopic/20000441).

## Cas pratiques et combinaisons

| Photo personnelle | Description à construire | Ce qu'il faut éviter |
| --- | --- | --- |
| Naissance, maternité, première rencontre | Contexte confirmé + personnes privées + date | Diagnostiquer une situation médicale ou identifier les liens familiaux par apparence |
| Premiers pas, jeux, sortie familiale | Activité + contexte familial confirmé + lieu | Attribuer un âge exact ou une parenté sans donnée fiable |
| Anniversaire et fête de famille | Anniversaire confirmé + personnes + objets visibles | Déduire systématiquement l'occasion d'un gâteau |
| Mariage, union, célébration | Cérémonie de mariage si confirmée + lieu + participants privés | Confondre cérémonie et statut matrimonial durable |
| Rentrée, diplôme, spectacle scolaire | Thème éducatif/cérémonie + activité + groupe privé | Déduire établissement ou identité d'un enfant sans confirmation |
| Travail, artisan, chantier, commerce | Action + objets/outils + métier confirmé | Déduire profession ou employeur de la seule présence sur les lieux |
| Maison, déménagement, rénovation | Contexte d'habitat/travaux + types d'objets/bâtiments | Publier une adresse privée, ou confondre chantier et bâtiment achevé |
| Jardin, balcon fleuri, potager | Jardinage + plante à précision vérifiée + lieu | Inventer une espèce à partir d'une silhouette incertaine |
| Chien, chat, animal de compagnie | Type d'animal + activité + identité locale éventuelle | Confondre race, espèce et nom propre de l'animal |
| Oiseau sauvage, insecte, faune | Groupe reconnaissable, puis taxon vérifié si possible | Transformer une proposition visuelle d'espèce en fait |
| Voyage, excursion, camping, randonnée | Activité/contexte + sujets visibles + lieux séparés | Déduire la ville d'un paysage générique |
| Plage, montagne, rivière, forêt | Type de paysage/sujet + activité éventuelle | Fusionner paysage naturel, représentation artistique et motif décoratif |
| Repas, fête culinaire, recette, restaurant | Gastronomie/cuisine + aliments/objets visibles | Inférer un régime médical, une origine ou une allergie |
| Sport, entraînement, match, médaille | Discipline et pratique/compétition confirmées + équipement | Déduire résultat, club ou performance de la tenue seule |
| Concert, musique à la maison, danse | Événement ou activité + instrument/objet | Confondre instrument visible et musicien identifié |
| Musée, monument, église, œuvre | Sujet architectural/artistique + visite + lieu | Attribuer la croyance des personnes à partir du bâtiment |
| Avion, planeur, train, bateau, automobile | Type d'objet standard + déplacement/loisir/événement confirmé | Faire de « transport aérien » économique le synonyme exact de « planeur » |
| Soleil couchant, neige, pluie, orage | Phénomène visible + lieu/date fiables | Inventer une saison, une catastrophe ou un phénomène précis |
| Lune, ciel étoilé, observation scientifique | Astronomie + objet identifié à partir de preuves | Nommer automatiquement une constellation ou une planète incertaine |
| Soins, convalescence, visite à un proche | Contexte volontairement renseigné + date/personnes privées | Déduire diagnostic, handicap ou autre caractéristique sensible |
| Funérailles, tombe, commémoration | Objet/lieu + événement confirmé | Déduire décès d'une personne précise sans contexte fiable |
| Accident, dégât, constat d'assurance | Sujet et rôle documentaire + date/lieu privés | Transformer un constat visuel en conclusion juridique ou technique |
| Photo ancienne, album, généalogie | Objet photographié + caractère de reproduction + période connue | Confondre date de numérisation et date de prise de vue ancienne |
| Facture, billet, lettre, dessin, capture d'écran | Type de document/rôle + sujet pertinent | Publier le texte OCR, des coordonnées ou des identifiants personnels |
| Hobby, collection, jeu, fabrication | Activité + objet collectionné/fabriqué + contexte | Forcer l'objet dans un thème de presse sans rapport |

Ces cas servent de guide de couverture, pas de règles de reconnaissance automatique. Certains objets précis restent à ajouter depuis un référentiel spécialisé après contrôle du sens et de la licence.

## Règles de précision

1. **Identifiant avant libellé** : le mot français « Mariage » désigne deux concepts IPTC distincts (institution et cérémonie). Ils ne sont pas fusionnés.
2. **Définition avant correspondance** : un mot identique ne suffit pas à créer un exactMatch entre vocabulaires.
3. **Granularité prudente** : animal → oiseau est une précision possible ; canard puis espèce ne sont ajoutés que si les preuves le permettent. La sélection Getty n'est pas une taxonomie biologique exhaustive. Une version précise d'un référentiel GBIF/Catalogue of Life reste à sélectionner pour les taxons.
4. **Plusieurs concepts par photo** : on peut associer un thème de jardinage, une plante et un bâtiment, sans choisir une catégorie unique exclusive.
5. **Statut séparé du concept** : une annotation suggested n'est pas validée parce que son identifiant appartient à un standard.
6. **Retraits conservés** : ne pas supprimer l'histoire ni réutiliser un identifiant retiré pour un autre sens ; proposer seulement les termes actifs en usage courant.
7. **Données privées séparées** : noms, parenté, événements propres à la famille, adresses et coordonnées restent des entités locales.
8. **Pas d'inférence sensible automatique** : santé, croyance, orientation sexuelle, origine et situations intimes exigent un contexte volontaire et une validation adaptée.

## Ce qui est livré et ce qui reste à faire

Livré : vocabulaire local figé, sources/licences/empreintes, vues éditoriales, recherche FR/EN, export SKOS et catalogue HTML consultable. Aucun média privé n'a été nécessaire.

Non livré : attribution automatique des concepts aux photos, interface de validation d'annotations, géocodage, catalogue complet des espèces, tous les objets Getty, export de mots-clés dans les images. Ces étapes devront suivre leur propre plan et leurs tests. Le vocabulaire actuel n'est pas présenté comme exhaustif de toutes les situations humaines.
