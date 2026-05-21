# S.Y.S.T.U.S.

S.Y.S.T.U.S signifie **Sound-Yielded System for Tracking & User Sync**.

Le projet vise a prototyper un stand musical intelligent, au style cassette
futuriste, capable de reconnaitre une musique en cours de lecture puis
d'afficher les informations du morceau sur un ecran e-ink.

## Objectif prototype

- Capturer un extrait audio avec un micro MEMS I2S.
- Identifier le morceau via une solution open source de reconnaissance musicale.
- Recuperer les metadonnees utiles : titre, artiste, album, pochette si
  disponible.
- Afficher ces informations sur un ecran e-ink.
- Fournir une interface web locale en Wi-Fi pour la configuration et le suivi.
- Garder une architecture legere, modulaire et testable sur Raspberry Pi Zero.

## Structure du depot

```text
.
├── config/                 # Exemples de configuration applicative
├── docs/                   # Documentation projet, technique et ressources
├── scripts/                # Scripts d'installation, diagnostic, maintenance
├── src/                    # Code source Python de S.Y.S.T.U.S
├── systemd/                # Unites systemd pour Raspberry Pi
└── tests/                  # Tests automatises et notes de validation
```

Voir [docs/README.md](docs/README.md) pour le plan de documentation detaille.

## Modules logiciels prevus

- `audio_capture` : capture audio depuis le micro I2S.
- `recognition` : integration du service de reconnaissance musicale.
- `display` : rendu e-ink, pochette, metadonnees et egaliseur minimaliste.
- `web` : interface locale Flask ou FastAPI.
- `config` : chargement `.env`, YAML ou JSON.
- `buttons` : gestion des boutons physiques.

Le code n'est pas encore implemente : le depot est d'abord structure pour
accueillir proprement la documentation, les schemas, les choix techniques et le
futur code source.
