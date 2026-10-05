import re
import unicodedata
from typing import Tuple

class UnicodeNormalizer:
    """
    Unicode and Text Normalization Engine for Sanskrit, English, and Tulu.
    Handles canonical decomposition/composition (NFC), whitespace hygiene,
    elongated character reduction, punctuation standardization, and script-safe cleanup.
    """

    # Quotation and dash normalizations
    PUNCTUATION_REPLACEMENTS = {
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '-', '\u2026': '...', '\u00A0': ' ',
        '’': "'", '‘': "'", '“': '"', '”': '"', '—': '-', '–': '-'
    }

    # Sanskrit / Indic specific character normalizations
    # Nuktas or variant signs in Devanagari / Kannada
    INDIC_NORMALIZATIONS = {
        '\u0931': '\u0930',  # Devanagari RRA to RA
        '\u0934': '\u0933',  # Devanagari LLLA to LLA
        '\u0929': '\u0928',  # Devanagari NNNA to NA
    }

    def normalize_whitespace(self, text: str) -> str:
        """Collapses irregular whitespace, tabs, and non-breaking spaces."""
        text = re.sub(r'[\r\f\v]', ' ', text)
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()

    def normalize_repeated_chars(self, text: str, lang: str = "en") -> str:
        """
        Compresses repeated characters from typing elongation (e.g., 'heyyy' -> 'hey',
        'pleaaase' -> 'please', 'soo good' -> 'so good').
        Carefully avoids destroying double consonants in Dravidian / Sanskrit words where
        gemination is phonemic (e.g., Kannada/Tulu 'ಇಜ್ಜಿ' [ijji], Sanskrit 'अस्ति' [asti]).
        """
        # In Latin script, reduce 3+ consecutive identical characters to 1 or 2
        # (e.g., 'heyyyyy' -> 'hey', 'sooooo' -> 'so', 'pleaaase' -> 'please')
        def reduce_latin(match):
            char = match.group(1)
            full = match.group(0)
            # Greeting contractions
            if char.lower() == 'o' and len(full) >= 3:
                return 'o'
            if char.lower() in ('y', 'i', 'a', 'u') and len(full) >= 2:
                return char
            # English standard double allowed: 'll', 'ee', 'ss', 'tt', 'ff'
            if char.lower() in 'lestf':
                return char * 2
            return char

        text = re.sub(r'([a-zA-Z])\1{2,}', reduce_latin, text)

        # In Indic scripts, reduce identical matras or repeated halantas that are typing typos
        text = re.sub(r'([\u0901-\u0903\u093C-\u094D])\1+', r'\1', text)
        text = re.sub(r'([\u0C81-\u0C83\u0CBC-\u0CCD])\1+', r'\1', text)

        return text

    def normalize_punctuation(self, text: str) -> str:
        """Standardizes typography, smart quotes, dashes, preserving Danda (। and ॥)."""
        for orig, rep in self.PUNCTUATION_REPLACEMENTS.items():
            text = text.replace(orig, rep)
        return text

    def normalize_unicode(self, text: str) -> str:
        """Applies Unicode NFC normalization."""
        # NFC preserves pre-composed characters while normalizing decomposed sequences
        normalized = unicodedata.normalize('NFC', text)
        for orig, rep in self.INDIC_NORMALIZATIONS.items():
            normalized = normalized.replace(orig, rep)
        return normalized

    def normalize(self, text: str, lang: str = "en") -> Tuple[str, list[dict]]:
        """
        Full text normalization pipeline.
        Returns normalized text and list of transformation audit logs.
        """
        transformations = []
        original = text

        # 1. Unicode NFC
        nfc_text = self.normalize_unicode(text)
        if nfc_text != original:
            transformations.append({"stage": "unicode_nfc", "before": original, "after": nfc_text})

        # 2. Punctuation standardization
        punct_text = self.normalize_punctuation(nfc_text)
        if punct_text != nfc_text:
            transformations.append({"stage": "punctuation", "before": nfc_text, "after": punct_text})

        # 3. Repeated character reduction
        char_reduced = self.normalize_repeated_chars(punct_text, lang=lang)
        if char_reduced != punct_text:
            transformations.append({"stage": "repeated_chars", "before": punct_text, "after": char_reduced})

        # 4. Whitespace cleanup
        clean_text = self.normalize_whitespace(char_reduced)
        if clean_text != char_reduced:
            transformations.append({"stage": "whitespace", "before": char_reduced, "after": clean_text})

        return clean_text, transformations

normalizer = UnicodeNormalizer()
