from typing import List, Dict, Any
from backend.nlp.languages.sanskrit.morphology import sa_morphology
from backend.nlp.languages.tulu.morphology import tulu_morphology
from backend.nlp.languages.english.morphology import en_morphology

class MultilingualPOSTagger:
    """
    Multilingual Part-of-Speech Tagger.
    Assigns universal POS tags:
    NOUN, VERB, ADJECTIVE, ADVERB, PRONOUN, PREPOSITION/PARTICLE,
    CONJUNCTION, DETERMINER, INTERJECTION, PROPER_NOUN, NUMBER.
    Delegates to language-specific morphological analyzers and contextual rules.
    """

    ENGLISH_DETERMINERS = {"the", "a", "an", "this", "that", "these", "those", "each", "every", "some", "any"}
    ENGLISH_PREPOSITIONS = {"in", "on", "at", "to", "for", "from", "with", "by", "about", "into", "through", "over", "before", "after"}
    ENGLISH_CONJUNCTIONS = {"and", "but", "or", "so", "because", "although", "while", "if", "unless"}
    ENGLISH_PRONOUNS = {"i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them", "my", "your", "his", "their", "our", "what", "which", "who", "whom", "whose"}
    ENGLISH_INTERJECTIONS = {"hello", "hi", "hey", "oh", "wow", "please", "thanks", "bye", "goodbye", "yes", "no"}

    def tag_token(self, token_dict: Dict[str, Any], lang: str) -> Dict[str, Any]:
        """Tags a single token given its dictionary representation and language code."""
        surface = token_dict.get("surface_form", "")
        tok_type = token_dict.get("token_type", "WORD")
        norm = token_dict.get("normalized_form", surface).lower()

        # Numbers
        if tok_type == "NUMBER" or surface.isdigit():
            return {"pos": "NUMBER", "confidence": 1.0}

        # Punctuation
        if tok_type in ("PUNCT", "DANDA"):
            return {"pos": "PUNCTUATION", "confidence": 1.0}

        # URLs
        if tok_type == "URL":
            return {"pos": "URL", "confidence": 1.0}

        # Language-specific morphological taggers
        if lang == "sa":
            analysis = sa_morphology.analyze(surface)
            return {
                "pos": analysis["pos"],
                "lemma": analysis["lemma"],
                "morphology": analysis["morphology"],
                "concept": analysis["concept"],
                "confidence": analysis["confidence"],
                "sandhi_components": analysis.get("sandhi_components", [])
            }

        elif lang == "tcy":
            analysis = tulu_morphology.analyze(surface)
            return {
                "pos": analysis["pos"],
                "lemma": analysis["lemma"],
                "morphology": analysis["morphology"],
                "concept": analysis["concept"],
                "confidence": analysis["confidence"],
                "resource_tier": analysis.get("resource_tier", "PARTIAL")
            }

        else:
            # English / Latin fallback
            if norm in self.ENGLISH_DETERMINERS:
                return {"pos": "DETERMINER", "lemma": norm, "confidence": 0.98}
            if norm in self.ENGLISH_PREPOSITIONS:
                return {"pos": "PREPOSITION/PARTICLE", "lemma": norm, "confidence": 0.98}
            if norm in self.ENGLISH_CONJUNCTIONS:
                return {"pos": "CONJUNCTION", "lemma": norm, "confidence": 0.98}
            if norm in self.ENGLISH_PRONOUNS:
                return {"pos": "PRONOUN", "lemma": norm, "confidence": 0.98}
            if norm in self.ENGLISH_INTERJECTIONS:
                return {"pos": "INTERJECTION", "lemma": norm, "confidence": 0.98}

            analysis = en_morphology.analyze(surface)
            return {
                "pos": analysis["pos"],
                "lemma": analysis["lemma"],
                "morphology": analysis.get("morphology", {}),
                "concept": analysis.get("concept"),
                "confidence": analysis["confidence"]
            }

    def tag_tokens(self, tokens: List[Dict[str, Any]], lang: str) -> List[Dict[str, Any]]:
        """Tags an entire list of tokens."""
        tagged = []
        for tok in tokens:
            tag_info = self.tag_token(tok, lang)
            merged = {**tok, **tag_info}
            tagged.append(merged)
        return tagged

pos_tagger = MultilingualPOSTagger()
