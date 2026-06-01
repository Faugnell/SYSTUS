# Outils de management - S.Y.S.T.U.S.

## 1. Methode de pilotage

Le projet est pilote de maniere incrementale. Chaque etape doit produire un
resultat testable avant de passer a la suivante.

Principe :

- documenter avant d'assembler ;
- tester chaque module seul ;
- integrer progressivement ;
- garder une trace des decisions techniques ;
- privilegier un prototype fonctionnel avant l'optimisation.

## 2. Phases du projet

| Phase | Objectif | Livrable principal |
| --- | --- | --- |
| P1 | Cadrage | Cahier des charges et analyse fonctionnelle |
| P2 | Architecture | Architecture logicielle et materielle |
| P3 | Validation audio | Capture audio fonctionnelle |
| P4 | Reconnaissance | Identification musicale testee |
| P5 | Affichage | Rendu e-ink exploitable |
| P6 | Interface web | Interface locale minimale |
| P7 | Integration | Prototype assemble |
| P8 | Documentation finale | Guide de montage et tests |

## 3. WBS

```text
1. Gestion projet
   1.1 Cahier des charges
   1.2 Analyse fonctionnelle
   1.3 Planning
   1.4 Suivi des risques

2. Conception materielle
   2.1 Choix composants
   2.2 Schema electrique
   2.3 Branchement micro I2S
   2.4 Branchement e-ink
   2.5 Integration boutons
   2.6 Boitier style cassette

3. Conception logicielle
   3.1 Architecture Python
   3.2 Module capture audio
   3.3 Module reconnaissance
   3.4 Module metadonnees
   3.5 Module affichage
   3.6 Interface web
   3.7 Configuration Wi-Fi
   3.8 Services systemd

4. Tests
   4.1 Test audio
   4.2 Test reconnaissance
   4.3 Test affichage
   4.4 Test boutons
   4.5 Test Wi-Fi
   4.6 Test autonomie

5. Documentation
   5.1 Guide installation
   5.2 Guide cablage
   5.3 Guide utilisation
   5.4 Bilan prototype
```

## 4. Planning type

Planning indicatif a adapter selon la duree reelle du projet.

| Semaine | Objectif | Resultat attendu |
| --- | --- | --- |
| S1 | Cadrage et structure depot | Documentation projet initiale |
| S2 | Choix materiels et schemas | BOM et schema de cablage v1 |
| S3 | Capture audio | Enregistrement WAV depuis micro I2S |
| S4 | Reconnaissance musicale | Test d'identification sur extraits |
| S5 | Affichage e-ink | Ecran de resultat lisible |
| S6 | Interface web locale | Page d'etat et action d'ecoute |
| S7 | Integration boutons et systemd | Prototype utilisable sans terminal |
| S8 | Tests et documentation finale | Demo stable et dossier complet |

## 5. Jalons

| Jalon | Description | Critere de validation |
| --- | --- | --- |
| J1 | Depot structure | Arborescence docs/code disponible |
| J2 | Audio valide | Un extrait WAV est capture sur Raspberry Pi |
| J3 | Reconnaissance valide | Un morceau connu est identifie |
| J4 | Affichage valide | L'ecran e-ink affiche titre et artiste |
| J5 | Interface valide | L'interface web locale repond |
| J6 | Prototype integre | Bouton -> capture -> reconnaissance -> affichage |
| J7 | Documentation finale | Installation et tests reproductibles |

## 6. Tableau Kanban

Colonnes conseillees :

- A faire
- En cours
- A tester
- Termine
- Bloque

Exemples de cartes :

| Carte | Priorite | Etat |
| --- | --- | --- |
| Choisir le modele exact d'ecran e-ink | Haute | A faire |
| Documenter le brochage du micro ICS-43434 | Haute | A faire |
| Tester la capture audio ALSA | Haute | A faire |
| Comparer les solutions de reconnaissance open source | Haute | A faire |
| Creer une page web de diagnostic | Moyenne | A faire |
| Ajouter le service systemd | Moyenne | A faire |
| Modeliser le boitier cassette | Moyenne | A faire |

