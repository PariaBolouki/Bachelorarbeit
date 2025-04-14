# Bachelorarbeit
## Symbolnamen extrahieren

Um Symbolnamen aus einer OWL-Ontologie im Verzeichnis 'ontologies/' zu extrahieren, kann das folgende Skript ausgeführt werden: 

- Für die Pizza-Ontologie:
python src/symbolName_extractor.py pizza.owl
- Für die Clyh-Ontologie:
python src/symbolName_extractor.py clyh.owl
- Für die Three-ST-Ontologie:
python src/symbolName_extractor.py 3st.owl

Die Ergebnisse der Symbolnamen-Extraktion werden als ` <ontologietitel>_symbolnames.json` im Ordner 'results/' gespeichert.

