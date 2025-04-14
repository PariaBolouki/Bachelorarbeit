# Bachelorarbeit
## Symbolnamen extrahieren

Um Symbolnamen aus einer OWL-Ontologie im Verzeichnis `ontologies/` zu extrahieren, kann das folgende Skript ausgeführt werden: 

- Für die Pizza-Ontologie: python src/symbolName_extractor.py pizza.owl
- Für die Clyh-Ontologie: python src/symbolName_extractor.py clyh.owl
- Für die Three-ST-Ontologie: python src/symbolName_extractor.py 3st.owl

Die Ergebnisse der Symbolnamen-Extraktion werden als `<ontologietitel>_symbolnames.json` im Ordner `results/` gespeichert.

## Annotationen analysieren

Um statistische Informationen über Annotation Properties aus einer OWL-Ontologie im Verzeichnis `ontologies/` zu extrahieren, kann das folgende Skript ausgeführt werden:

- Für die Pizza-Ontologie: python src/annotation_statistics.py pizza.owl
- Für die Clyh-Ontologie: python src/annotation_statistics.py clyh.owl
- Für die Three-ST-Ontologie: python src/annotation_statistics.py 3st.owl

Die Ergebnisse der Analyse werden als `<ontologietitel>_annotation_stats.json` im Ordner `results/` gespeichert.

## Keywords extrahieren

Um automatisch Keywords aus den textuellen Annotationen einer OWL-Ontologie im Verzeichnis `ontologies/` zu extrahieren, kann das folgende Skript verwendet werden:

- Für die Pizza-Ontologie: python src/keyword_extractor.py pizza.owl

- Für die Clyh-Ontologie: python src/keyword_extractor.py clyh.owl

Die Ergebnisse werden als `<ontologietitel>_keywords.json` im Ordner `results/` gespeichert.  

Die Ontologie `3st.owl` enthält keine textuellen Annotationen, daher wurde für diese Ontologie keine keyword-Extraktion durchgeführt.

Hinweis: Zur Ausführung dieses Skripts wird das Python-Modul `transformers` benötigt.  
Es kann mit `pip install transformers` installiert werden.



