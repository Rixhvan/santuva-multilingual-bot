import re
from typing import List, Dict, Any, Optional
from backend.models.schemas import IntentInfo
from backend.nlp.embeddings.vector_space import vector_space

class MultilingualIntentClassifier:
    """
    Multilingual Intent Classification Engine.
    Employs token-level matching, syntactic question detection, and
    multilingual vector semantic similarity.
    """

    LOCATION_WORDS = {
        "where", "where is", "location", "place", "which floor", "directions", "located",
        "कुत्र", "कुत्र अस्ति", "क्व", "मार्गः", "kutra", "kutra asti", "द्वारं", "प्रवेशद्वारं",
        "ವಾಡೆ", "ವಾಡೆ ಉಲ್ಲೆರ್", "ವಾಡೆ ಉಂಡು", "vaade", "vaade uller", "vaade undu", "ode", "ಓಡೆ"
    }

    TIME_WORDS = {
        "when", "time", "timing", "schedule", "what time", "hours", "visiting hours", "opd", "open",
        "कदा", "समयः", "कति", "वेला", "कालः", "दिवसः", "उद्घाट्यते", "kada",
        "ಏಪ", "ಪೊರ್ತು", "ಗಂಟೆ", "aepa", "portu", "gante", "timing", "eapa"
    }

    GREETING_WORDS = {
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening", "good day", "greetings", "suprabhatam",
        "नमस्ते", "नमो", "प्रणामः", "सुप्रभातम्", "शुभदिनम्", "सुस्वागतम्", "शुभरात्रिः", "namaste", "shubhadiinam",
        "ನಮಸ್ಕಾರ", "ನಮಸ್ಕಾರೊ", "namaskara", "namaskaro"
    }

    FAREWELL_EXACT = {
        "bye", "goodbye", "see you", "farewell", "take care",
        "पुनर्मिलामः", "गमिष्यामि", "शुभं भवतु", "punarmilamah",
        "ಪೋದು ಬರ್ಪೆ", "podu barpe"
    }

    THANKS_WORDS = {
        "thank", "thanks", "appreciate", "grateful",
        "धन्यवादः", "अनुगृहीतोऽस्मि", "कृतज्ञोऽस्मि", "dhanyavadah",
        "ಸೊಲ್ಮೆಲು", "solmelu", "ಧನ್ಯವಾದ", "dhanyavada"
    }

    INTRODUCTION_PHRASES = [
        "my name is", "i am", "myself", "call me",
        "मम नाम", "अहम्", "अहं", "mama nama",
        "ಎನ್ನ ಪುದರ್", "enna pudar", "yan"
    ]

    HELP_WORDS = {
        "help", "assist", "assistance", "support", "guidance", "i don't know where to go",
        "साहाय्यम्", "साहाय्यं", "कृपया साहाय्यं", "मां रक्ष", "साहाय्यार्थं", "sahayyam",
        "ಸಹಾಯ", "sahaya", "help malpule"
    }

    EMERGENCY_WORDS = {
        "emergency", "urgent", "ambulance", "critical", "danger", "dying", "accident", "unconscious", "choking", "bleeding",
        "आपत्कालः", "सङ्कटम्", "त्राणम्", "शीघ्रम्", "रक्तस्रावः", "अचेतनः", "शीघ्रं साहाय्यं",
        "ಆಪತ್ತ್", "ತುರ್ತು", "aapath", "ನೆತ್ತೆರ್"
    }

    YES_EXACT = {"yes", "yeah", "yep", "sure", "correct", "आम्", "सत्यम्", "ಆಂಡ್", "ಅಂದ್", "and", "aand"}
    NO_EXACT = {"no", "nope", "nah", "never", "न", "नहि", "मा", "ಇಜ್ಜಿ", "ಅತ್ತ್", "ijji", "att"}

    def classify(self, text: str, tokens: List[Dict[str, Any]], lang: str) -> IntentInfo:
        text_lower = text.lower().strip()
        clean_no_punct = re.sub(r'[^\w\s]', '', text_lower)
        words_lower = [t.get("normalized_form", t.get("surface_form", "")).lower() for t in tokens]
        concepts = {t.get("concept") for t in tokens if t.get("concept")}
        is_question = "?" in text or any(w in ["what", "where", "when", "why", "who", "which", "how", "कुत्र", "कदा", "कथम्", "किम्", "ವಾಡೆ", "ಏಪ", "ದಾನೆ", "ಎಂಚ", "eapa", "vaade", "daane", "encha"] for w in words_lower)

        # 1. Emergency
        if any(w in text_lower for w in self.EMERGENCY_WORDS) or "EMERGENCY" in concepts:
            return IntentInfo(intent="EMERGENCY", confidence=0.98, all_scores={"EMERGENCY": 0.98})

        # 2. Greetings
        if any(w in text_lower for w in self.GREETING_WORDS) or "GREETING" in concepts:
            # If greeting also asks "how are you"
            if is_question and any(w in text_lower for w in ["how are you", "encha uller", "कथम् अस्ति"]):
                return IntentInfo(intent="GENERAL_QUESTION", confidence=0.92, secondary_intent="GREETING")
            return IntentInfo(intent="GREETING", confidence=0.96, all_scores={"GREETING": 0.96})

        # 3. Thanks
        if any(w in text_lower for w in self.THANKS_WORDS) or "THANKS" in concepts:
            return IntentInfo(intent="THANKS", confidence=0.96, secondary_intent="GREETING" if "solmelu" in text_lower or "ಸೊಲ್ಮೆಲು" in text else None, all_scores={"THANKS": 0.96})

        # 4. Farewell
        if any(w in text_lower for w in self.FAREWELL_EXACT) or (clean_no_punct in ["bye", "goodbye", "barpe", "ಬರ್ಪೆ"]):
            return IntentInfo(intent="FAREWELL", confidence=0.96, all_scores={"FAREWELL": 0.96})

        # 5. Introduction
        if any(p in text_lower for p in self.INTRODUCTION_PHRASES) or "INTRODUCTION" in concepts:
            if not is_question and any(p in text_lower for p in ["my name is", "मम नाम", "ಎನ್ನ ಪುದರ್", "enna pudar", "i am", "call me", "myself"]):
                return IntentInfo(intent="INTRODUCTION", confidence=0.96, all_scores={"INTRODUCTION": 0.96})

        # 6. Yes / No (Only if not a question)
        if not is_question:
            if clean_no_punct in self.YES_EXACT or "YES" in concepts:
                return IntentInfo(intent="YES", confidence=0.98, all_scores={"YES": 0.98})
            if clean_no_punct in self.NO_EXACT or "NO" in concepts or "NO_NOT" in concepts:
                return IntentInfo(intent="NO", confidence=0.98, all_scores={"NO": 0.98})
            if "correct" in clean_no_punct or "exactly" in clean_no_punct or "ಎವಮೇವ" in text:
                return IntentInfo(intent="CONFIRMATION", confidence=0.94, all_scores={"CONFIRMATION": 0.94})
            if "incorrect" in clean_no_punct or "wrong" in clean_no_punct or "ನ ಸಮ್ಯಕ್" in text:
                return IntentInfo(intent="DENIAL", confidence=0.94, all_scores={"DENIAL": 0.94})

        # 8. Help vs Request
        has_help_word = any(w in text_lower for w in ["help", "assist", "assistance", "support", "guidance", "साहाय्यं", "साहाय्यम्", "sahaya", "sahayyam", "मां रक्ष"])
        has_polite_request = any(w in text_lower for w in ["please", "कृपया", "ದಯಮಲ್ತ್", "dayamalth", "kindly", "ददातु", "सूचयतु", "दर्शयतु", "पठतु", "स्पष्टीकरोतु", "दाव्यम्", "दातव्यम्"])

        if has_help_word:
            return IntentInfo(intent="HELP", confidence=0.95, all_scores={"HELP": 0.95})
        elif has_polite_request:
            return IntentInfo(intent="REQUEST", confidence=0.93, all_scores={"REQUEST": 0.93})

        # 9. Location Query
        if any(w in text_lower for w in self.LOCATION_WORDS) or "WHERE" in concepts:
            return IntentInfo(intent="LOCATION_QUERY", confidence=0.96, secondary_intent="INFORMATION_QUERY", all_scores={"LOCATION_QUERY": 0.96})

        # 10. Time Query
        if any(w in text_lower for w in self.TIME_WORDS) or "WHEN" in concepts or "TIME" in concepts or any(w in text_lower for w in ["appointment time", "portu", "gante", "hours", "open"]):
            return IntentInfo(intent="TIME_QUERY", confidence=0.95, secondary_intent="INFORMATION_QUERY", all_scores={"TIME_QUERY": 0.95})

        # 11. Complaint (Physical Symptoms / Fatigue / Pain)
        if any(w in text_lower for w in ["tired", "fatigue", "headache", "stomach", "fever", "pain", "hurt", "dizzy", "sore", "swollen", "shrantah", "श्रान्तः", "शिरोवेदना", "उदरवेदना", "ज्वरः", "तीव्रज्वरः", "तरेಬೇನೆ", "ತರೆಬೇನೆ", "tarebene", "ಬೇನೆ", "ಬಂಜಿಬೇನೆ", "कष्टे", "श्वासकष्टम्", "दुर्बलः"]) or any("वेदना" in w or "पीडा" in w for w in words_lower):
            return IntentInfo(intent="COMPLAINT", confidence=0.95, secondary_intent="INFORMATION_QUERY", all_scores={"COMPLAINT": 0.95})

        # 12. Feedback
        if any(w in text_lower for w in ["laik", "mast laik", "edde uthara", "good response", "nice answer", "very helpful"]):
            return IntentInfo(intent="FEEDBACK", confidence=0.94, all_scores={"FEEDBACK": 0.94})

        # 13. General Conversational Question
        if any(w in text_lower for w in ["what are you doing", "daane malpuva", "madthiya", "किं करोषि", "how are you", "encha uller", "daane vishesha", "ದಾನೆ ವಿಶೇಷ", "enla", "boduva", "who is", "who are", "how does", "katham asti", "कोऽपि नास्ति", "अधिकारी", "जानाति"]):
            return IntentInfo(intent="GENERAL_QUESTION", confidence=0.94, secondary_intent="GREETING", all_scores={"GENERAL_QUESTION": 0.94})

        # 14. Information Query
        if any(w in text_lower for w in ["tell", "information", "report", "appointment", "about", "diagnos", "tips", "sanskrit", "tulu", "medicine", "दೋಕ್ತೆರೆನ್", "ಮರ್ದ್", "ತಿಕ್ಕುಂಡಾ", "ವಿಷಯ", "ಬಗ್ಗೆ", "ज्ञातुम्", "द्रष्टुम्", "বিষये", "विषये", "सूचनां", "विवरणं", "उपलभ्यते", "गच्छामि"]):
            return IntentInfo(intent="INFORMATION_QUERY", confidence=0.93, all_scores={"INFORMATION_QUERY": 0.93})

        # 15. Classical Statement
        if "इत्याह" in text:
            return IntentInfo(intent="STATEMENT", confidence=0.90, all_scores={"STATEMENT": 0.90})

        # 15. Vector Semantic Fallback
        ranked = vector_space.find_closest_intent(text)
        if ranked and ranked[0][1] >= 0.28:
            top_intent, top_score = ranked[0]
            sec_intent = ranked[1][0] if len(ranked) > 1 else None
            conf = min(0.92, top_score + 0.35)
            scores_dict = {name: score for name, score in ranked[:5]}
            return IntentInfo(
                intent=top_intent,
                confidence=conf,
                secondary_intent=sec_intent,
                all_scores=scores_dict
            )

        return IntentInfo(
            intent="UNKNOWN",
            confidence=0.35,
            secondary_intent=None,
            all_scores={}
        )

intent_classifier = MultilingualIntentClassifier()
