from typing import Optional, Any
from pydantic import BaseModel, Field

class TokenInfo(BaseModel):
    surface_form: str
    normalized_form: str
    lemma: str
    pos: str
    morphology: dict[str, Any] = Field(default_factory=dict)
    sandhi_components: list[str] = Field(default_factory=list)
    language: str = "unknown"
    is_stopword: bool = False
    semantic_concept: Optional[str] = None

class EntityInfo(BaseModel):
    text: str
    label: str
    start: int
    end: int
    confidence: float = 1.0

class IntentInfo(BaseModel):
    intent: str
    confidence: float
    secondary_intent: Optional[str] = None
    all_scores: dict[str, float] = Field(default_factory=dict)

class LanguageInfo(BaseModel):
    language: str
    language_code: str
    script: str
    confidence: float
    is_code_switched: bool = False
    code_switched_languages: list[str] = Field(default_factory=list)
    needs_clarification: bool = False
    details: dict[str, Any] = Field(default_factory=dict)

class SemanticRepresentation(BaseModel):
    language: str
    intent: str
    entities: dict[str, Any] = Field(default_factory=dict)
    dialogue_act: str
    concepts: list[str] = Field(default_factory=list)
    confidence: float
    shared_concept_id: Optional[str] = None

class SandhiSplittingItem(BaseModel):
    compound: str
    components: list[str]
    rule_type: str
    confidence: float
    meaning: Optional[str] = None

class NLPAnalysis(BaseModel):
    original_text: str
    normalized_text: str
    language_info: LanguageInfo
    tokens: list[TokenInfo]
    entities: list[EntityInfo]
    intent_info: IntentInfo
    semantic_rep: SemanticRepresentation
    sandhi_analysis: list[SandhiSplittingItem] = Field(default_factory=list)
    code_switching_tokens: list[dict[str, Any]] = Field(default_factory=list)
    slang_normalized: bool = False
    slang_transformations: list[dict[str, str]] = Field(default_factory=list)
    english_translation: Optional[str] = None
    word_glosses: list[dict[str, str]] = Field(default_factory=list)
    translation_confidence: Optional[float] = None

class DialogueState(BaseModel):
    conversation_id: str = "default"
    turn_count: int = 0
    current_topic: Optional[str] = None
    last_intent: Optional[str] = None
    accumulated_entities: dict[str, str] = Field(default_factory=dict)
    previous_language: Optional[str] = None
    clarification_pending: bool = False
    recent_turns: list[dict[str, Any]] = Field(default_factory=list)

class ChatRequest(BaseModel):
    text: str
    conversation_id: Optional[str] = "default"
    user_selected_language: Optional[str] = None

class ChatResponse(BaseModel):
    response_text: str
    detected_language: str
    response_language: str
    confidence: float
    nlp_analysis: NLPAnalysis
    response_nlp_analysis: Optional[NLPAnalysis] = None
    dialogue_state: DialogueState
    clarification_requested: bool = False