## 7. Matrice RACI

Hypothese : projet mene principalement par une personne. A adapter si le projet
est realise en equipe.

| Tache | Responsable | Approbateur | Consulte | Informe |
| --- | --- | --- | --- | --- |
| Cahier des charges | Porteur projet | Encadrant | Utilisateurs tests | Equipe |
| Choix materiels | Porteur projet | Encadrant | Fournisseurs/docs | Equipe |
| Architecture logicielle | Developpeur | Porteur projet | Encadrant | Equipe |
| Montage electronique | Porteur projet | Encadrant | Documentation fabricant | Equipe |
| Tests prototype | Porteur projet | Encadrant | Utilisateurs tests | Equipe |
| Documentation finale | Porteur projet | Encadrant | Equipe | Jury/public |

## 8. Matrice des risques

| Risque | Probabilite | Impact | Prevention | Plan de secours |
| --- | --- | --- | --- | --- |
| Micro I2S mal configure | Moyenne | Eleve | Tester ALSA tot | Utiliser micro USB temporaire |
| Reconnaissance trop lourde | Moyenne | Eleve | Comparer plusieurs solutions | Envoyer l'extrait a un service local distant |
| Ecran e-ink lent | Haute | Moyen | Limiter les rafraichissements | Afficher uniquement les etats importants |
| Wi-Fi instable | Moyenne | Moyen | Tester la reconnexion | Configuration manuelle par fichier |
| Batterie insuffisante | Moyenne | Moyen | Mesurer la consommation | Demo sur alimentation USB |
| Delai de CAO trop long | Moyenne | Moyen | Commencer avec boitier simple | Presenter une maquette non finale |
| Dependances incompatibles Pi Zero | Moyenne | Eleve | Installer tot sur cible | Simplifier la stack logicielle |

## 9. Indicateurs de suivi

| Indicateur | Cible |
| --- | --- |
| Modules documentes | 100 % des modules principaux |
| Fonctions critiques testees | Audio, reconnaissance, affichage |
| Temps de reconnaissance | A mesurer, objectif raisonnable pour demo |
| Taux de reconnaissance demo | Au moins un extrait connu reconnu |
| Autonomie | A mesurer apres integration UPS |
| Bugs bloquants avant demo | 0 |

## 10. Budget previsionnel

Les prix sont indicatifs et doivent etre confirmes au moment de l'achat.

| Element | Quantite | Cout unitaire estime | Total estime |
| --- | --- | --- | --- |
| Raspberry Pi Zero / Zero W | 1 | A confirmer | A confirmer |
| Micro MEMS I2S ICS-43434 | 1 | A confirmer | A confirmer |
| Ecran e-ink | 1 | A confirmer | A confirmer |
| Boutons physiques | 3 | A confirmer | A confirmer |
| UPS HAT Waveshare | 1 | A confirmer | A confirmer |
| Batterie compatible | 1 | A confirmer | A confirmer |
| Cables, connecteurs, visserie | 1 lot | A confirmer | A confirmer |
| Impression 3D / prototypage boitier | 1 | A confirmer | A confirmer |

## 11. Compte rendu type

```text
Date :
Participant(s) :

Objectif de la session :

Travail realise :

Problemes rencontres :

Decisions prises :

Actions a faire :

Prochaine etape :
```

## 12. Journal de decisions type

| Date | Decision | Justification | Impact |
| --- | --- | --- | --- |
| A completer | A completer | A completer | A completer |

## 13. Definition of Done

Une tache est consideree terminee si :

- le resultat attendu est produit ;
- le test manuel ou automatique associe est effectue ;
- la documentation utile est mise a jour ;
- les limites connues sont notees ;
- le depot reste dans un etat comprehensible.

