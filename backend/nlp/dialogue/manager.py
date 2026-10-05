from typing import Dict, Any, Optional, Tuple
from backend.models.schemas import DialogueState, LanguageInfo, IntentInfo, EntityInfo
from backend.nlp.dialogue.memory import conversation_memory
from backend.config.settings import settings

class DialogueManager:
    """
    Dialogue State Manager.
    Tracks conversational flow, handles context-sensitive follow-ups,
    anaphora resolution, explicit language-switching directives,
    and ambiguity mitigation.
    """

    # Language Switch Directives
    LANG_SWITCH_DIRECTIVES = {
        "sa": ["संस्कृतेन", "संस्कृतभाषायां", "संस्कृतम्", "speak in sanskrit", "talk in sanskrit"],
        "en": ["english", "in english", "speak in english", "talk in english", "ಆಂಗ್ಲ"],
        "tcy": ["ತುಳುಟು", "ತುಳು", "tulu", "in tulu", "speak in tulu", "tcy"]
    }

    def detect_language_switch_request(self, text: str) -> Optional[str]:
        """Detects if user explicitly commanded the chatbot to switch languages."""
        text_lower = text.lower()
        for lang_code, triggers in self.LANG_SWITCH_DIRECTIVES.items():
            for trigger in triggers:
                if trigger in text_lower or trigger in text:
                    return lang_code
        return None

    def process_turn(
        self,
        session_id: str,
        text: str,
        lang_info: LanguageInfo,
        intent_info: IntentInfo,
        entities: list[EntityInfo]
    ) -> Tuple[DialogueState, bool, Optional[str], Optional[str]]:
        """
        Processes conversational context.
        Returns: (dialogue_state, requires_clarification, clarification_prompt, target_topic)
        """
        state = conversation_memory.get_or_create_state(session_id)

        # 1. Check explicit language switch directive
        switch_lang = self.detect_language_switch_request(text)
        if switch_lang:
            target_lang = settings.language_names.get(switch_lang, lang_info.language)
            lang_info.language = target_lang
            lang_info.language_code = switch_lang

        # 2. Check for ambiguous pronouns (Section 21)
        resolved_text, was_resolved, antecedent = conversation_memory.resolve_anaphora(text, session_id)
        if ("about it" in text.lower() or "tell me about it" in text.lower() or "तस्य विषये" in text or "ಅಯಿತ್ತ ಬಗ್ಗೆ" in text) and not antecedent:
            # Ambiguity: user said "it" without any antecedent
            state.clarification_pending = True
            lang_code = lang_info.language_code
            if lang_code == "sa":
                clarification = "कृपया कस्य विषये पृच्छसि इति स्पष्टं कुरु।"
            elif lang_code == "tcy":
                clarification = "ಈರ್ ಒವ್ವೆನ ಬಗ್ಗೆ ಕೇಣೊಂದುಲ್ಲೆರ್ ಪಂಡ್ದ್ ದಯಮಲ್ತ್ ಪಣ್ಲೆ।"
            else:
                clarification = "Could you please tell me what you are referring to?"
            return state, True, clarification, None

        # 3. Check for low confidence / unknown intent clarification
        if intent_info.intent == "UNKNOWN" or intent_info.confidence < settings.clarification_threshold:
            state.clarification_pending = True
            lang_code = lang_info.language_code
            if lang_code == "sa":
                clarification = "क्षम्यताम्, अहं सम्यक् न अवगच्छम्। कृपया पुनः स्पष्टतया वदतु।"
            elif lang_code == "tcy":
                clarification = "ಎಂಕ್ ಸರಿಯಾದ್ ಅರ್ಥ ಆಯಿಜಿ. ದಯಮಲ್ತ್ ಕುಡೊರ ಪಣ್ಲೆ।"
            else:
                clarification = "I'm not completely sure I understood that. Could you please rephrase or provide more details?"
            return state, True, clarification, None

        # Determine topic from entities or intent
        topic = None
        for ent in entities:
            if ent.label in ("LANGUAGE", "MEDICAL_TERM", "PERSON", "LOCATION"):
                topic = ent.text
                break
        if not topic and "sanskrit" in text.lower():
            topic = "Sanskrit"
        elif not topic and "tulu" in text.lower():
            topic = "Tulu"

        return state, False, None, topic

dialogue_manager = DialogueManager()
