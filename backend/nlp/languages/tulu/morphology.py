import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from backend.config.settings import LEXICONS_DIR

class TuluMorphologicalAnalyzer:
    """
    Morphological and Lexical Analyzer for Tulu.
    Supports both Kannada script and Latin transliteration.
    Follows Dravidian agglutinative morphology for nominal cases, plurals,
    and verbal tense/aspect/mood suffixes.
    Clearly tracks and reports Resource Support Tiers: FULL, PARTIAL, FALLBACK.
    """

    # Tulu Case and Inflection Suffixes (Kannada Script and Latin)
    TULU_SUFFIXES_KANNADA = [
        # Plural + Dative
        ("ಕುಲೆಗ್", {"pos": "NOUN", "number": "plural", "case": "dative"}),
        ("ಗುಲೆಗ್", {"pos": "NOUN", "number": "plural", "case": "dative"}),
        # Plural
        ("ಕುಲು", {"pos": "NOUN", "number": "plural", "case": "nominative"}),
        ("ಗುಲು", {"pos": "NOUN", "number": "plural", "case": "nominative"}),
        # Dative
        ("ರೆಗ್", {"pos": "NOUN", "number": "singular", "case": "dative_honorific"}),
        ("ಲೆಗ್", {"pos": "NOUN", "number": "plural", "case": "dative"}),
        ("ಗ್", {"pos": "NOUN", "number": "singular", "case": "dative"}),
        ("ಕ್", {"pos": "NOUN", "number": "singular", "case": "dative"}),
        # Locative
        ("ಡ್", {"pos": "NOUN", "number": "singular", "case": "locative"}),
        ("ಟ್", {"pos": "NOUN", "number": "singular", "case": "locative"}),
        ("ೊಡು", {"pos": "NOUN", "number": "singular", "case": "locative"}),
        # Genitive
        ("ದ", {"pos": "NOUN", "number": "singular", "case": "genitive"}),
        ("ತ", {"pos": "NOUN", "number": "singular", "case": "genitive"}),
        ("ನ", {"pos": "NOUN", "number": "singular", "case": "genitive"}),
        # Ablative
        ("ಡ್ದ್", {"pos": "NOUN", "number": "singular", "case": "ablative"}),
        ("ರ್ದ್", {"pos": "NOUN", "number": "singular", "case": "ablative"}),
        # Accusative
        ("ರೆನ್", {"pos": "NOUN", "number": "singular", "case": "accusative_honorific"}),
        ("ನ್", {"pos": "NOUN", "number": "singular", "case": "accusative"}),
        # Verb Imperative (Honorific)
        ("ಪುಲೆ", {"pos": "VERB", "mood": "imperative_honorific"}),
        ("ಲೆ", {"pos": "VERB", "mood": "imperative_honorific"}),
        # Verb 3rd Person Neuter Present / Future
        ("ಪುಂಡು", {"pos": "VERB", "tense": "present_habitual", "person": "3rd_neuter"}),
        ("ಉಂಡು", {"pos": "VERB", "tense": "present", "person": "3rd_neuter"}),
        ("ಆಪುಂಡು", {"pos": "VERB", "tense": "future", "person": "3rd_neuter"}),
        # Interrogative marker
        ("ರಾ", {"type": "question_marker"}),
        ("ಡಾ", {"type": "question_marker"}),
        ("ವಾ", {"type": "question_marker"})
    ]

    TULU_SUFFIXES_LATIN = [
        # Plural
        ("kulu", {"pos": "NOUN", "number": "plural", "case": "nominative"}),
        ("gulu", {"pos": "NOUN", "number": "plural", "case": "nominative"}),
        # Dative
        ("ereg", {"pos": "NOUN", "number": "singular", "case": "dative_honorific"}),
        ("leg", {"pos": "NOUN", "number": "plural", "case": "dative"}),
        ("g", {"pos": "NOUN", "number": "singular", "case": "dative"}),
        ("k", {"pos": "NOUN", "number": "singular", "case": "dative"}),
        # Locative
        ("odu", {"pos": "NOUN", "number": "singular", "case": "locative"}),
        ("d", {"pos": "NOUN", "number": "singular", "case": "locative"}),
        ("t", {"pos": "NOUN", "number": "singular", "case": "locative"}),
        # Genitive
        ("da", {"pos": "NOUN", "number": "singular", "case": "genitive"}),
        ("ta", {"pos": "NOUN", "number": "singular", "case": "genitive"}),
        ("na", {"pos": "NOUN", "number": "singular", "case": "genitive"}),
        # Ablative
        ("ddu", {"pos": "NOUN", "number": "singular", "case": "ablative"}),
        # Verb Imperative
        ("pule", {"pos": "VERB", "mood": "imperative_honorific"}),
        ("le", {"pos": "VERB", "mood": "imperative_honorific"}),
        # Verb Neuter
        ("pundu", {"pos": "VERB", "tense": "present_habitual", "person": "3rd_neuter"}),
        ("undu", {"pos": "VERB", "tense": "present", "person": "3rd_neuter"}),
        ("aapundu", {"pos": "VERB", "tense": "future", "person": "3rd_neuter"}),
        # Interrogative
        ("ra", {"type": "question_marker"}),
        ("va", {"type": "question_marker"}),
        ("ya", {"type": "question_marker"}),
        ("a", {"type": "question_marker"})
    ]

    def __init__(self):
        self.lexicon = self._load_lexicon()
        self._build_surface_index()

    def _load_lexicon(self) -> dict:
        lexicon_path = LEXICONS_DIR / "tulu_lexicon.json"
        if lexicon_path.exists():
            with open(lexicon_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"entries": []}

    def _build_surface_index(self):
        self.surface_map: Dict[str, Dict[str, Any]] = {}
        for entry in self.lexicon.get("entries", []):
            for form in entry.get("surface_forms", []):
                norm_form = form.lower()
                self.surface_map[norm_form] = {
                    "lemma": entry.get("lemma"),
                    "pos": entry.get("pos"),
                    "concept": entry.get("concept"),
                    "meaning": entry.get("meaning"),
                    "morphology": entry.get("morphology", {}),
                    "resource_tier": entry.get("resource_tier", "FULL")
                }
                # Also index original case
                self.surface_map[form] = self.surface_map[norm_form]

    def analyze(self, surface_form: str) -> Dict[str, Any]:
        """
        Analyzes a Tulu token in Kannada script or Latin transliteration:
        Surface Form -> Normalized Form -> Lemma -> Semantic Concept -> Grammatical Info.
        """
        clean_lower = surface_form.lower().strip()

        # 1. Exact match in Tulu Lexicon (Tier: FULL SUPPORT)
        if clean_lower in self.surface_map:
            data = self.surface_map[clean_lower]
            return {
                "surface_form": surface_form,
                "normalized_form": clean_lower,
                "lemma": data["lemma"],
                "pos": data["pos"],
                "morphology": data["morphology"],
                "concept": data["concept"],
                "confidence": 0.96,
                "resource_tier": data.get("resource_tier", "FULL")
            }

        if surface_form in self.surface_map:
            data = self.surface_map[surface_form]
            return {
                "surface_form": surface_form,
                "normalized_form": clean_lower,
                "lemma": data["lemma"],
                "pos": data["pos"],
                "morphology": data["morphology"],
                "concept": data["concept"],
                "confidence": 0.96,
                "resource_tier": data.get("resource_tier", "FULL")
            }

        # 2. Rule-based Suffix Stemming (Tier: PARTIAL SUPPORT)
        # Check Kannada script suffixes
        for suffix, morph_info in self.TULU_SUFFIXES_KANNADA:
            if surface_form.endswith(suffix) and len(surface_form) > len(suffix) + 1:
                stem = surface_form[:-len(suffix)]
                # Check if stem is in lexicon
                if stem in self.surface_map or stem.lower() in self.surface_map:
                    entry = self.surface_map.get(stem) or self.surface_map.get(stem.lower())
                    return {
                        "surface_form": surface_form,
                        "normalized_form": clean_lower,
                        "lemma": entry["lemma"],
                        "pos": morph_info.get("pos", entry.get("pos", "NOUN")),
                        "morphology": {**entry.get("morphology", {}), **morph_info},
                        "concept": entry["concept"],
                        "confidence": 0.88,
                        "resource_tier": "PARTIAL"
                    }
                # Even if stem not in small lexicon, return grammatical analysis
                return {
                    "surface_form": surface_form,
                    "normalized_form": clean_lower,
                    "lemma": stem,
                    "pos": morph_info.get("pos", "NOUN"),
                    "morphology": morph_info,
                    "concept": None,
                    "confidence": 0.75,
                    "resource_tier": "PARTIAL"
                }

        # Check Latin script suffixes
        for suffix, morph_info in self.TULU_SUFFIXES_LATIN:
            if clean_lower.endswith(suffix) and len(clean_lower) > len(suffix) + 1:
                stem = clean_lower[:-len(suffix)]
                if stem in self.surface_map:
                    entry = self.surface_map[stem]
                    return {
                        "surface_form": surface_form,
                        "normalized_form": clean_lower,
                        "lemma": entry["lemma"],
                        "pos": morph_info.get("pos", entry.get("pos", "NOUN")),
                        "morphology": {**entry.get("morphology", {}), **morph_info},
                        "concept": entry["concept"],
                        "confidence": 0.85,
                        "resource_tier": "PARTIAL"
                    }
                return {
                    "surface_form": surface_form,
                    "normalized_form": clean_lower,
                    "lemma": stem,
                    "pos": morph_info.get("pos", "NOUN"),
                    "morphology": morph_info,
                    "concept": None,
                    "confidence": 0.70,
                    "resource_tier": "PARTIAL"
                }

        # 3. Fallback Support (Tier: FALLBACK SUPPORT)
        return {
            "surface_form": surface_form,
            "normalized_form": clean_lower,
            "lemma": clean_lower,
            "pos": "NOUN",
            "morphology": {"unknown": True},
            "concept": None,
            "confidence": 0.45,
            "resource_tier": "FALLBACK"
        }

tulu_morphology = TuluMorphologicalAnalyzer()
