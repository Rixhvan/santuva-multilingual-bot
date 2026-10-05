import json
import re
from typing import Tuple, List, Dict, Any
from backend.config.settings import LEXICONS_DIR

class SlangNormalizer:
    """
    Slang and Informal Language Normalization Layer.
    Detects and normalizes colloquialisms, chat abbreviations, and coastal informal slang
    (e.g., 'bro enna madthiya', 'mast', 'laik', 'plz', 'idk') into canonical semantic equivalents.
    """

    def __init__(self):
        self.slang_map: Dict[str, Dict[str, str]] = {}
        self._load_slang_lexicon()

    def _load_slang_lexicon(self):
        slang_path = LEXICONS_DIR / "slang_lexicon.json"
        if slang_path.exists():
            with open(slang_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("slang_mappings", []):
                    self.slang_map[item["slang"].lower()] = item

    def normalize_slang(self, text: str) -> Tuple[str, bool, List[Dict[str, str]]]:
        """
        Scans text for informal slang and replaces known colloquialisms.
        Returns: (normalized_text, was_modified, list_of_transformations)
        """
        text_lower = text.lower().strip()
        transformations = []
        modified = False
        result_text = text

        # 1. Multi-word slang checks first (e.g., "enna madthiya", "idk")
        for slang_key, item in sorted(self.slang_map.items(), key=lambda x: -len(x[0])):
            pattern = rf'\b{re.escape(slang_key)}\b'
            if re.search(pattern, result_text, re.IGNORECASE):
                norm_val = item["normalized"]
                result_text = re.sub(pattern, norm_val, result_text, flags=re.IGNORECASE)
                modified = True
                transformations.append({
                    "slang": slang_key,
                    "normalized": norm_val,
                    "concept": item.get("concept", "INFORMAL")
                })

        return result_text, modified, transformations

slang_normalizer = SlangNormalizer()
