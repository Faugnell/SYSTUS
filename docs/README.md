# Documentation S.Y.S.T.U.S

Ce dossier centralise toute la documentation du projet. Il separe les documents
de gestion projet, la documentation technique et les ressources visuelles afin
de garder le depot lisible pendant les iterations de prototypage.

## Plan

```text
docs/
├── 00_overview/            # Vision generale, glossaire, schema global
├── 10_project-management/  # Analyse, cahier des charges, planning, WBS
├── 20_technical/           # Architecture, hardware, software, tests manuels
└── 30_assets/              # Images, references, exports de croquis
```

## Regles de rangement

- Les fichiers sources modifiables vont dans leur dossier metier
  (`.docx`, `.drawio`, `.f3d`, `.step`, `.kicad_*`, etc.).
- Les exports consultables vont de preference en PDF, PNG ou SVG dans le meme
  dossier ou dans `30_assets/` si ce sont des ressources communes.
- Les noms de fichiers utilisent des minuscules, des tirets et pas d'espaces,
  par exemple `schema-electrique-v1.pdf`.
- Chaque decision importante doit etre resumee dans un fichier Markdown pour
  rester lisible sans outil proprietaire.

## Documents deja ranges

- `10_project-management/functional-analysis/analyse-fonctionnelle.docx`
- `10_project-management/specifications/cahier-des-charges.docx`
- `10_project-management/tools/outils-de-management.docx`
