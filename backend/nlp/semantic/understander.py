from typing import List, Dict, Any, Optional
from backend.models.schemas import SemanticRepresentation, EntityInfo, IntentInfo
from backend.nlp.embeddings.vector_space import vector_space

class MultilingualSemanticUnderstander:
    """
    Transforms lexical, syntactic, and morphological analysis into a structured,
    language-independent semantic representation.
    Extracts Dialogue Act, Intent, Entities, and Shared Semantic Concepts.
    """

    QUESTION_WORDS = {
        "what", "where", "when", "why", "who", "which", "how", "is", "can", "could", "do",
        "कुत्र", "कदा", "कथम्", "किम्", "कः", "का", "किं", "कति",
        "ದಾನೆ", "ಎಂಚ", "ಒವ್ವು", "ವಾಡೆ", "ಏರ್", "ಏಪ", "ಉಂಡಾ", "ಬೋಡಾ",
        "daane", "encha", "ovvu", "vaade", "er", "aepa", "unda", "boda", "idiya"
    }

    IMPERATIVE_WORDS = {
        "please", "tell", "show", "give", "help",
        "वदतु", "कथयतु", "पश्यतु", "कुरु", "भवतु",
        "ದಯಮಲ್ತ್", "ಪಣ್ಲೆ", "ತೂಲೆ", "ಮಲ್ಪುಲೆ", "ಕೊರ್ಲೆ",
        "dayamalth", "panle", "toole", "malpule", "korle"
    }

    def determine_dialogue_act(self, text: str, intent: str, tokens: List[Dict[str, Any]]) -> str:
        """Determines the communicative dialogue act of the utterance."""
        clean = text.strip()
        words_lower = [t.get("normalized_form", t.get("surface_form", "")).lower() for t in tokens]

        if intent in ("GREETING", "FAREWELL"):
            return intent
        if intent in ("YES", "CONFIRMATION"):
            return "AFFIRMATION"
        if intent in ("NO", "DENIAL"):
            return "NEGATION"
        if intent == "EMERGENCY":
            return "DIRECTIVE"

        # Check question punctuation or question words
        if clean.endswith("?") or any(w in self.QUESTION_WORDS for w in words_lower):
            return "QUESTION"

        # Check imperative
        if any(w in self.IMPERATIVE_WORDS for w in words_lower) or intent in ("REQUEST", "HELP"):
            return "DIRECTIVE"

        return "STATEMENT"

    def build_semantic_representation(
        self,
        text: str,
        lang_name: str,
        intent_info: IntentInfo,
        entities: List[EntityInfo],
        tokens: List[Dict[str, Any]]
    ) -> SemanticRepresentation:
        """Generates the unified semantic representation."""
        dialogue_act = self.determine_dialogue_act(text, intent_info.intent, tokens)

        # Entity dictionary formatting
        entity_dict: Dict[str, Any] = {}
        for ent in entities:
            key = ent.label.lower()
            if key not in entity_dict:
                entity_dict[key] = ent.text
            else:
                if isinstance(entity_dict[key], list):
                    entity_dict[key].append(ent.text)
                else:
                    entity_dict[key] = [entity_dict[key], ent.text]

        # Check cross-lingual concept anchors (Section 14)
        concept_match = vector_space.find_closest_concept(text)
        shared_concept = concept_match[0] if concept_match else None

        # Token-level concepts
        token_concepts = [t.get("concept") for t in tokens if t.get("concept")]

        return SemanticRepresentation(
            language=lang_name,
            intent=intent_info.intent,
            entities=entity_dict,
            dialogue_act=dialogue_act,
            concepts=list(set(token_concepts)),
            confidence=intent_info.confidence,
            shared_concept_id=shared_concept
        )

semantic_understander = MultilingualSemanticUnderstander()
