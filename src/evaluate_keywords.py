import json
import csv
from pathlib import Path

gold_file = Path("evaluation") / "aeo_goldstandard.json"
auto_file = Path("evaluation") / "aeo_keywords_subset.json"
output_csv = Path("evaluation") / "evaluation_results.csv"

with open(gold_file, "r", encoding="utf-8") as f:
    gold_data = json.load(f)

with open(auto_file, "r", encoding="utf-8") as f:
    auto_data = json.load(f)

results = []

for class_id in gold_data:
    gold_keywords = set(kw.lower() for kw in gold_data[class_id]["keywords"])
    auto_keywords = set(kw.lower() for kw in auto_data.get(class_id, {}).get("keywords", []))
    
    tp = len(gold_keywords & auto_keywords)
    fp = len(auto_keywords - gold_keywords)
    fn = len(gold_keywords - auto_keywords)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    results.append({
        "Class": class_id,
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "Precision": round(precision, 2),
        "Recall": round(recall, 2),
        "F1-Score": round(f1, 2),
    })

num_classes = len(results)
avg_precision = sum(r["Precision"] for r in results) / num_classes if num_classes > 0 else 0
avg_recall = sum(r["Recall"] for r in results) / num_classes if num_classes > 0 else 0
avg_f1 = sum(r["F1-Score"] for r in results) / num_classes if num_classes > 0 else 0

results.append({
    "Class": "Average",
    "TP": "",
    "FP": "",
    "FN": "",
    "Precision": round(avg_precision, 2),
    "Recall": round(avg_recall, 2),
    "F1-Score": round(avg_f1, 2),
})


with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Class", "TP", "FP", "FN", "Precision", "Recall", "F1-Score"])
    writer.writeheader()
    writer.writerows(results)

print(f"\nEvaluation abgeschlossen. Ergebnisse gespeichert unter: {output_csv}")
