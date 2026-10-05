import re
from typing import List, Dict, Any, Optional
from backend.models.schemas import EntityInfo

class BaseNER:
    """Base class for language-specific NER extractors."""
    def extract_entities(self, text: str, tokens: List[Dict[str, Any]]) -> List[EntityInfo]:
        raise NotImplementedError

class EnglishNER(BaseNER):
    """NER extractor for English."""
    
    PERSON_PATTERNS = [
        re.compile(r'\b(?:Dr\.|Doctor|Mr\.|Mrs\.|Ms\.|Prof\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'),
        re.compile(r'\b(?:my name is|I am|call me)\s+([A-Z][a-z]+)\b', re.IGNORECASE)
    ]
    
    KNOWN_ENTITIES = {
        "MEDICAL_TERM": {
            "doctor", "physician", "surgeon", "hospital", "clinic", "dispensary",
            "appointment", "consultation", "report", "test", "prescription",
            "treatment", "diagnosis", "nurse", "patient"
        },
        "BODY_PART": {
            "head", "brain", "eye", "eyes", "ear", "ears", "throat", "neck",
            "chest", "heart", "stomach", "abdomen", "back", "hand", "hands",
            "leg", "legs", "foot", "feet", "blood", "bone", "skin"
        },
        "DISEASE": {
            "fever", "headache", "migraine", "stomach ache", "backache",
            "pain", "cough", "cold", "flu", "infection", "diabetes",
            "hypertension", "asthma", "allergy", "nausea"
        },
        "MEDICINE": {
            "medicine", "medicines", "medication", "paracetamol", "aspirin",
            "ibuprofen", "antibiotic", "tablet", "syrup", "capsule", "injection"
        },
        "LANGUAGE": {
            "english", "sanskrit", "tulu", "kannada", "hindi", "tamil", "telugu"
        },
        "DATE": {
            "today", "tomorrow", "yesterday", "monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"
        },
        "TIME": {
            "morning", "afternoon", "evening", "night", "noon", "midnight",
            "am", "pm", "o'clock", "schedule", "time"
        },
        "LOCATION": {
            "hospital", "clinic", "mangalore", "udupi", "bangalore", "delhi", "mumbai"
        }
    }

    def extract_entities(self, text: str, tokens: List[Dict[str, Any]]) -> List[EntityInfo]:
        entities = []
        lower_text = text.lower()

        # Check Person regexes
        for pat in self.PERSON_PATTERNS:
            for match in pat.finditer(text):
                entities.append(EntityInfo(
                    text=match.group(1),
                    label="PERSON",
                    start=match.start(1),
                    end=match.end(1),
                    confidence=0.92
                ))

        # Check token/word dictionary
        for tok in tokens:
            surface = tok.get("surface_form", "")
            norm = tok.get("normalized_form", surface).lower()
            start = tok.get("start", 0)
            end = tok.get("end", len(surface))

            for label, word_set in self.KNOWN_ENTITIES.items():
                if norm in word_set:
                    entities.append(EntityInfo(
                        text=surface,
                        label=label,
                        start=start,
                        end=end,
                        confidence=0.95
                    ))

            # Number entity
            if tok.get("token_type") == "NUMBER" or surface.isdigit():
                entities.append(EntityInfo(
                    text=surface,
                    label="NUMBER",
                    start=start,
                    end=end,
                    confidence=1.0
                ))

        return entities

class SanskritNER(BaseNER):
    """NER extractor for Sanskrit (Devanagari & Latin transliteration)."""
    
    KNOWN_ENTITIES = {
        "PERSON": {
            "रामः", "रामम्", "रामेण", "रामाय", "रामस्य", "रामे", "राम", "रामोऽस्ति",
            "कृष्णः", "कृष्णस्य", "कृष्णम्", "कृष्ण", "रमेशः", "सुरेशः",
            "ramasya", "ramah", "rama", "krishna", "Ramah"
        },
        "MEDICAL_TERM": {
            "चिकित्सकः", "चिकित्सकम्", "चिकित्सकस्य", "चिकित्सकाय", "चिकित्सक", "चिकित्सकं",
            "चिकित्सालयः", "चिकित्सालयम्", "चिकित्सालये", "चिकित्सालयस्य", "चिकित्सालय", "चिकित्सालयं",
            "वैद्यः", "वैद्यस्य", "वैद्याः", "वैद्यम्", "स्वास्थ्यम्", "आरोग्यम्", "रुग्णः", "रोगी", "रुग्णालयः",
            "chikitsakah", "chikitsalayah", "vaidya", "svasthya"
        },
        "BODY_PART": {
            "शिरः", "शिरसि", "नेत्रम्", "कर्णः", "नासिका", "मुखम्",
            "दन्तः", "जिह्वा", "हस्तः", "पादः", "हृदयम्", "उदरम्", "रक्तम्", "पाद"
        },
        "DISEASE": {
            "ज्वरः", "तापः", "वेदना", "शिरोवेदना", "उदरवेदना", "कासः", "श्वासः", "प्रमेहः", "रोगः",
            "तीव्रज्वरः", "नेत्रवेदना", "दन्तपीडा", "पादवेदना", "हृदयवेदना"
        },
        "MEDICINE": {
            "औषधम्", "औषधस्य", "औषधानि", "भेषजम्", "क्वाथः", "चूर्णम्", "वटी", "aushadham",
            "महौषधम्", "महौषधं", "औषधं"
        },
        "DATE": {
            "अद्य", "श्वः", "ह्यः", "adya", "shvah", "hyah"
        },
        "TIME": {
            "समयः", "वेला", "कालः", "प्रातः", "सायम्", "मध्याह्नः"
        },
        "LOCATION": {
            "चिकित्सालयः", "चिकित्सालयं", "काशी", "अयोध्या", "भारतम्", "कुत्र"
        },
        "LANGUAGE": {
            "संस्कृतम्", "संस्कृतेन", "संस्कृतभाषा", "संस्कृतभाषायाः", "भाषा", "sanskrit"
        }
    }

    def extract_entities(self, text: str, tokens: List[Dict[str, Any]]) -> List[EntityInfo]:
        entities = []
        for tok in tokens:
            surface = tok.get("surface_form", "")
            norm = tok.get("normalized_form", surface).lower()
            start = tok.get("start", 0)
            end = tok.get("end", len(surface))

            for label, word_set in self.KNOWN_ENTITIES.items():
                if surface in word_set or norm in word_set:
                    entities.append(EntityInfo(
                        text=surface,
                        label=label,
                        start=start,
                        end=end,
                        confidence=0.94
                    ))
        return entities

