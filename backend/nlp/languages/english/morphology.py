import json
import re
from pathlib import Path
from typing import Dict, Any, Optional
from backend.config.settings import LEXICONS_DIR

class EnglishMorphologicalAnalyzer:
    """
    Morphological and Lexical Analyzer for English.
    Handles irregular verbs, noun pluralization, inflectional suffixes,
    and maps surface forms to lemmas, POS tags, and semantic concepts.
    """

    IRREGULAR_LEMMAS = {
        "is": ("be", "VERB", {"tense": "present", "person": "3rd", "number": "singular"}),
        "are": ("be", "VERB", {"tense": "present", "number": "plural"}),
        "am": ("be", "VERB", {"tense": "present", "person": "1st", "number": "singular"}),
        "was": ("be", "VERB", {"tense": "past", "number": "singular"}),
        "were": ("be", "VERB", {"tense": "past", "number": "plural"}),
        "been": ("be", "VERB", {"tense": "past_participle"}),
        "being": ("be", "VERB", {"tense": "present_participle"}),
        "has": ("have", "VERB", {"tense": "present", "person": "3rd"}),
        "have": ("have", "VERB", {"tense": "present"}),
        "had": ("have", "VERB", {"tense": "past"}),
        "does": ("do", "VERB", {"tense": "present", "person": "3rd"}),
        "did": ("do", "VERB", {"tense": "past"}),
        "done": ("do", "VERB", {"tense": "past_participle"}),
        "feels": ("feel", "VERB", {"tense": "present"}),
        "feeling": ("feel", "VERB", {"tense": "present_participle"}),
        "felt": ("feel", "VERB", {"tense": "past"}),
        "sees": ("see", "VERB", {"tense": "present"}),
        "seeing": ("see", "VERB", {"tense": "present_participle"}),
        "saw": ("see", "VERB", {"tense": "past"}),
        "seen": ("see", "VERB", {"tense": "past_participle"}),
        "comes": ("come", "VERB", {"tense": "present"}),
        "coming": ("come", "VERB", {"tense": "present_participle"}),
        "came": ("come", "VERB", {"tense": "past"}),
        "goes": ("go", "VERB", {"tense": "present"}),
        "going": ("go", "VERB", {"tense": "present_participle"}),
        "went": ("go", "VERB", {"tense": "past"}),
        "gone": ("go", "VERB", {"tense": "past_participle"}),
        "tells": ("tell", "VERB", {"tense": "present"}),
        "telling": ("tell", "VERB", {"tense": "present_participle"}),
        "told": ("tell", "VERB", {"tense": "past"}),
        "me": ("i", "PRONOUN", {"case": "objective", "number": "singular"}),
        "my": ("i", "PRONOUN", {"case": "possessive", "number": "singular"}),
        "myself": ("i", "PRONOUN", {"case": "reflexive"}),
        "your": ("you", "PRONOUN", {"case": "possessive"}),
        "yours": ("you", "PRONOUN", {"case": "possessive"}),
        "yourself": ("you", "PRONOUN", {"case": "reflexive"}),
        "his": ("he", "PRONOUN", {"case": "possessive"}),
        "him": ("he", "PRONOUN", {"case": "objective"}),
        "her": ("she", "PRONOUN", {"case": "objective_possessive"}),
        "their": ("they", "PRONOUN", {"case": "possessive"}),
        "them": ("they", "PRONOUN", {"case": "objective"}),
        "us": ("we", "PRONOUN", {"case": "objective"}),
        "our": ("we", "PRONOUN", {"case": "possessive"})
    }

    def __init__(self):
        self.lexicon = self._load_lexicon()
        self._build_surface_index()

    def _load_lexicon(self) -> dict:
        lexicon_path = LEXICONS_DIR / "english_lexicon.json"
        if lexicon_path.exists():
            with open(lexicon_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"entries": []}

    def _build_surface_index(self):
        self.surface_map: Dict[str, Dict[str, Any]] = {}
        for entry in self.lexicon.get("entries", []):
            for form in entry.get("surface_forms", []):
                norm = form.lower()
                self.surface_map[norm] = {
                    "lemma": entry.get("lemma"),
                    "pos": entry.get("pos"),
                    "concept": entry.get("concept"),
                    "meaning": entry.get("meaning")
                }

    def analyze(self, surface_form: str) -> Dict[str, Any]:
        """Analyzes an English surface word form."""
        lower = surface_form.lower().strip()

        # 1. Check irregular tables
        if lower in self.IRREGULAR_LEMMAS:
            lemma, pos, morph = self.IRREGULAR_LEMMAS[lower]
            concept = self.surface_map.get(lemma, {}).get("concept")
            return {
                "surface_form": surface_form,
                "normalized_form": lower,
                "lemma": lemma,
                "pos": pos,
                "morphology": morph,
                "concept": concept,
                "confidence": 0.98
            }

        # 2. Check Lexicon
        if lower in self.surface_map:
            data = self.surface_map[lower]
            return {
                "surface_form": surface_form,
                "normalized_form": lower,
                "lemma": data["lemma"],
                "pos": data["pos"],
                "morphology": {},
                "concept": data["concept"],
                "confidence": 0.95
            }

        # 3. Rule-based inflection stripping
        # Plural -ies -> -y
        if lower.endswith("ies") and len(lower) > 4:
            stem = lower[:-3] + "y"
            return {
                "surface_form": surface_form,
                "normalized_form": lower,
                "lemma": stem,
                "pos": "NOUN",
                "morphology": {"number": "plural"},
                "concept": self.surface_map.get(stem, {}).get("concept"),
                "confidence": 0.90
            }

        # Plural -es / -s
        if lower.endswith("es") and len(lower) > 3:
            stem = lower[:-2]
            return {
                "surface_form": surface_form,
                "normalized_form": lower,
                "lemma": stem,
                "pos": "NOUN",
                "morphology": {"number": "plural"},
                "concept": self.surface_map.get(stem, {}).get("concept"),
                "confidence": 0.90
            }
        elif lower.endswith("s") and not lower.endswith("ss") and len(lower) > 2:
            stem = lower[:-1]
            return {
                "surface_form": surface_form,
                "normalized_form": lower,
                "lemma": stem,
                "pos": "NOUN",
                "morphology": {"number": "plural"},
                "concept": self.surface_map.get(stem, {}).get("concept"),
                "confidence": 0.90
            }

        # Verbal -ing
        if lower.endswith("ing") and len(lower) > 4:
            stem = lower[:-3]
            return {
                "surface_form": surface_form,
                "normalized_form": lower,
                "lemma": stem,
                "pos": "VERB",
                "morphology": {"aspect": "progressive"},
                "concept": self.surface_map.get(stem, {}).get("concept"),
                "confidence": 0.88
            }

        # Verbal -ed
        if lower.endswith("ed") and len(lower) > 3:
            stem = lower[:-2]
            return {
                "surface_form": surface_form,
                "normalized_form": lower,
                "lemma": stem,
                "pos": "VERB",
                "morphology": {"tense": "past"},
                "concept": self.surface_map.get(stem, {}).get("concept"),
                "confidence": 0.88
            }

        return {
            "surface_form": surface_form,
            "normalized_form": lower,
            "lemma": lower,
            "pos": "NOUN",
            "morphology": {},
            "concept": None,
            "confidence": 0.50
        }

en_morphology = EnglishMorphologicalAnalyzer()
