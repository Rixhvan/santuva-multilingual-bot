import re
from typing import List, Dict, Any, Optional
from backend.models.schemas import SandhiSplittingItem

class SanskritSandhiEngine:
    """
    Classical Sanskrit Sandhi Analysis and Splitting Engine.
    Handles Dirgha, Guna, Vriddhi, Yan, Visarga, and Anusvara Sandhi,
    as well as known classical compound expressions.
    """

    # Known classical compounds and sandhied words with exact decomposition
    KNOWN_COMPOUNDS = {
        "सूर्योदयः": {
            "components": ["सूर्य", "उदयः"],
            "rule": "guna_sandhi (a + u -> o)",
            "meaning": "sunrise",
            "confidence": 0.98
        },
        "सूर्योदय": {
            "components": ["सूर्य", "उदय"],
            "rule": "guna_sandhi (a + u -> o)",
            "meaning": "sunrise",
            "confidence": 0.98
        },
        "चिकित्सालयः": {
            "components": ["चिकित्सा", "आलयः"],
            "rule": "dirgha_sandhi (ā + ā -> ā)",
            "meaning": "hospital (abode of treatment)",
            "confidence": 0.98
        },
        "चिकित्सालय": {
            "components": ["चिकित्सा", "आलय"],
            "rule": "dirgha_sandhi (ā + ā -> ā)",
            "meaning": "hospital",
            "confidence": 0.98
        },
        "विद्यालयः": {
            "components": ["विद्या", "आलयः"],
            "rule": "dirgha_sandhi (ā + ā -> ā)",
            "meaning": "school / temple of learning",
            "confidence": 0.98
        },
        "शिरोवेदना": {
            "components": ["शिरस्", "वेदना"],
            "rule": "visarga_sandhi (as -> o before voiced cons)",
            "meaning": "headache",
            "confidence": 0.95
        },
        "उदरवेदना": {
            "components": ["उदर", "वेदना"],
            "rule": "tatpurusha_compound",
            "meaning": "stomach pain",
            "confidence": 0.95
        },
        "नमस्ते": {
            "components": ["नमः", "ते"],
            "rule": "visarga_sandhi (ḥ + t -> st)",
            "meaning": "salutations to you",
            "confidence": 0.99
        },
        "रामोऽस्ति": {
            "components": ["रामः", "अस्ति"],
            "rule": "visarga_avagraha (aḥ + a -> o' + avagraha)",
            "meaning": "Rama exists / is",
            "confidence": 0.99
        },
        "कृतज्ञोऽस्मि": {
            "components": ["कृतज्ञः", "अस्मि"],
            "rule": "visarga_avagraha (aḥ + a -> o' + avagraha)",
            "meaning": "I am grateful",
            "confidence": 0.98
        },
        "पुनर्मिलामः": {
            "components": ["पुनः", "मिलामः"],
            "rule": "visarga_rutva (ḥ -> r before m)",
            "meaning": "we meet again",
            "confidence": 0.98
        },
        "इत्याह": {
            "components": ["इति", "आह"],
            "rule": "yan_sandhi (i + ā -> yā)",
            "meaning": "thus spoke",
            "confidence": 0.95
        },
        "नास्ति": {
            "components": ["न", "अस्ति"],
            "rule": "dirgha_sandhi (a + a -> ā)",
            "meaning": "is not / does not exist",
            "confidence": 0.98
        },
        "महौषधम्": {
            "components": ["महा", "औषधम्"],
            "rule": "vriddhi_sandhi (ā + au -> au)",
            "meaning": "great medicine",
            "confidence": 0.95
        }
    }

    # Common Sanskrit noun roots for morphological validation during heuristic split
    KNOWN_ROOTS = {
        "सूर्य", "चन्द्र", "चिकित्सा", "आलय", "विद्या", "गृह", "राम", "शिव", 
        "महा", "औषध", "वेद", "शास्त्र", "ज्ञान", "पुत्र", "नर", "देव", "राज",
        "मार्ग", "समय", "रोग", "शिरस्", "उदर", "वेदना", "सुख", "दुःख", "प्राण"
    }

    def analyze_word(self, word: str) -> Optional[SandhiSplittingItem]:
        """
        Attempts to segment a word into its underlying sandhi / compound constituents.
        Returns a SandhiSplittingItem with components, rule type, and confidence.
        """
        # 1. Exact match in classical compounds
        if word in self.KNOWN_COMPOUNDS:
            item = self.KNOWN_COMPOUNDS[word]
            return SandhiSplittingItem(
                compound=word,
                components=item["components"],
                rule_type=item["rule"],
                confidence=item["confidence"],
                meaning=item.get("meaning")
            )

        # 2. Avagraha Sandhi (e.g. word contains 'ऽ')
        if "ऽ" in word:
            parts = word.split("ऽ")
            if len(parts) == 2:
                prefix = parts[0]
                suffix = parts[1]
                # If prefix ends with 'ो', base word ended with 'ः'
                if prefix.endswith("ो"):
                    first_root = prefix[:-1] + "ः"
                else:
                    first_root = prefix
                second_root = "अ" + suffix
                return SandhiSplittingItem(
                    compound=word,
                    components=[first_root, second_root],
                    rule_type="visarga_avagraha_sandhi",
                    confidence=0.92,
                    meaning=f"{first_root} + {second_root}"
                )

        # 3. Rule-based Guṇa Sandhi heuristic (e.g., contains 'ो' medial)
        # e.g., 'सूर्य' + 'उदय' = 'सूर्योदय'
        if "ो" in word:
            idx = word.find("ो")
            if 1 < idx < len(word) - 1:
                left = word[:idx]
                right = word[idx+1:]
                # Check if left is a known root or valid stem
                possible_left = left
                possible_right = "उ" + right
                if possible_left in self.KNOWN_ROOTS:
                    return SandhiSplittingItem(
                        compound=word,
                        components=[possible_left, possible_right],
                        rule_type="guna_sandhi (a + u -> o)",
                        confidence=0.85,
                        meaning=f"{possible_left} + {possible_right}"
                    )

        # 4. Rule-based Dīrgha Sandhi heuristic (contains 'ा' medial)
        # e.g., 'विद्यालय' -> 'विद्या' + 'आलय'
        if "ा" in word:
            idx = word.find("ा")
            if 1 < idx < len(word) - 1:
                left = word[:idx]
                right = word[idx+1:]
                # Test possible splits
                candidate_1 = left + "ा"
                candidate_2 = "आ" + right
                if candidate_1 in self.KNOWN_ROOTS or "आलय" in candidate_2:
                    return SandhiSplittingItem(
                        compound=word,
                        components=[candidate_1, candidate_2],
                        rule_type="dirgha_sandhi (ā + ā -> ā)",
                        confidence=0.80,
                        meaning=f"{candidate_1} + {candidate_2}"
                    )

        return None

    def process_sentence(self, tokens: List[str]) -> List[SandhiSplittingItem]:
        """Analyzes all tokens in a sentence for sandhi compounds."""
        results = []
        for tok in tokens:
            analysis = self.analyze_word(tok)
            if analysis:
                results.append(analysis)
        return results

sandhi_engine = SanskritSandhiEngine()
