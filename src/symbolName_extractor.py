import json
import sys
from owlready2 import get_ontology
from pathlib import Path


filename = sys.argv[1]
ontology_path = Path("ontologies") / filename

onto = get_ontology(str(ontology_path)).load()
ontology_name = ontology_path.stem

output_dir = Path("results")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / f"{ontology_name}_symbolnames.json"

annotation_properties = [
    prop for prop in onto.properties()
    if "AnnotationProperty" in str(type(prop))
]

data = {
    "titel": "Extraktion aus OWL-Ontologie",
    "ontologie": ontology_name,
    "anzahl": {
        "klassen": len(list(onto.classes())),
        "objekt_properties": len(list(onto.object_properties())),
        "daten_properties": len(list(onto.data_properties())),
        "annotation_properties": len(annotation_properties),
        "individuals": len(list(onto.individuals()))
    },
    "klassen": [],
    "objekt_properties": [],
    "daten_properties": [],
    "annotation_properties": [],
    "individuals": [],
}

for cls in onto.classes():
    data["klassen"].append({
        "symbol": cls.name,
        "label": getattr(cls, "label", []),
        "comment": getattr(cls, "comment", []),
        "definition": getattr(cls, "definition", []),
    })

for prop in onto.object_properties():
    data["objekt_properties"].append({
        "name": prop.name,
        "label": getattr(prop, "label", []),
        "comment": getattr(prop, "comment", []),
    })

for prop in onto.data_properties():
    data["daten_properties"].append({
        "name": prop.name,
        "label": getattr(prop, "label", []),
        "comment": getattr(prop, "comment", []),
    })

for prop in annotation_properties:
    data["annotation_properties"].append({
        "name": prop.name,
        "label": getattr(prop, "label", []),
        "comment": getattr(prop, "comment", []),
    })

for individual in onto.individuals():
    data["individuals"].append({
        "name": individual.name,
        "label": getattr(individual, "label", []),
        "comment": getattr(individual, "comment", []),
    })

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Datei {filename} wurde verarbeitet.")
print(f"Ergebnis: {output_file}")
