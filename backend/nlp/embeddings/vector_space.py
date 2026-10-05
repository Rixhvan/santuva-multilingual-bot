import json
import math
from typing import List, Dict, Tuple, Optional
from collections import Counter
from backend.config.settings import INTENTS_DIR

class MultilingualSemanticVectorSpace:
    """
    Multilingual Semantic Vector Space.
    Constructs cross-lingual character and subword n-gram representations
    aligned with semantic concept anchors and intent prototypes across
    English, Sanskrit, and Tulu.
    Calculates cosine similarities in a shared continuous space.
    """

    def __init__(self, ngram_range: Tuple[int, int] = (2, 4)):
        self.ngram_range = ngram_range
        self.vocabulary: Dict[str, int] = {}
        self.intent_prototypes: Dict[str, Dict[str, float]] = {}
        self.concept_anchors: Dict[str, Dict[str, float]] = {}
        self._initialize_space()

    def _get_ngrams(self, text: str) -> List[str]:
        """Extracts character n-grams from normalized text."""
        clean = f"^{text.lower().strip()}$"
        ngrams = []
        for n in range(self.ngram_range[0], self.ngram_range[1] + 1):
            for i in range(len(clean) - n + 1):
                ngrams.append(clean[i:i+n])
        return ngrams

    def text_to_vector(self, text: str) -> Dict[str, float]:
        """Converts text into an L2-normalized sparse n-gram frequency vector."""
        ngrams = self._get_ngrams(text)
        counts = Counter(ngrams)
        length = math.sqrt(sum(v * v for v in counts.values()))
        if length == 0:
            return {}
        return {k: v / length for k, v in counts.items()}

    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Computes cosine similarity between two sparse unit vectors."""
        if not vec1 or not vec2:
            return 0.0
        # Iterate over the smaller vector
        small, large = (vec1, vec2) if len(vec1) < len(vec2) else (vec2, vec1)
        score = sum(val * large.get(k, 0.0) for k, val in small.items())
        return max(0.0, min(1.0, score))

    def _initialize_space(self):
        """Loads intent exemplars from ontology and computes concept centroid vectors."""
        ontology_path = INTENTS_DIR / "intent_ontology.json"
        if not ontology_path.exists():
            return

        with open(ontology_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data.get("intents", []):
            intent_name = item["name"]
            all_examples = []
            for lang_code, ex_list in item.get("examples", {}).items():
                all_examples.extend(ex_list)

            # Build prototype centroid vector for this intent
            centroid: Dict[str, float] = {}
            for ex in all_examples:
                vec = self.text_to_vector(ex)
                for k, v in vec.items():
                    centroid[k] = centroid.get(k, 0.0) + v

            # Normalize centroid
            norm = math.sqrt(sum(v * v for v in centroid.values()))
            if norm > 0:
                self.intent_prototypes[intent_name] = {k: v / norm for k, v in centroid.items()}

        # Concept Anchors for Section 14 (Semantic Space)
        self.concept_seeds = {
            "FATIGUE": ["i am feeling tired", "अहं श्रान्तः अस्मि", "ಯಾನ್ ಬಚ್ಚೆಲ್ ಉಲ್ಲೆ", "exhausted", "weakness"],
            "DOCTOR": ["doctor", "physician", "चिकित्सकः", "दोಕ್ತೆರ್", "dr", "vaidya"],
            "HOSPITAL": ["hospital", "clinic", "चिकित्सालयः", "ದವಾಖಾನೆ", "dispensary"],
            "HEADACHE": ["headache", "शिरोवेदना", "ತರೆಬೇನೆ", "head pain"],
            "HELP": ["help", "assist", "साहाय्यम्", "ಸಹಾಯ"],
            "TIME": ["time", "timing", "समयः", "ಪೊರ್ತು"],
            "LOCATION": ["where is it", "कुत्र अस्ति", "ವಾಡೆ ಉಂಡು"]
        }

        for concept, examples in self.concept_seeds.items():
            centroid = {}
            for ex in examples:
                vec = self.text_to_vector(ex)
                for k, v in vec.items():
                    centroid[k] = centroid.get(k, 0.0) + v
            norm = math.sqrt(sum(v * v for v in centroid.values()))
            if norm > 0:
                self.concept_anchors[concept] = {k: v / norm for k, v in centroid.items()}

    def find_closest_intent(self, text: str) -> List[Tuple[str, float]]:
        """Computes similarity of text to all intent prototypes."""
        vec = self.text_to_vector(text)
        scores = []
        for intent_name, proto_vec in self.intent_prototypes.items():
            sim = self.cosine_similarity(vec, proto_vec)
            scores.append((intent_name, sim))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def find_closest_concept(self, text: str) -> Optional[Tuple[str, float]]:
        """Identifies underlying semantic concept in multilingual shared space."""
        vec = self.text_to_vector(text)
        best_concept = None
        best_score = 0.0
        for concept, c_vec in self.concept_anchors.items():
            sim = self.cosine_similarity(vec, c_vec)
            if sim > best_score:
                best_score = sim
                best_concept = concept
        if best_concept and best_score >= 0.35:
            return best_concept, best_score
        return None

vector_space = MultilingualSemanticVectorSpace()
