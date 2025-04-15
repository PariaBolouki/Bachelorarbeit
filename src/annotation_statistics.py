import json
import sys
from owlready2 import get_ontology
from rdflib import URIRef
from collections import defaultdict
from pathlib import Path
from rdflib.namespace import RDF

filename = sys.argv[1]
ontology_path = Path("ontologies") / filename
onto = get_ontology(str(ontology_path)).load()
ontology_name = ontology_path.stem

output_dir = Path("results")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / f"{ontology_name}_annotation_stats.json"

def count_words(text):
    return len(text.strip().split())

def shorten_uri(uri):
    uri_str = str(uri)
    if "#" in uri_str:
        return uri_str.split("#")[-1]
    else:
        return uri_str.split("/")[-1]

classes = list(onto.classes())
obj_props = list(onto.object_properties())
data_props = list(onto.data_properties())
anno_props = list(onto.annotation_properties())
individuals = list(onto.individuals())
all_elements = classes + obj_props + data_props + anno_props + individuals

graph = onto.world.as_rdflib_graph()

annotation_distribution = defaultdict(lambda: defaultdict(set)) 
annotation_word_counts = defaultdict(list)

def get_type(element):
    if element in classes:
        return "Klasse"
    elif element in obj_props:
        return "Objekt-Property"
    elif element in data_props:
        return "Daten-Property"
    elif element in anno_props:
        return "Annotation-Property"
    elif element in individuals:
        return "Individuum"
    return "Unbekannt"


for element in all_elements:
    for s, p, o in graph.triples((element.storid, None, None)):
        p_short = shorten_uri(p)
        if p == RDF.type or p_short in {"subClassOf", "sameAs", "equivalentClass", "inverseOf", "subPropertyOf", "disjointWith"}:
            continue  
        typ = get_type(element)
        annotation_distribution[p_short][typ].add(str(element))

        if isinstance(o, str):
            annotation_word_counts[p_short].append(count_words(o))

output_data = {
    "ontologie": ontology_name,
    "statistik": {
        "klassen": len(classes),
        "objekt_properties": len(obj_props),
        "daten_properties": len(data_props),
        "annotation_properties": len(anno_props),
        "individuals": len(individuals)
    },
    "Verteilung von Annotationen": [],
}

for ann, typ_map in annotation_distribution.items():
    eintrag = {
        "annotation": ann,
        "gesamt": sum(len(v) for v in typ_map.values()),
        "typen": {typ: len(elements) for typ, elements in typ_map.items()},
    }
    if ann in annotation_word_counts:
        avg = round(sum(annotation_word_counts[ann]) / len(annotation_word_counts[ann]), 2)
        eintrag["durchschnittliche_wortanzahl"] = avg
    output_data["Verteilung von Annotationen"].append(eintrag)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"Annotation-Statistik gespeichert unter: {output_file}")
