BUILD=build

.PHONY: all clean

all: SYSTUS_CDC SYSTUS_DocTechnique main

main:
	mkdir -p $(BUILD)
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD) main.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD) main.tex

SYSTUS_CDC:
	mkdir -p $(BUILD)
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD) SYSTUS_CDC.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD) SYSTUS_CDC.tex

SYSTUS_DocTechnique:
	mkdir -p $(BUILD)
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD) SYSTUS_DocTechnique.tex
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD) SYSTUS_DocTechnique.tex

clean:
	rm -rf $(BUILD)
