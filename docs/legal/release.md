# Publication des archives sources canoniques

**Précondition :** Git `main` protégé, PR revue, tests et contrôles de secrets/NOTICE passés, licences et modèles audités, aucun fichier privé ni image dans l'historique, source correspondante disponible si binaires distribués. Fixer `vMAJOR.MINOR.PATCH`, créer un tag **annoté et signé** si possible (`git tag -s v0.1.0 -m 'Release v0.1.0'`), puis vérifier `git tag -v v0.1.0`.

Sur un environnement avec Git et GnuPG installés :

```sh
name=photosemantique-0.1.0
git archive --format=tar.gz --prefix="$name/" --output="$name.tar.gz" v0.1.0
git archive --format=zip --prefix="$name/" --output="$name.zip" v0.1.0
sha256sum "$name.tar.gz" "$name.zip" > "$name.sha256"
gpg --armor --detach-sign --output "$name.tar.gz.asc" "$name.tar.gz"
gpg --armor --detach-sign --output "$name.zip.asc" "$name.zip"
gpg --armor --detach-sign --output "$name.sha256.asc" "$name.sha256"
```

Windows : utiliser Git Bash ou environnement possédant ces outils ; `Get-FileHash -Algorithm SHA256` pour vérifier les checksums. Vérification indépendante : `sha256sum -c <nom>.sha256`, `gpg --verify <archive>.asc <archive>`. Publier clé publique, empreinte de clé vérifiée hors bande, changelog, SBOM, NOTICE, instructions de source correspondante et hash des archives.

MD5 / SHA-1 peuvent être produits **uniquement** pour l'interopérabilité historique si requis, mais ne suffisent pas pour l'intégrité sécuritaire. **SHA-256 et signature sont les contrôles obligatoires.** L'archive de ce blueprint n'est pas une release GPG signée.
