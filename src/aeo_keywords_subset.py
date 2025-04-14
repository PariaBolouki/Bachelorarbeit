import json
from pathlib import Path
from transformers import pipeline
from owlready2 import get_ontology, IRIS 

ontology_path = Path("ontologies") / "aeo.owl"
onto = get_ontology(str(ontology_path)).load()

output_file = Path("evaluation") / "aeo_keywords_subset.json"

target_class_ids = [
    "AEO_0000125", "AEO_0000131", "AEO_0000211", "AEO_0001018", "AEO_0001009",
    "AEO_0000212", "AEO_0000200", "CARO_0000029", "CARO_0000050", "CARO_0000063",
    "CARO_0000072", "AEO_0000193", "CARO_0000040", "AEO_0000090", "AEO_0000135",
    "AEO_0000151", "CARO_0000055", "AEO_0000183", "AEO_0000199", "AEO_0001006",
    "CL_0000062", "AEO_0000186", "AEO_0000215", "AEO_0000222", "CARO_0000008", 
    "CARO_0000010", "CL_0000000", "CL_0000066", "CL_0000015", "CL_0000080",
    "CL_0000737", "CL_0000746", "CL_0000540", "CL_0000107", "CL_0000526", 
    "CL_0002371", "CL_0000187", "CL_0002372", "CL_0000129", "CL_0002573",
    "CL_0002320", "CL_0000136", "CL_0000667", "CL_0000058", "CL_0000414",
    "CARO_0000000", "CARO_0000005", "AEO_0000079", "CL_0000055", "CL_0000165"
]

def extract_annotations(entity):
    text = ""
    for prop in ["IAO_0000115"]:
        if hasattr(entity, prop):
            value = getattr(entity, prop)
            if value:
                text += f"{value[0]} "
    return text.strip()

ontology_texts = {}

for cls in onto.classes():
    if cls.name in target_class_ids:
        name = f"Class:{cls.name}"
        text = extract_annotations(cls)
        if text:
            ontology_texts[name] = text

print(f"\nDie {len(ontology_texts)} Klassen mit Definitionen wurden extrahiert.\n")

keyword_pipeline = pipeline(
    "text2text-generation",
    model="ilsilfverskiold/tech-keywords-extractor",
    tokenizer="ilsilfverskiold/tech-keywords-extractor"
)

extracted_keywords = {}

for entity, text in ontology_texts.items():
    result = keyword_pipeline(text, max_length=50, truncation=True)[0]['generated_text']
    extracted_keywords[entity] = {
        "text": text,
        "keywords": result.split(", ")
    }

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(extracted_keywords, f, indent=2, ensure_ascii=False)

print(f"\nErgebnis gespeichert unter:\n{output_file}")
