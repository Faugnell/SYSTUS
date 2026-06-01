# Cahier des charges - S.Y.S.T.U.S.

## 1. Presentation du projet

S.Y.S.T.U.S signifie **Sound-Yielded System for Tracking & User Sync**.

Le projet consiste a concevoir un stand musical intelligent, au style cassette
futuriste, capable de reconnaitre une musique en cours de lecture, puis
d'afficher les informations principales du morceau sur un ecran e-ink.

Le prototype doit rester accessible a un public maker : cout raisonnable,
composants disponibles, documentation claire, architecture evolutive et
possibilite de le reproduire ou de le modifier.

## 2. Contexte

La reconnaissance musicale est souvent associee a des applications mobiles et a
des services fermes. S.Y.S.T.U.S cherche a explorer une alternative ouverte,
locale autant que possible, integree dans un objet physique autonome.

Le prototype s'appuie sur un Raspberry Pi Zero ou Pi Zero W, un microphone MEMS
I2S, un ecran e-ink, des boutons physiques et une interface web locale accessible
en Wi-Fi.

## 3. Besoin

L'utilisateur doit pouvoir poser l'objet dans un environnement ou de la musique
est jouee, lancer une ecoute depuis un bouton physique, puis obtenir rapidement
les informations du morceau detecte.

En cas d'absence de reconnaissance, l'objet doit afficher une information claire
ou une visualisation minimaliste, par exemple un egaliseur ou un etat d'attente.

## 4. Objectifs

### Objectif principal

Realiser un prototype fonctionnel capable de capturer un extrait audio, de tenter
une reconnaissance musicale et d'afficher le resultat sur un ecran e-ink.

### Objectifs secondaires

- Proposer une interface web locale pour consulter l'etat du systeme et modifier
  certains reglages.
- Permettre une configuration Wi-Fi simple, idealement via portail captif ou
  faux DNS.
- Integrer des boutons physiques pour les actions principales.
- Documenter l'architecture, le montage, les tests et les choix techniques.
- Prevoir une structure logicielle modulaire pour faciliter les evolutions.

## 5. Perimetre du prototype

### Inclus

- Capture audio courte depuis un microphone I2S.
- Integration d'un service ou moteur de reconnaissance musicale open source.
- Recuperation des metadonnees disponibles : titre, artiste, album, pochette.
- Affichage e-ink du morceau reconnu ou d'un etat alternatif.
- Interface web locale minimale.
- Configuration par fichiers simples.
- Documentation technique et projet.

### Hors perimetre initial

- Production industrielle du boitier.
- Application mobile native.
- Reconnaissance 100 % locale garantie.
- Synchronisation multi-utilisateur avancee.
- Optimisation poussee de l'autonomie.
- Stockage massif d'historique musical.

## 6. Utilisateurs cibles

- Maker souhaitant reproduire ou modifier le prototype.
- Etudiant ou equipe projet ayant besoin d'un objet demonstrateur.
- Utilisateur curieux voulant identifier une musique depuis un objet autonome.
- Developpeur souhaitant experimenter la reconnaissance audio open source.

## 7. Contraintes

### Contraintes materielles

- Le prototype doit etre compatible avec Raspberry Pi Zero ou Pi Zero W.
- Le microphone cible est un MEMS I2S ICS-43434.
- L'affichage cible est un ecran e-ink.
- L'objet doit integrer des boutons physiques.
- L'alimentation peut s'appuyer sur un UPS HAT Waveshare avec batterie.
- Une extension future par carte MicroSD SPI doit rester envisageable.

### Contraintes logicielles

- Le langage principal est Python.
- L'interface web locale doit etre developpee avec Flask ou FastAPI.
- Les services doivent pouvoir etre lances au demarrage via systemd.
- La configuration doit rester lisible : `.env`, YAML ou JSON.
- Les dependances doivent rester compatibles avec les ressources limitees du
  Raspberry Pi Zero.

### Contraintes de documentation

- Les fichiers doivent etre ranges dans une architecture claire.
- Les schemas, croquis, fichiers CAO et documents projet doivent etre
  conserves dans le depot.
- Les choix techniques importants doivent etre expliques en Markdown.
- Les procedures de test doivent etre reproductibles.

