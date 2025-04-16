# Extraktion und Analyse von Symbolnamen in beschreibungslogischen Ontologien
## Symbolnamen extrahieren

Um Symbolnamen aus einer OWL-Ontologie im Verzeichnis `ontologies/` zu extrahieren, kann das folgende Skript ausgeführt werden: 

- Für die Pizza-Ontologie: python src/symbolName_extractor.py pizza.owl
- Für die Clyh-Ontologie: python src/symbolName_extractor.py clyh.owl
- Für die Three-ST-Ontologie: python src/symbolName_extractor.py 3st.owl
- Für die Gene-Ontologie: python src/symbolName_extractor.py gene.owl

Die Ergebnisse der Symbolnamen-Extraktion werden als `<ontologietitel>_symbolnames.json` im Ordner `results/` gespeichert.

## Annotationen analysieren

Um statistische Informationen über Annotation Properties aus einer OWL-Ontologie im Verzeichnis `ontologies/` zu extrahieren, kann das folgende Skript ausgeführt werden:

- Für die Pizza-Ontologie: python src/annotation_statistics.py pizza.owl
- Für die Clyh-Ontologie: python src/annotation_statistics.py clyh.owl
- Für die Three-ST-Ontologie: python src/annotation_statistics.py 3st.owl
- Für die Gene-Ontologie: python src/annotation_statistics.py gene.owl

Die Ergebnisse der Analyse werden als `<ontologietitel>_annotation_stats.json` im Ordner `results/` gespeichert.

## Keywords extrahieren

Um automatisch Keywords aus den textuellen Annotationen einer OWL-Ontologie im Verzeichnis `ontologies/` zu extrahieren, kann das folgende Skript verwendet werden:

- Für die Pizza-Ontologie: python src/keyword_extractor.py pizza.owl
- Für die Clyh-Ontologie: python src/keyword_extractor.py clyh.owl
- Für die Gene-Ontologie: python src/keyword_extractor.py gene.owl

Die Gene-Ontologie ist sehr umfangreich – abhängig von der Hardware kann die Keyword-Extraktion **mehrere Stunden** in Anspruch nehmen.

Die Ergebnisse werden als `<ontologietitel>_keywords.json` im Ordner `results/` gespeichert.  

Die Ontologie `3st.owl` enthält keine textuellen Annotationen, daher wurde für diese Ontologie keine keyword-Extraktion durchgeführt.

## Evaluation

Der manuell erstellte Goldstandard befindet sich in `evaluation/aeo_goldstandard.json`

Um automatisch Keywords aus den Definitionen derselben 50 Klassen der Ontologie `aeo.owl` zu extrahieren, kann das folgende Skript verwendet werden: python src/aeo_keywords_subset.py

Die Ergebnisse werden als `aeo_keywords_subset.json` im Ordner `evaluation/` gespeichert.

Um die automatisch extrahierten Keywords mit dem Goldstandard vergleichen, kann das folgende Skript ausgeführt werden: python src/evaluate_keywords.py

Die Evaluationsergebnisse werden im CSV-Format als `evaluation_results.csv` im Ordner `evaluation/` gespeichert.







