import re
import unicodedata
from typing import Tuple, List, Dict, Any
from backend.models.schemas import LanguageInfo
from backend.config.settings import settings

class LanguageDetector:
    """
    Multilingual Language Identification System.
    Identifies: Sanskrit (sa), English (en), Tulu (tcy), and distinguishes Kannada from Tulu.
    Supports Devanagari, Kannada, Latin scripts, and IAST transliteration.
    """
    
    # Script Unicode Ranges
    DEVANAGARI_RANGE = (0x0900, 0x097F)
    KANNADA_RANGE = (0x0C80, 0x0CFF)
    
    # Sanskrit IAST diacritics
    IAST_CHARS = set("āīūṛṝḷḹṃḥṅñṭḍṇśṣ")
    
    # Strong Tulu Lexical Markers (Kannada Script)
    TULU_KANNADA_MARKERS = {
        "ದಾನೆ", "ದಾನೆ?", "ದಾಲ", "ದಾಲಾ", "ಇಜ್ಜಿ", "ಇಜ್ಜಂಡ", "ಬೋಡು", "ಬಲ್ಲಿ", 
        "ಎಂಚ", "ಎಂಚಿನ", "ಒವ್ವು", "ವಾಡೆ", "ಏರ್", "ಯಾನ್", "ಈ", "ನಮ", "ನಂಕ್", 
        "ಎಂಕ್", "ಅಪಗ", "ಇಪಗ", "ಬಲೆ", "ಪೋಲೆ", "ತೂಲೆ", "ಮಲ್ಪುಲೆ", "ಮಲ್ಪು", 
        "ಆಪುಂಡು", "ಆಂಡ್", "ಉಲ್ಲೆರಾ", "ಉಂಡು", "ಉಲ್ಲ", "ಉಲ್ಲೆ", "ಕುಡ್ಲ", "ತುಳು",
        "ಬತ್ತೆ", "ಪೋಯೆ", "ಪಣ್ಲೆ", "ಗೊತ್ತುಂಡು", "ಗೊತ್ತಿಜ್ಜಿ", "ದಯಮಲ್ತ್", "ಕೇಣ್ಲೆ",
        "ಸಾಲೆಯಿ", "ಇನಿ", "ನಾಲೆ", "ತಿಕುಂಡು", "ಮರ್ದ್", "ಸೀಕ್", "ಬೇನೆ", "ತರೆಬೇನೆ"
    }

    # Standard Kannada Markers (to distinguish from Tulu)
    KANNADA_DISTINCT_MARKERS = {
        "ಏನು", "ಹೇಗೆ", "ಎಲ್ಲಿ", "ಯಾರು", "ಯಾವಾಗ", "ಬೇಕು", "ಬೇಡ", "ಇಲ್ಲ", "ಇದೆ",
        "ನಾನು", "ನೀವು", "ನಾವು", "ನನ್ನ", "ನಿಮ್ಮ", "ಮಾಡುತ್ತೇನೆ", "ಆಗುತ್ತದೆ", "ಬನ್ನಿ",
        "ಹೋಗಿ", "ನೋಡಿ", "ಹೇಳಿ", "ಗೊತ್ತಿದೆ", "ಗೊತ್ತಿಲ್ಲ", "ದಯವಿಟ್ಟು", "ಕೇಳಿ"
    }

    # Strong Tulu Lexical Markers (Latin Script / Transliterated)
    TULU_LATIN_MARKERS = {
        "encha", "uller", "ullera", "ullara", "daane", "daala", "dala", "ijji", 
        "ijjanda", "bodu", "balli", "ovvu", "vaade", "er", "eer", "yaan", "yan", 
        "ee", "nama", "nank", "enk", "apaga", "ipaga", "bale", "pole", "toole", 
        "tule", "malpule", "malpu", "aapundu", "apundu", "and", "aand", "undu", 
        "kudla", "tulu", "tulunad", "panle", "gottundu", "gottijji", "dayamalth", 
        "kenle", "ini", "naale", "tikundu", "mard", "seek", "bene", "tarebene",
        "enla", "laik", "mast", "padchi", "boduva", "kannige", "kayi", "karthi",
        "idiya", "madthiya", "enna"
    }

    # Sanskrit Lexical Markers (Devanagari)
    SANSKRIT_DEVANAGARI_MARKERS = {
        "नमस्ते", "नमो", "अहम्", "अहं", "त्वम्", "त्वं", "भवन्तः", "भवतः", "भवत्याः", 
        "अस्ति", "सन्ति", "असि", "अस्मि", "कुत्र", "कदा", "कथम्", "कथं", "किम्", "किं", 
        "कः", "का", "चिकित्सकः", "चिकित्सालयः", "स्वास्थ्यम्", "औषधम्", "रुग्णः", 
        "इच्छामि", "कृपया", "धन्यवादः", "शुभदिनम्", "पुनर्मिलामः", "द्रष्टुम्", 
        "ज्ञातुम्", "वदतु", "श्रोतुम्", "गच्छामि", "आगच्छति", "रामस्य", "मार्गः",
        "समयः", "कति", "नेष्यति", "कार्यम्", "भवतु", "शान्तिः", "वेद", "शास्त्रम्"
    }

    # Sanskrit Lexical Markers (Latin / IAST)
    SANSKRIT_LATIN_MARKERS = {
        "namaste", "namo", "aham", "tvam", "bhavatah", "bhavan", "asti", "santi", 
        "asmi", "kutra", "kada", "katham", "kim", "kah", "kaa", "chikitsaka", 
        "chikitsakah", "chikitsalayah", "aushadham", "icahami", "kripaya", 
        "dhanyavadah", "shubhadiinam", "punarmilamah", "drashtum", "jnatum", 
        "vadatu", "gacchami", "agacchati", "ramasya", "samayah", "kati", "bhavatu"
    }

    # English Common Function Words
    ENGLISH_MARKERS = {
        "hello", "hi", "hey", "how", "what", "where", "when", "why", "who", "which", 
        "is", "are", "am", "was", "were", "be", "been", "can", "could", "will", "would", 
        "should", "have", "has", "had", "do", "does", "did", "please", "thank", "thanks", 
        "doctor", "hospital", "medicine", "appointment", "help", "need", "want", "tell", 
        "good", "morning", "afternoon", "evening", "yes", "no", "report", "pain", "time",
        "located", "where is", "i am", "my", "your", "name", "about"
    }

    def detect_script(self, text: str) -> str:
        """Determines the primary script of the input string."""
        devanagari_count = 0
        kannada_count = 0
        latin_count = 0
        iast_diacritics = 0

        for char in text:
            code = ord(char)
            if self.DEVANAGARI_RANGE[0] <= code <= self.DEVANAGARI_RANGE[1]:
                devanagari_count += 1
            elif self.KANNADA_RANGE[0] <= code <= self.KANNADA_RANGE[1]:
                kannada_count += 1
            elif ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
                latin_count += 1
            elif char in self.IAST_CHARS:
                iast_diacritics += 1
                latin_count += 1

        total = devanagari_count + kannada_count + latin_count
        if total == 0:
            return "Latin"

        if devanagari_count / total > 0.4:
            return "Devanagari"
        if kannada_count / total > 0.4:
            return "Kannada"
        if iast_diacritics > 0 and (iast_diacritics / max(1, latin_count) > 0.05):
            return "IAST"
        return "Latin"

    def detect_token_language(self, token: str) -> str:
        """Identifies the language of an individual token for code-switching."""
        clean = re.sub(r'[^\w\s]', '', token).strip()
        clean_lower = clean.lower()
        if not clean:
            return "unknown"

        script = self.detect_script(token)

        # Devanagari script: predominantly Sanskrit
        if script == "Devanagari":
            return "sa"

        # Kannada script: differentiate Tulu vs Kannada
        if script == "Kannada":
            if clean in self.TULU_KANNADA_MARKERS:
                return "tcy"
            if clean in self.KANNADA_DISTINCT_MARKERS:
                return "kn"
            # Characteristic Tulu phonology endings
            if clean.endswith("ಂಡು") or clean.endswith("ೆರಾ") or clean.endswith("ೆರ್") or clean.endswith("ೊಡು"):
                return "tcy"
            return "tcy"  # Default assumption in Tulu context if script is Kannada

        # Latin script: could be English, Tulu (translit), or Sanskrit (translit)
        if clean_lower in self.TULU_LATIN_MARKERS or clean_lower.endswith("undu") or clean_lower.endswith("odu") or clean_lower.endswith("iya"):
            return "tcy"
        if clean_lower in self.SANSKRIT_LATIN_MARKERS or any(c in self.IAST_CHARS for c in clean_lower):
            return "sa"
        if clean_lower in self.ENGLISH_MARKERS:
            return "en"

        # General English dictionary word check
        if re.match(r'^[a-zA-Z]+$', clean):
            # Check length and character distribution
            return "en"

        return "unknown"

    UNICODE_WORD_PATTERN = re.compile(
        r'[\u0900-\u0963\u0966-\u097F]+|[\u0C80-\u0CE3\u0CE6-\u0CFF]+|[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]+'
    )

    def extract_words(self, text: str) -> List[str]:
        """Extracts words preserving Indic combining marks, vowels, and visarga."""
        return self.UNICODE_WORD_PATTERN.findall(text)

    def identify_language(self, text: str) -> LanguageInfo:
        """
        Full language identification with script, lexical, and contextual features.
        Returns LanguageInfo with language, script, confidence, and code-switching metrics.
        """
        script = self.detect_script(text)
        words = self.extract_words(text)
        clean_text_lower = text.lower().strip()

        token_langs = [self.detect_token_language(w) for w in words]
        lang_counts = {
            "en": token_langs.count("en"),
            "sa": token_langs.count("sa"),
            "tcy": token_langs.count("tcy"),
            "kn": token_langs.count("kn"),
            "unknown": token_langs.count("unknown")
        }
        total_tokens = len(words) if words else 1

        is_code_switched = False
        switched_languages = []

        # Check for multiple active languages
        active_langs = [l for l in ["en", "sa", "tcy"] if lang_counts[l] > 0]
        if len(active_langs) > 1:
            is_code_switched = True
            switched_languages = [settings.language_names[l] for l in active_langs]

        # Case 1: Devanagari Script -> Sanskrit
        if script == "Devanagari":
            # Check for classical Sanskrit markers
            sa_hits = sum(1 for w in words if w in self.SANSKRIT_DEVANAGARI_MARKERS or w.endswith("ः") or w.endswith("म्") or w.endswith("स्य") or w.endswith("ति") or w.endswith("सि") or w.endswith("मि"))
            confidence = min(0.98, max(0.70, (sa_hits + 1) / (len(words) + 1) + 0.4))
            return LanguageInfo(
                language="Sanskrit",
                language_code="sa",
                script="Devanagari",
                confidence=confidence,
                is_code_switched=is_code_switched,
                code_switched_languages=switched_languages,
                needs_clarification=False,
                details={"marker_hits": sa_hits, "total_words": len(words)}
            )

        # Case 2: Kannada Script -> Tulu vs Kannada distinction
        if script == "Kannada":
            tulu_hits = sum(1 for w in words if w in self.TULU_KANNADA_MARKERS or w.endswith("ಂಡು") or w.endswith("ೆರಾ") or w.endswith("ೊಡು") or w.endswith("ೆರ್"))
            kannada_hits = sum(1 for w in words if w in self.KANNADA_DISTINCT_MARKERS)

            if kannada_hits > tulu_hits:
                # User typed standard Kannada, low Tulu confidence
                return LanguageInfo(
                    language="Kannada",
                    language_code="kn",
                    script="Kannada",
                    confidence=0.75,
                    is_code_switched=is_code_switched,
                    code_switched_languages=switched_languages,
                    needs_clarification=True,
                    details={"note": "Kannada text detected; Tulu expected. Prompt user for confirmation.", "kannada_hits": kannada_hits}
                )
            else:
                confidence = min(0.96, 0.70 + (tulu_hits * 0.1))
                return LanguageInfo(
                    language="Tulu",
                    language_code="tcy",
                    script="Kannada",
                    confidence=confidence,
                    is_code_switched=is_code_switched,
                    code_switched_languages=switched_languages,
                    needs_clarification=False,
                    details={"tulu_hits": tulu_hits, "tulu_resource_tier": "PARTIAL"}
                )

        # Case 3: IAST Script -> Sanskrit
        if script == "IAST":
            return LanguageInfo(
                language="Sanskrit",
                language_code="sa",
                script="IAST",
                confidence=0.92,
                is_code_switched=is_code_switched,
                code_switched_languages=switched_languages,
                needs_clarification=False,
                details={"transliteration": "IAST"}
            )

        # Case 4: Latin Script -> Differentiate English, Tulu (translit), Sanskrit (translit), or Code-switched
        tulu_latin_hits = sum(1 for w in words if w.lower() in self.TULU_LATIN_MARKERS or w.lower().endswith("undu") or w.lower().endswith("odu") or w.lower().endswith("iya") or w.lower().endswith("ina"))
        sa_latin_hits = sum(1 for w in words if w.lower() in self.SANSKRIT_LATIN_MARKERS)
        en_hits = sum(1 for w in words if w.lower() in self.ENGLISH_MARKERS)

        # Check for mixed Tulu + English code-switching e.g. "Doctor naale appointment idiya?"
        if tulu_latin_hits > 0 and en_hits > 0:
            primary_lang = "Tulu" if tulu_latin_hits >= en_hits else "English"
            return LanguageInfo(
                language=primary_lang,
                language_code="tcy" if primary_lang == "Tulu" else "en",
                script="Latin",
                confidence=0.88,
                is_code_switched=True,
                code_switched_languages=["English", "Tulu"],
                needs_clarification=False,
                details={"code_switching": True, "en_tokens": en_hits, "tulu_tokens": tulu_latin_hits}
            )

        # Transliterated Tulu
        if tulu_latin_hits > 0 and tulu_latin_hits >= sa_latin_hits:
            confidence = min(0.95, 0.70 + (tulu_latin_hits * 0.12))
            return LanguageInfo(
                language="Tulu",
                language_code="tcy",
                script="Latin",
                confidence=confidence,
                is_code_switched=is_code_switched,
                code_switched_languages=switched_languages,
                needs_clarification=False,
                details={"tulu_latin_hits": tulu_latin_hits}
            )

        # Transliterated Sanskrit
        if sa_latin_hits > 0 and sa_latin_hits > en_hits:
            return LanguageInfo(
                language="Sanskrit",
                language_code="sa",
                script="Latin",
                confidence=0.85,
                is_code_switched=is_code_switched,
                code_switched_languages=switched_languages,
                needs_clarification=False,
                details={"sa_latin_hits": sa_latin_hits}
            )

        # English
        if en_hits > 0 or words:
            # If word is unknown or ambiguous single letter
            confidence = 0.95 if en_hits > 0 else 0.65
            needs_clarif = confidence < settings.lang_confidence_threshold
            return LanguageInfo(
                language="English",
                language_code="en",
                script="Latin",
                confidence=confidence,
                is_code_switched=is_code_switched,
                code_switched_languages=switched_languages,
                needs_clarification=needs_clarif,
                details={"en_hits": en_hits}
            )

        # Ambiguous fallback
        return LanguageInfo(
            language="English",
            language_code="en",
            script="Latin",
            confidence=0.40,
            is_code_switched=False,
            code_switched_languages=[],
            needs_clarification=True,
            details={"fallback": True}
        )

# Global singleton detector
language_detector = LanguageDetector()