## 8. Fonctions attendues

| Code | Fonction | Priorite |
| --- | --- | --- |
| F1 | Capturer un extrait audio via le micro I2S | Haute |
| F2 | Envoyer ou traiter l'extrait avec une solution de reconnaissance musicale | Haute |
| F3 | Recuperer les metadonnees du morceau | Haute |
| F4 | Afficher titre, artiste et etat sur ecran e-ink | Haute |
| F5 | Afficher une pochette si disponible | Moyenne |
| F6 | Afficher un egaliseur minimaliste si aucun morceau n'est reconnu | Moyenne |
| F7 | Fournir une interface web locale | Haute |
| F8 | Configurer le Wi-Fi simplement | Moyenne |
| F9 | Gerer les boutons physiques | Haute |
| F10 | Lancer automatiquement les services au demarrage | Moyenne |
| F11 | Documenter le montage et les tests | Haute |

## 9. Exigences fonctionnelles

### EF1 - Capture audio

Le systeme doit pouvoir enregistrer un extrait audio court depuis le microphone
I2S. La duree cible initiale est comprise entre 5 et 15 secondes.

Critere d'acceptation : un fichier audio exploitable est produit et lisible sur
le Raspberry Pi.

### EF2 - Reconnaissance musicale

Le systeme doit transmettre ou traiter l'extrait audio avec un moteur de
reconnaissance musicale open source.

Critere d'acceptation : pour un morceau connu et audible, le systeme retourne au
minimum un titre et un artiste lorsque le moteur le permet.

### EF3 - Affichage e-ink

Le systeme doit afficher les informations principales du morceau reconnu sur
l'ecran e-ink.

Critere d'acceptation : apres une reconnaissance reussie, l'ecran affiche un
etat stable contenant au minimum le titre et l'artiste.

### EF4 - Interface web locale

Le systeme doit proposer une interface web accessible depuis le reseau local.

Critere d'acceptation : un utilisateur connecte au meme reseau peut consulter
l'etat du systeme depuis un navigateur.

### EF5 - Boutons physiques

Le systeme doit gerer au minimum trois actions :

- lancer l'ecoute ;
- changer d'ecran ;
- mettre en veille ou reveiller le systeme.

Critere d'acceptation : chaque bouton declenche l'action attendue avec une
gestion correcte du rebond.

## 10. Exigences non fonctionnelles

| Domaine | Exigence |
| --- | --- |
| Performance | Le systeme doit rester utilisable sur Raspberry Pi Zero. |
| Maintenance | Le code doit etre modulaire et lisible. |
| Robustesse | Les erreurs de micro, reseau ou reconnaissance doivent etre gerees proprement. |
| Cout | Les composants doivent rester compatibles avec un prototype low-cost. |
| Evolutivite | Les modules doivent pouvoir etre remplaces sans reecrire toute l'application. |
| Documentation | Les etapes d'installation et de test doivent etre decrites. |

## 11. Architecture logicielle cible

```text
src/systus/
├── audio_capture/
├── recognition/
├── metadata/
├── display/
├── web/
├── wifi_setup/
├── buttons/
└── app.py
```

Chaque module doit pouvoir etre teste seul avant integration dans le flux
global.

## 12. Livrables attendus

- Depot Git structure.
- Documentation projet.
- Documentation technique.
- Schema de fonctionnement.
- Schema electrique.
- Liste materielle.
- Code source Python.
- Interface web locale.
- Scripts d'installation.
- Services systemd.
- Procedures de tests manuels.

## 13. Criteres de reussite du prototype

Le prototype est considere valide si :

- le Raspberry Pi capture un extrait audio ;
- une reconnaissance est lancee depuis un bouton ou l'interface web ;
- un resultat ou un etat d'echec clair est affiche sur e-ink ;
- l'interface web locale est accessible ;
- la documentation permet de comprendre le montage et de reproduire les tests.

## 14. Hypotheses a confirmer

- Modele exact de l'ecran e-ink.
- Moteur de reconnaissance musicale retenu.
- Duree optimale de capture audio.
- Format final du boitier cassette.
- Niveau d'autonomie attendu sur batterie.
- Niveau de finition attendu pour la soutenance ou demonstration.

