import re
from typing import List, Dict, Any, Tuple

class MultilingualTokenizer:
    """
    Language-aware multilingual tokenizer and sentence segmenter for Sanskrit,
    English, and Tulu.
    Recognizes words, Sanskrit danda (।/॥), numbers (Arabic, Devanagari, Kannada),
    abbreviations, URLs, and punctuation.
    """

    # URL pattern
    URL_PATTERN = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\-.~!$&\'()*+,;=:@%]*')

    # Abbreviations
    ABBR_PATTERN = re.compile(r'\b(?:Dr|Mr|Mrs|Ms|Prof|Govt|Dept|No|vs)\.', re.IGNORECASE)

    # Master token regex for Sanskrit, Kannada, Latin, Numbers, Dandas, Punctuation
    TOKEN_REGEX = re.compile(
        r'(?P<URL>https?://[^\s]+)|'
        r'(?P<ABBR>\b(?:Dr|Mr|Mrs|Ms|Prof|Govt|Dept|No|vs)\.)|'
        r'(?P<DATE>\d{1,4}[-/\.]\d{1,2}[-/\.]\d{1,4})|'
        r'(?P<DEVANAGARI_WORD>[\u0900-\u0963\u0966-\u097F]+)|'
        r'(?P<KANNADA_WORD>[\u0C80-\u0CE3\u0CE6-\u0CFF]+)|'
        r'(?P<LATIN_WORD>[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]+(?:[\'-][a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]+)*)|'
        r'(?P<NUMBER>[0-9]+|[\u0966-\u096F]+|[\u0CE6-\u0CEF]+)|'
        r'(?P<DANDA>[\u0964\u0965])|'
        r'(?P<PUNCT>[^\w\s\u0900-\u097F\u0C80-\u0CFF])'
    )

    # Sentence boundary regex including Sanskrit Dandas
    SENTENCE_END_REGEX = re.compile(r'([.?!।॥\n]+)')

    def segment_sentences(self, text: str) -> List[str]:
        """Segments text into sentences based on punctuation and Sanskrit dandas."""
        # Split on sentence terminals while keeping them
        parts = self.SENTENCE_END_REGEX.split(text)
        sentences = []
        current = ""
        for part in parts:
            if not part:
                continue
            current += part
            if self.SENTENCE_END_REGEX.match(part):
                cleaned = current.strip()
                if cleaned:
                    sentences.append(cleaned)
                current = ""
        if current.strip():
            sentences.append(current.strip())
        return sentences if sentences else [text.strip()]

    def tokenize_raw(self, text: str) -> List[str]:
        """Returns list of token surface forms."""
        tokens = []
        for match in self.TOKEN_REGEX.finditer(text):
            tok = match.group(0).strip()
            if tok:
                tokens.append(tok)
        return tokens

    def tokenize(self, text: str) -> List[Dict[str, Any]]:
        """
        Tokenizes text with token metadata:
        surface_form, normalized_form, token_type, start_idx, end_idx.
        """
        tokens = []
        for match in self.TOKEN_REGEX.finditer(text):
            tok_text = match.group(0)
            if not tok_text:
                continue
            tok_type = match.lastgroup or "WORD"
            norm_form = tok_text.lower() if tok_type in ("LATIN_WORD", "ABBR") else tok_text

            tokens.append({
                "surface_form": tok_text,
                "normalized_form": norm_form,
                "token_type": tok_type,
                "start": match.start(),
                "end": match.end()
            })
        return tokens

tokenizer = MultilingualTokenizer()
