import json
import sys
from pathlib import Path
from owlready2 import get_ontology
from transformers import pipeline

filename = sys.argv[1]
ontology_path = Path("ontologies") / filename
onto = get_ontology(str(ontology_path)).load()
ontology_name = ontology_path.stem

output_dir = Path("results")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / f"{ontology_name}_keywords.json"

def extract_annotations(entity):
    text = ""
    for prop in ["IAO_0000115", "comment", "definition", "description"]:
        if hasattr(entity, prop):
            value = getattr(entity, prop)
            if value:
                text += f"{value[0]} "
    return text.strip()

ontology_texts = {}

for cls in onto.classes():
    name = f"Class:{cls.name}"
    text = extract_annotations(cls)
    if text:
        ontology_texts[name] = text

for prop in onto.object_properties():
    name = f"ObjectProperty:{prop.name}"
    text = extract_annotations(prop)
    if text:
        ontology_texts[name] = text

for prop in onto.data_properties():
    name = f"DataProperty:{prop.name}"
    text = extract_annotations(prop)
    if text:
        ontology_texts[name] = text

for prop in onto.annotation_properties():
    name = f"AnnotationProperty:{prop.name}"
    text = extract_annotations(prop)
    if text:
        ontology_texts[name] = text

for indiv in onto.individuals():
    name = f"Individual:{indiv.name}"
    text = extract_annotations(indiv)
    if text:
        ontology_texts[name] = text

print(f"{len(ontology_texts)} Annotationstexte extrahiert.")

keyword_pipeline = pipeline(
    "text2text-generation",
    model="ilsilfverskiold/tech-keywords-extractor",
    tokenizer="ilsilfverskiold/tech-keywords-extractor"
)

extracted_keywords = {}

for entity, text in ontology_texts.items():
    keyword_result = keyword_pipeline(text, max_length=50, truncation=True)[0]['generated_text']
    extracted_keywords[entity] = {
        "text": text,
        "keywords": keyword_result.split(", ")
    }


with open(output_file, "w", encoding="utf-8") as f:
    json.dump(extracted_keywords, f, indent=2, ensure_ascii=False)

print(f"\nSchlüsselwörter gespeichert unter: {output_file}")