class TuluNER(BaseNER):
    """NER extractor for Tulu (Kannada script and Latin transliteration)."""

    KNOWN_ENTITIES = {
        "PERSON": {
            "ರಮೇಶ್", "ರಾವ್", "ಸುರೇಶ್", "ದಿನೇಶ್", "ಪ್ರಿಯಾ", "Ramesh", "Rao", "Suresh", "Priya"
        },
        "MEDICAL_TERM": {
            "ದೋಕ್ತೆರ್", "ದೋಕ್ತರ್", "ಡಾಕ್ಟರ್", "ದವಾಖಾನೆ", "ಆಸ್ಪತ್ರೆ", "ದೋಕ್ತೆರೆಗ್",
            "doctor", "dokther", "davakhane", "aspatre", "appointment"
        },
        "BODY_PART": {
            "ತರೆ", "ಕಣ್ಣ್", "ಕೈ", "ಕಾರ್", "ಬಂಜಿ", "ನೆತ್ತೆರ್", "ಬಾಯಿ", "ಮೂಂಕು",
            "tare", "kann", "kayi", "kaar", "banji", "netter"
        },
        "DISEASE": {
            "ಸೀಕ್", "ಬೇನೆ", "ತರೆಬೇನೆ", "ಬಂಜಿಬೇನೆ", "ಸೀಕುಲು",
            "seek", "bene", "tarebene", "banjibene"
        },
        "MEDICINE": {
            "ಮರ್ದ್", "ಮರ್ದ್‌ನ್", "ಗುಳಿಗೆ", "mard", "mardu", "gulige"
        },
        "LOCATION": {
            "ಕುಡ್ಲ", "ಕುಡ್ಲಡ್", "ಉಡುಪಿ", "ದವಾಖಾನೆ", "kudla", "kudlad", "udupi"
        },
        "DATE": {
            "ಇನಿ", "ನಾಲೆ", "ಕೊಡೆ", "ini", "naale", "kode"
        },
        "TIME": {
            "ಪೊರ್ತು", "ಗಂಟೆ", "portu", "gante", "timing"
        },
        "LANGUAGE": {
            "ತುಳು", "ತುಳುನಾಡ್", "ಕನ್ನಡ", "tulu", "tulunad", "kannada"
        }
    }

    def extract_entities(self, text: str, tokens: List[Dict[str, Any]]) -> List[EntityInfo]:
        entities = []
        for tok in tokens:
            surface = tok.get("surface_form", "")
            norm = tok.get("normalized_form", surface).lower()
            start = tok.get("start", 0)
            end = tok.get("end", len(surface))

            for label, word_set in self.KNOWN_ENTITIES.items():
                if surface in word_set or norm in word_set:
                    entities.append(EntityInfo(
                        text=surface,
                        label=label,
                        start=start,
                        end=end,
                        confidence=0.92
                    ))
        return entities

class MultilingualNEREngine:
    """
    Unified Multilingual Named Entity Recognition Engine.
    Dispatches to language-specific NER modules with cross-lingual fallback.
    """
    def __init__(self):
        self.en_ner = EnglishNER()
        self.sa_ner = SanskritNER()
        self.tu_ner = TuluNER()

    def extract_entities(self, text: str, tokens: List[Dict[str, Any]], lang: str) -> List[EntityInfo]:
        # Call primary language extractor
        if lang == "sa":
            entities = self.sa_ner.extract_entities(text, tokens)
        elif lang == "tcy":
            entities = self.tu_ner.extract_entities(text, tokens)
        else:
            entities = self.en_ner.extract_entities(text, tokens)

        # Cross-lingual / Code-switched check: if no entities or text has English words
        # (e.g. "Doctor naale appointment idiya?"), run English NER on remaining tokens
        if lang in ("tcy", "sa"):
            en_entities = self.en_ner.extract_entities(text, tokens)
            existing_spans = {(e.start, e.end) for e in entities}
            for e in en_entities:
                if (e.start, e.end) not in existing_spans:
                    entities.append(e)

        return sorted(entities, key=lambda x: x.start)

ner_engine = MultilingualNEREngine()
