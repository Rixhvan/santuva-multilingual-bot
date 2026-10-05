import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Ensure backend can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.services.nlp_service import nlp_service
from backend.config.settings import EVALUATION_DIR

def evaluate_language_dataset(dataset_path: Path, expected_lang_code: str, lang_name: str) -> Dict[str, Any]:
    with open(dataset_path, "r", encoding="utf-8") as f:
        samples = json.load(f)

    total = len(samples)
    lang_correct = 0
    intent_correct = 0
    tp_entities = 0
    fp_entities = 0
    fn_entities = 0
    code_switch_total = 0
    code_switch_correct = 0

    for item in samples:
        text = item["text"]
        target_intent = item["intent"]
        expected_entities = item.get("entities", {})
        category = item.get("category", "")

        # Process through NLP Service
        res = nlp_service.process_query(text, session_id="eval_session")

        # 1. Language ID
        pred_lang_code = res.nlp_analysis.language_info.language_code
        # In Tulu code-switched queries, primary lang could be detected as tcy or en, both valid if is_code_switched is True
        if pred_lang_code == expected_lang_code:
            lang_correct += 1
        elif expected_lang_code == "tcy" and res.nlp_analysis.language_info.is_code_switched:
            lang_correct += 1

        # 2. Intent Accuracy
        pred_intent = res.nlp_analysis.intent_info.intent
        sec_intent = res.nlp_analysis.intent_info.secondary_intent
        if pred_intent == target_intent or sec_intent == target_intent:
            intent_correct += 1

        # 3. Entity Precision / Recall / F1
        pred_entities = {e.label.lower(): e.text for e in res.nlp_analysis.entities}
        for k, v in expected_entities.items():
            if k in pred_entities:
                tp_entities += 1
            else:
                fn_entities += 1
        for k in pred_entities:
            if k not in expected_entities:
                fp_entities += 1

        # 4. Code-Switching Accuracy
        if category == "code_switching":
            code_switch_total += 1
            if res.nlp_analysis.language_info.is_code_switched:
                code_switch_correct += 1

    precision = tp_entities / (tp_entities + fp_entities) if (tp_entities + fp_entities) > 0 else 1.0
    recall = tp_entities / (tp_entities + fn_entities) if (tp_entities + fn_entities) > 0 else 1.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "language": lang_name,
        "language_code": expected_lang_code,
        "total_samples": total,
        "language_accuracy": round((lang_correct / total) * 100, 2),
        "intent_accuracy": round((intent_correct / total) * 100, 2),
        "entity_precision": round(precision * 100, 2),
        "entity_recall": round(recall * 100, 2),
        "entity_f1": round(f1 * 100, 2),
        "code_switching_accuracy": round((code_switch_correct / max(1, code_switch_total)) * 100, 2) if code_switch_total > 0 else "N/A"
    }

def run_all_evaluations():
    print("=" * 70)
    print("MULTILINGUAL NLP PIPELINE BENCHMARK EVALUATION REPORT")
    print("=" * 70)

    datasets = [
        ("sa_100.json", "sa", "Sanskrit"),
        ("en_100.json", "en", "English"),
        ("tu_100.json", "tcy", "Tulu")
    ]

    all_metrics = []
    for filename, code, name in datasets:
        path = EVALUATION_DIR / filename
        metrics = evaluate_language_dataset(path, code, name)
        all_metrics.append(metrics)

    print(f"\n{'Language':<12} | {'Samples':<8} | {'Lang Acc':<10} | {'Intent Acc':<10} | {'NER F1':<8} | {'Code-Switch Acc':<15}")
    print("-" * 75)
    for m in all_metrics:
        cs_str = f"{m['code_switching_accuracy']}%" if m['code_switching_accuracy'] != "N/A" else "N/A"
        print(f"{m['language']:<12} | {m['total_samples']:<8} | {m['language_accuracy']:>8}% | {m['intent_accuracy']:>9}% | {m['entity_f1']:>6}% | {cs_str:>15}")

    print("\n" + "=" * 70)
    print("DETAILED METRICS PER LANGUAGE")
    print("=" * 70)
    for m in all_metrics:
        print(f"\n--- {m['language'].upper()} (Code: {m['language_code']}) ---")
        print(f"Total Test Examples: {m['total_samples']}")
        print(f"Language Identification Accuracy: {m['language_accuracy']}%")
        print(f"Intent Classification Accuracy:    {m['intent_accuracy']}%")
        print(f"Named Entity Recognition Precision: {m['entity_precision']}%")
        print(f"Named Entity Recognition Recall:    {m['entity_recall']}%")
        print(f"Named Entity Recognition F1:        {m['entity_f1']}%")
        if m['code_switching_accuracy'] != "N/A":
            print(f"Code-Switching Detection Accuracy:  {m['code_switching_accuracy']}%")

    return all_metrics

if __name__ == "__main__":
    run_all_evaluations()
