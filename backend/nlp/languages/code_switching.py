from typing import List, Dict, Any, Tuple
from backend.nlp.language_detection.detector import language_detector
from backend.config.settings import settings

class CodeSwitchingHandler:
    """
    Code-Switching and Mixed-Language Processing Pipeline.
    Performs token-level language identification, segmenting mixed sentences
    such as 'Doctor naale appointment idiya?' into their constituents.
    """

    def analyze_tokens(self, tokens: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[Dict[str, Any]]]:
        """
        Runs token-level language identification.
        Returns:
            - is_code_switched (bool)
            - detected_languages (list of language names)
            - token_lang_records (list with token text and detected language)
        """
        token_records = []
        lang_set = set()

        for tok in tokens:
            surface = tok.get("surface_form", "")
            tok_type = tok.get("token_type", "WORD")

            if tok_type in ("PUNCT", "DANDA", "NUMBER", "URL"):
                token_records.append({
                    "token": surface,
                    "language": "neutral",
                    "type": tok_type
                })
                continue

            lang_code = language_detector.detect_token_language(surface)
            lang_name = settings.language_names.get(lang_code, lang_code)

            if lang_code in ("en", "sa", "tcy", "kn"):
                lang_set.add(lang_name)

            token_records.append({
                "token": surface,
                "language": lang_name,
                "language_code": lang_code,
                "type": tok_type
            })

        is_switched = len(lang_set) > 1
        return is_switched, sorted(list(lang_set)), token_records

code_switching_handler = CodeSwitchingHandler()
