export interface TokenInfo {
  surface_form: string;
  normalized_form: string;
  lemma: string;
  pos: string;
  morphology: Record<string, any>;
  sandhi_components?: string[];
  language?: string;
  is_stopword?: boolean;
  semantic_concept?: string | null;
}

export interface EntityInfo {
  text: string;
  label: string;
  start: number;
  end: number;
  confidence: number;
}

export interface IntentInfo {
  intent: string;
  confidence: number;
  secondary_intent?: string | null;
  all_scores?: Record<string, number>;
}

export interface LanguageInfo {
  language: string;
  language_code: string;
  script: string;
  confidence: number;
  is_code_switched: boolean;
  code_switched_languages: string[];
  needs_clarification: boolean;
  details?: Record<string, any>;
}

export interface SemanticRepresentation {
  language: string;
  intent: string;
  entities: Record<string, any>;
  dialogue_act: string;
  concepts: string[];
  confidence: number;
  shared_concept_id?: string | null;
}

export interface SandhiSplittingItem {
  compound: string;
  components: string[];
  rule_type: string;
  confidence: number;
  meaning?: string | null;
}

export interface WordGloss {
  token: string;
  lemma: string;
  gloss: string;
  grammar_note: string;
}

export interface NLPAnalysis {
  original_text: string;
  normalized_text: string;
  language_info: LanguageInfo;
  tokens: TokenInfo[];
  entities: EntityInfo[];
  intent_info: IntentInfo;
  semantic_rep: SemanticRepresentation;
  sandhi_analysis: SandhiSplittingItem[];
  code_switching_tokens: Array<{ token: string; language: string; type: string }>;
  slang_normalized: boolean;
  slang_transformations: Array<{ slang: string; normalized: string; concept: string }>;
  english_translation?: string | null;
  word_glosses?: WordGloss[];
  translation_confidence?: number | null;
}

export interface DialogueState {
  conversation_id: string;
  turn_count: number;
  current_topic?: string | null;
  last_intent?: string | null;
  accumulated_entities: Record<string, string>;
  previous_language?: string | null;
  clarification_pending: boolean;
  recent_turns: any[];
}

export interface ChatResponse {
  response_text: string;
  detected_language: string;
  response_language: string;
  confidence: number;
  nlp_analysis: NLPAnalysis;
  response_nlp_analysis?: NLPAnalysis | null;
  dialogue_state: DialogueState;
  clarification_requested: boolean;
}

export interface MessageItem {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
  response?: ChatResponse;
  nlpAnalysis?: NLPAnalysis;
  dialogueState?: DialogueState;
  analysisSource?: 'request' | 'response';
}

export interface BenchmarkMetric {
  language: string;
  language_code: string;
  total_samples: number;
  language_accuracy: number;
  intent_accuracy: number;
  entity_precision: number;
  entity_recall: number;
  entity_f1: number;
  code_switching_accuracy: number | string;
}
