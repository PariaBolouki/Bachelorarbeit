import json
import sys
from pathlib import Path
from transformers import pipeline
from owlready2 import get_ontology

filename = sys.argv[1]
ontology_path = Path("ontologies") / filename
onto = get_ontology(str(ontology_path)).load()
ontology_name = ontology_path.stem

output_dir = Path("results")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / f"{ontology_name}_keywords.json"

ontology_texts = {}

for cls in onto.classes():
    entity_name = cls.name
    entity_info = ""

    if hasattr(cls, "IAO_0000115") and cls.IAO_0000115:
        entity_info += f"{cls.IAO_0000115[0]} "

    if hasattr(cls, "comment") and cls.comment:
        entity_info += f"{cls.comment[0]} "

    if hasattr(cls, "definition") and cls.definition:
        entity_info += f"{cls.definition[0]} "

    if hasattr(cls, "description") and cls.description:
        entity_info += f"{cls.description[0]} "

    if entity_info.strip():
        ontology_texts[entity_name] = entity_info.strip()

print(f"🔍 {len(ontology_texts)} Texte aus Ontologie geladen.")

keyword_pipeline = pipeline(
    "text2text-generation",
    model="ilsilfverskiold/tech-keywords-extractor",
    tokenizer="ilsilfverskiold/tech-keywords-extractor"
)

extracted_keywords = {}

for entity, text in ontology_texts.items():
    print(f"➡️  Verarbeite: {entity}")
    result = keyword_pipeline(text, max_length=50, truncation=True)[0]["generated_text"]
    extracted_keywords[entity] = {
        "text": text,
        "keywords": result.split(", ")
    }

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(extracted_keywords, f, indent=2, ensure_ascii=False)

print(f"\n✅ Keyword-Extraktion abgeschlossen. Datei gespeichert unter: {output_file}")
