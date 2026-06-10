# Documentation LaTeX S.Y.S.T.U.S.

Ce dossier contient le rendu documentaire du projet S.Y.S.T.U.S. pour la
période du 11 mai 2026 au 11 juin 2026.

Le poster de présentation n'est pas inclus ici, conformément au choix de le
réaliser séparément.

## Contenu

- `main.tex` : document principal.
- `sections/` : chapitres LaTeX du rendu.
- `build/` : dossier de sortie généré à la compilation.
- `Makefile` : commande pratique pour générer le PDF.

## Compilation

Depuis le dossier `docs` :

```bash
make
```

Ou directement :

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

Le PDF attendu sera généré dans `docs/build/main.pdf`.

## Informations à compléter avant rendu

- Groupe et encadrant.
- Résultats de tests réellement observés sur Raspberry Pi.
- Captures, schémas et photos du montage si disponibles.
