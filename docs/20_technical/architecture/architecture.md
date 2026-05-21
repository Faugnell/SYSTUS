# Architecture cible

S.Y.S.T.U.S est decoupe en modules simples afin de pouvoir tester chaque brique
independamment sur Raspberry Pi Zero.

## Flux principal

```text
Bouton ecoute
    -> capture audio I2S
    -> reconnaissance musicale
    -> normalisation metadonnees
    -> rendu e-ink
    -> historique visible dans l'interface web locale
```

## Modules prevus

- `audio_capture` : enregistre un extrait court depuis le micro ICS-43434.
- `recognition` : encapsule le moteur de reconnaissance choisi.
- `metadata` : nettoie et structure titre, artiste, album et pochette.
- `display` : prepare les vues compatibles e-ink.
- `web` : expose une interface locale de configuration et de diagnostic.
- `wifi_setup` : prepare le portail captif ou le faux DNS.
- `buttons` : mappe les boutons physiques vers les actions systeme.

## Principe d'evolution

Le prototype doit d'abord fonctionner avec des commandes manuelles et des
services simples. Les optimisations, le cache local, la carte MicroSD SPI et les
modes basse consommation seront ajoutes apres validation du flux principal.
