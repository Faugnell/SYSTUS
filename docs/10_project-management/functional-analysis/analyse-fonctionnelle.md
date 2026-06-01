# Analyse fonctionnelle - S.Y.S.T.U.S.

## 1. Systeme et finalite

S.Y.S.T.U.S est un objet de prototypage capable d'ecouter un extrait musical,
d'identifier le morceau et d'afficher les informations principales sur un ecran
e-ink.

Finalite : fournir une experience de reconnaissance musicale autonome, lisible
et documentee dans un objet physique au style cassette futuriste.

## 2. Expression du besoin

### Bete a cornes

| Question | Reponse |
| --- | --- |
| A qui le produit rend-il service ? | A un utilisateur qui souhaite identifier une musique depuis un objet autonome. |
| Sur quoi agit-il ? | Sur un extrait sonore capte dans l'environnement. |
| Dans quel but ? | Reconnaitre le morceau et afficher ses informations principales. |

Formulation du besoin :

> Permettre a un utilisateur d'identifier une musique diffusee autour de lui a
> l'aide d'un objet autonome, documente et accessible.

## 3. Environnement du systeme

Elements exterieurs :

- Utilisateur.
- Musique ambiante.
- Reseau Wi-Fi local.
- Source d'alimentation ou batterie.
- Base ou service de reconnaissance musicale.
- Navigateur web local.
- Ecran e-ink.
- Boutons physiques.
- Boitier du prototype.

## 4. Diagramme pieuvre textuel

| Code | Relation avec l'environnement | Type |
| --- | --- | --- |
| FP1 | Identifier une musique diffusee dans l'environnement | Fonction principale |
| FC1 | Etre commande simplement par l'utilisateur | Contrainte |
| FC2 | Afficher une information lisible sur ecran e-ink | Contrainte |
| FC3 | Fonctionner sur Raspberry Pi Zero | Contrainte |
| FC4 | Communiquer avec le reseau Wi-Fi local | Contrainte |
| FC5 | Utiliser des composants accessibles et low-cost | Contrainte |
| FC6 | Etre maintenable et documente | Contrainte |
| FC7 | S'integrer dans un boitier au style cassette futuriste | Contrainte |
| FC8 | Gerer les echecs de reconnaissance sans bloquer l'utilisateur | Contrainte |

## 5. Fonctions de service

### FP1 - Reconnaitre une musique

Le systeme doit capter un extrait sonore, l'analyser via un moteur de
reconnaissance, puis produire un resultat exploitable.

Entrees :

- signal audio ambiant ;
- action de lancement utilisateur.

Sorties :

- titre ;
- artiste ;
- album si disponible ;
- pochette si disponible ;
- etat de reconnaissance.

### FS1 - Capturer un extrait audio

Le systeme doit enregistrer un extrait court avec le microphone MEMS I2S.

### FS2 - Traiter ou envoyer l'extrait

Le systeme doit transmettre l'extrait au module de reconnaissance ou a un
service compatible.

### FS3 - Normaliser les metadonnees

Le systeme doit convertir le resultat de reconnaissance en structure commune
pour l'affichage et l'interface web.

### FS4 - Afficher le resultat

Le systeme doit produire une vue e-ink claire : titre, artiste, album, image ou
etat alternatif.

### FS5 - Proposer une interface web locale

Le systeme doit permettre la consultation de l'etat, de la configuration et des
resultats depuis un navigateur local.

### FS6 - Gerer les commandes physiques

Le systeme doit associer les boutons aux actions principales.

## 6. Fonctions contraintes

| Code | Fonction contrainte | Critere | Niveau attendu |
| --- | --- | --- | --- |
| FC1 | Rester leger | Usage CPU/RAM | Compatible Raspberry Pi Zero |
| FC2 | Rester low-cost | Cout composants | Raisonnable pour prototype maker |
| FC3 | Etre lisible | Affichage | Texte comprehensible sur e-ink |
| FC4 | Etre modulaire | Architecture | Modules separes et testables |
| FC5 | Etre documente | Documentation | Procedures et schemas disponibles |
| FC6 | Etre robuste | Erreurs | Message clair en cas d'echec |
| FC7 | Etre evolutif | Extensions | Wi-Fi, stockage, autonomie, UI |

## 7. Scenarios d'utilisation

### Scenario nominal

1. L'utilisateur allume S.Y.S.T.U.S.
2. Le systeme demarre ses services.
3. L'utilisateur appuie sur le bouton d'ecoute.
4. Le systeme capture un extrait audio.
5. Le module de reconnaissance analyse l'extrait.
6. Les metadonnees sont recuperees.
7. L'ecran e-ink affiche le titre et l'artiste.
8. L'interface web locale affiche le dernier resultat.

### Scenario sans reconnaissance

1. L'utilisateur lance une ecoute.
2. Le systeme capture correctement l'audio.
3. Aucun morceau n'est reconnu.
4. L'ecran affiche un etat "non reconnu" ou une visualisation minimaliste.
5. L'utilisateur peut relancer une ecoute.

### Scenario configuration Wi-Fi

1. Le systeme ne trouve aucun reseau configure.
2. Il lance un mode configuration.
3. L'utilisateur se connecte au point d'acces local.
4. Il renseigne les parametres Wi-Fi.
5. Le systeme redemarre la connexion.

## 8. Criticite des fonctions

| Fonction | Importance | Commentaire |
| --- | --- | --- |
| Capture audio | Critique | Sans audio exploitable, aucune reconnaissance possible. |
| Reconnaissance musicale | Critique | Coeur fonctionnel du projet. |
| Affichage e-ink | Critique | Sortie principale de l'objet. |
| Boutons physiques | Importante | Rend l'objet autonome sans ordinateur. |
| Interface web | Importante | Simplifie configuration et diagnostic. |
| Portail Wi-Fi | Secondaire au prototype | Peut venir apres l'interface web minimale. |
| Pochette | Secondaire | Ameliore l'experience mais non bloquant. |
| Autonomie batterie | Secondaire au debut | A optimiser apres validation du flux. |

## 9. Chaine fonctionnelle

```text
Utilisateur
  -> Bouton ecoute
  -> Raspberry Pi
  -> Micro I2S
  -> Fichier audio temporaire
  -> Module de reconnaissance
  -> Metadonnees normalisees
  -> Rendu e-ink
  -> Interface web locale
```

## 10. Points a valider

- Qualite du signal audio avec le microphone ICS-43434.
- Compatibilite du moteur de reconnaissance sur Raspberry Pi Zero.
- Temps de traitement acceptable.
- Lisibilite de l'ecran e-ink avec pochette ou sans pochette.
- Ergonomie des boutons physiques.
- Consommation electrique avec l'UPS HAT.

