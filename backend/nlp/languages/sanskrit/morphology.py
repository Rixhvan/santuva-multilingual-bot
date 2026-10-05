import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from backend.config.settings import LEXICONS_DIR
from backend.nlp.languages.sanskrit.sandhi import sandhi_engine

class SanskritMorphologicalAnalyzer:
    """
    Morphological and Lexical Analyzer for Sanskrit.
    Maps surface forms to lemmas, grammatical cases, genders, numbers,
    verb tenses (lakaras), persons, and semantic concepts.
    """

    def __init__(self):
        self.lexicon = self._load_lexicon()
        self._build_surface_index()

    def _load_lexicon(self) -> dict:
        lexicon_path = LEXICONS_DIR / "sanskrit_lexicon.json"
        if lexicon_path.exists():
            with open(lexicon_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"entries": []}

    def _build_surface_index(self):
        self.surface_map: Dict[str, Dict[str, Any]] = {}
        for entry in self.lexicon.get("entries", []):
            for form in entry.get("surface_forms", []):
                self.surface_map[form] = {
                    "lemma": entry.get("lemma"),
                    "pos": entry.get("pos"),
                    "concept": entry.get("concept"),
                    "meaning": entry.get("meaning"),
                    "morphology": entry.get("morphology", {})
                }

    # Inflection patterns for masculine a-stem nouns (e.g. राम, चिकित्सक, चिकित्सालय, वैद्य, सूर्य)
    MASCULINE_A_STEM_SUFFIXES = [
        ("स्य", {"case": "genitive", "number": "singular", "gender": "masculine"}),
        ("ेण", {"case": "instrumental", "number": "singular", "gender": "masculine"}),
        ("ाय", {"case": "dative", "number": "singular", "gender": "masculine"}),
        ("ात्", {"case": "ablative", "number": "singular", "gender": "masculine"}),
        ("ेभ्यः", {"case": "dative_ablative", "number": "plural", "gender": "masculine"}),
        ("ाणाम्", {"case": "genitive", "number": "plural", "gender": "masculine"}),
        ("ेषु", {"case": "locative", "number": "plural", "gender": "masculine"}),
        ("ान्", {"case": "accusative", "number": "plural", "gender": "masculine"}),
        ("ैः", {"case": "instrumental", "number": "plural", "gender": "masculine"}),
        ("म्", {"case": "accusative", "number": "singular", "gender": "masculine"}),
        ("ः", {"case": "nominative", "number": "singular", "gender": "masculine"}),
        ("े", {"case": "locative", "number": "singular", "gender": "masculine"}),
        ("ौ", {"case": "nominative_accusative", "number": "dual", "gender": "masculine"}),
        ("ाः", {"case": "nominative", "number": "plural", "gender": "masculine"}),
    ]

    # Verb conjugations for Lat Lakara (present tense) & Lot (imperative) & Lrt (future)
    VERB_SUFFIXES = [
        ("िष्यति", {"tense": "future", "lakara": "lrt", "person": "3rd", "number": "singular"}),
        ("िष्यामि", {"tense": "future", "lakara": "lrt", "person": "1st", "number": "singular"}),
        ("िष्यन्ति", {"tense": "future", "lakara": "lrt", "person": "3rd", "number": "plural"}),
        ("तुम्", {"type": "infinitive", "tense": "invariable"}),
        ("तु", {"mood": "imperative", "lakara": "lot", "person": "3rd", "number": "singular"}),
        ("ताम्", {"mood": "imperative", "lakara": "lot", "person": "3rd", "number": "dual"}),
        ("न्तु", {"mood": "imperative", "lakara": "lot", "person": "3rd", "number": "plural"}),
        ("न्ति", {"tense": "present", "lakara": "lat", "person": "3rd", "number": "plural"}),
        ("तः", {"tense": "present", "lakara": "lat", "person": "3rd", "number": "dual"}),
        ("ति", {"tense": "present", "lakara": "lat", "person": "3rd", "number": "singular"}),
        ("थः", {"tense": "present", "lakara": "lat", "person": "2nd", "number": "dual"}),
        ("थ", {"tense": "present", "lakara": "lat", "person": "2nd", "number": "plural"}),
        ("सि", {"tense": "present", "lakara": "lat", "person": "2nd", "number": "singular"}),
        ("ामः", {"tense": "present", "lakara": "lat", "person": "1st", "number": "plural"}),
        ("ावः", {"tense": "present", "lakara": "lat", "person": "1st", "number": "dual"}),
        ("ामि", {"tense": "present", "lakara": "lat", "person": "1st", "number": "singular"}),
    ]

    def analyze(self, surface_form: str) -> Dict[str, Any]:
        """
        Analyzes a Sanskrit token:
        Surface Form -> Lemma -> Morphological Features -> Semantic Concept.
        Returns dict with lemma, pos, morphology, concept, confidence, and sandhi components.
        """
        # 1. Exact match in lexicon
        if surface_form in self.surface_map:
            data = self.surface_map[surface_form]
            morph = dict(data["morphology"])
            # If the surface form specifies case directly
            for suffix, m_info in self.MASCULINE_A_STEM_SUFFIXES:
                if surface_form.endswith(suffix):
                    morph.update(m_info)
                    break

            # Check if this word also has sandhi decomposition
            sandhi_item = sandhi_engine.analyze_word(surface_form)
            sandhi_comps = sandhi_item.components if sandhi_item else []
            lemma = "सूर्योदय" if surface_form in ("सूर्योदयः", "सूर्योदय") else data["lemma"]

            return {
                "surface_form": surface_form,
                "lemma": lemma,
                "pos": data["pos"],
                "morphology": morph,
                "concept": data["concept"],
                "confidence": 0.98,
                "sandhi_components": sandhi_comps
            }

        # 2. Check Sandhi engine
        sandhi_item = sandhi_engine.analyze_word(surface_form)
        if sandhi_item:
            # Check if second component or compound gives concept
            concept = None
            pos = "NOUN"
            lemma = sandhi_item.components[0]
            if surface_form == "सूर्योदयः" or surface_form == "सूर्योदय":
                concept = "SUNRISE"
                lemma = "सूर्योदय"
            elif "चिकित्सालय" in surface_form:
                concept = "HOSPITAL"
                lemma = "चिकित्सालय"
            elif "शिरोवेदना" in surface_form:
                concept = "PAIN"
                lemma = "शिरोवेदना"
            elif "नमस्ते" in surface_form:
                concept = "GREETING"
                lemma = "नमस्ते"
                pos = "INTERJECTION"

            return {
                "surface_form": surface_form,
                "lemma": lemma,
                "pos": pos,
                "morphology": {"compound": True, "components": sandhi_item.components, "rule": sandhi_item.rule_type},
                "concept": concept or "COMPOUND",
                "confidence": sandhi_item.confidence,
                "sandhi_components": sandhi_item.components
            }

        # 3. Rule-based Noun Paradigm Stripping (e.g. रामस्य -> राम + स्य)
        for suffix, morph_info in self.MASCULINE_A_STEM_SUFFIXES:
            if surface_form.endswith(suffix) and len(surface_form) > len(suffix):
                stem = surface_form[:-len(suffix)]
                # Check if stem is known or matches a known lemma
                if stem in ["राम", "चिकित्सक", "चिकित्सालय", "वैद्य", "सूर्य", "समय", "मार्ग", "रोग", "औषध"]:
                    return {
                        "surface_form": surface_form,
                        "lemma": stem,
                        "pos": "PROPER_NOUN" if stem == "राम" else "NOUN",
                        "morphology": morph_info,
                        "concept": self._lookup_stem_concept(stem),
                        "confidence": 0.95,
                        "sandhi_components": []
                    }

        # 4. Rule-based Verb Paradigm Stripping (e.g. गमिष्यामि, वदामि, इच्छामि)
        for suffix, verb_info in self.VERB_SUFFIXES:
            if surface_form.endswith(suffix) and len(surface_form) > len(suffix):
                v_stem = surface_form[:-len(suffix)]
                return {
                    "surface_form": surface_form,
                    "lemma": v_stem,
                    "pos": "VERB",
                    "morphology": verb_info,
                    "concept": "ACTION",
                    "confidence": 0.85,
                    "sandhi_components": []
                }

        # 5. Unknown or unanalyzable - do NOT fabricate confident grammar
        return {
            "surface_form": surface_form,
            "lemma": surface_form,
            "pos": "NOUN",
            "morphology": {"unknown": True},
            "concept": None,
            "confidence": 0.45,
            "sandhi_components": []
        }

    def _lookup_stem_concept(self, stem: str) -> Optional[str]:
        concept_map = {
            "राम": "PERSON_RAMA",
            "चिकित्सक": "DOCTOR",
            "चिकित्सालय": "HOSPITAL",
            "वैद्य": "DOCTOR",
            "सूर्य": "SUNRISE",
            "समय": "TIME",
            "रोग": "DISEASE",
            "औषध": "MEDICINE"
        }
        return concept_map.get(stem)

sa_morphology = SanskritMorphologicalAnalyzer()
