# TD Blockchain bitcoin

## Bip 39

Generer un entier de 128 bits

Hasher l'entier et récuperer les 4 premiers bits

Entropy : Entier + Checksum

Découper en 12 mots de 11 bits

Match avec la liste BIP 39

On a bien une seed phrase

## Bip 32

Importer une seed

Hasher pour retrouver la master private key et master chain code

Générer la master public key

Générer une clé enfant via dérivation
