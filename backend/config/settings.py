import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
LEXICONS_DIR = DATA_DIR / "lexicons"
INTENTS_DIR = DATA_DIR / "intents"
EVALUATION_DIR = DATA_DIR / "evaluation"

class Settings(BaseModel):
    app_name: str = "Multilingual NLP Chatbot (Sanskrit - English - Tulu)"
    version: str = "1.0.0"
    debug: bool = True
    
    # Confidence thresholds
    lang_confidence_threshold: float = 0.60
    intent_confidence_threshold: float = 0.55
    clarification_threshold: float = 0.50
    ambiguity_margin: float = 0.12
    
    # Supported Languages
    supported_languages: list[str] = ["en", "sa", "tcy"]
    language_names: dict[str, str] = {
        "en": "English",
        "sa": "Sanskrit",
        "tcy": "Tulu"
    }
    
    # Supported Scripts
    supported_scripts: list[str] = ["Latin", "Devanagari", "Kannada", "IAST"]
    
    # Tulu Resource Tier Declaration
    tulu_resource_tiers: dict[str, str] = {
        "lexicon_lookup": "FULL SUPPORT",
        "script_normalization": "FULL SUPPORT",
        "rule_based_morphology": "FULL SUPPORT",
        "intent_mapping": "FULL SUPPORT",
        "slang_normalization": "FULL SUPPORT",
        "code_switching_detection": "PARTIAL SUPPORT",
        "dravidian_suffix_stemming": "PARTIAL SUPPORT",
        "pos_tagging": "PARTIAL SUPPORT",
        "ner_extraction": "PARTIAL SUPPORT",
        "statistical_lm": "FALLBACK SUPPORT",
        "deep_semantic_embeddings": "FALLBACK SUPPORT"
    }
    
    # Paths
    lexicons_dir: Path = LEXICONS_DIR
    intents_dir: Path = INTENTS_DIR
    evaluation_dir: Path = EVALUATION_DIR

settings = Settings()
