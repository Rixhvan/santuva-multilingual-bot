from typing import Dict, Any, Optional
from backend.models.schemas import (
    NLPAnalysis, TokenInfo, EntityInfo, IntentInfo,
    LanguageInfo, SemanticRepresentation, DialogueState,
    ChatResponse, SandhiSplittingItem
)
from backend.nlp.language_detection.detector import language_detector
from backend.nlp.normalization.normalizer import normalizer
from backend.nlp.normalization.slang import slang_normalizer
from backend.nlp.tokenization.tokenizer import tokenizer
from backend.nlp.pos.tagger import pos_tagger
from backend.nlp.ner.recognizer import ner_engine
from backend.nlp.intent.classifier import intent_classifier
from backend.nlp.semantic.understander import semantic_understander
from backend.nlp.dialogue.manager import dialogue_manager
from backend.nlp.dialogue.memory import conversation_memory
from backend.nlp.response.generator import response_generator
from backend.nlp.languages.code_switching import code_switching_handler
from backend.nlp.languages.sanskrit.sandhi import sandhi_engine
from backend.nlp.translation.translator import translator
from backend.config.settings import settings

class NLPService:
    """
    Master Multilingual NLP Pipeline Orchestrator.
    Integrates all 20 phases into an end-to-end computational pipeline.
    """

    def process_query(
        self,
        raw_text: str,
        session_id: str = "default",
        user_selected_lang: Optional[str] = None
    ) -> ChatResponse:
        """Runs the entire Level 1 Multilingual NLP Pipeline."""

        # 1. Unicode & Text Normalization
        normalized_text, norm_transformations = normalizer.normalize(raw_text)

        # 2. Slang & Informal Handling
        slang_text, was_slang_modified, slang_records = slang_normalizer.normalize_slang(normalized_text)

        # 3. Language Identification
        lang_info = language_detector.identify_language(raw_text)

        # Override with user manual selection if provided
        if user_selected_lang and user_selected_lang in settings.supported_languages:
            lang_info.language_code = user_selected_lang
            lang_info.language = settings.language_names[user_selected_lang]
            lang_info.confidence = 1.0
            lang_info.needs_clarification = False

        # 4. Tokenization & Sentence Segmentation
        raw_tokens = tokenizer.tokenize(slang_text if was_slang_modified else normalized_text)

        # 5. Code-Switching Detection
        is_switched, switched_langs, code_switch_records = code_switching_handler.analyze_tokens(raw_tokens)
        if is_switched:
            lang_info.is_code_switched = True
            lang_info.code_switched_languages = switched_langs

        # 6. Part-of-Speech Tagging & Morphological Analysis
        tagged_tokens = pos_tagger.tag_tokens(raw_tokens, lang_info.language_code)

        # Build TokenInfo objects
        token_infos = []
        for t in tagged_tokens:
            token_infos.append(TokenInfo(
                surface_form=t.get("surface_form", ""),
                normalized_form=t.get("normalized_form", ""),
                lemma=t.get("lemma", t.get("surface_form", "")),
                pos=t.get("pos", "NOUN"),
                morphology=t.get("morphology", {}),
                sandhi_components=t.get("sandhi_components", []),
                language=lang_info.language,
                semantic_concept=t.get("concept")
            ))

        # 7. Sanskrit-Specific Sandhi Analysis
        sandhi_items: list[SandhiSplittingItem] = []
        if lang_info.language_code == "sa":
            token_surfaces = [t.get("surface_form", "") for t in raw_tokens]
            sandhi_items = sandhi_engine.process_sentence(token_surfaces)

        # 8. Named Entity Recognition
        entities = ner_engine.extract_entities(
            slang_text,
            raw_tokens,
            lang_info.language_code
        )

        # 9. Intent Classification
        intent_info = intent_classifier.classify(
            slang_text,
            tagged_tokens,
            lang_info.language_code
        )

        # 10. Semantic Understanding & Dialogue Act
        semantic_rep = semantic_understander.build_semantic_representation(
            slang_text,
            lang_info.language,
            intent_info,
            entities,
            tagged_tokens
        )

        # 11. Dialogue State & Context Resolution
        dialogue_state, requires_clarif, clarif_prompt, detected_topic = dialogue_manager.process_turn(
            session_id,
            raw_text,
            lang_info,
            intent_info,
            entities
        )

        # 12. Response Generation
        bot_response = response_generator.generate_response(
            semantic_rep=semantic_rep,
            dialogue_state=dialogue_state,
            target_lang_code=lang_info.language_code,
            script=lang_info.script,
            clarification_msg=clarif_prompt
        )

        # 13. Update Short-Term Conversation Memory
        conversation_memory.update_state(
            session_id=session_id,
            user_text=raw_text,
            bot_response=bot_response,
            lang=lang_info.language,
            intent=intent_info.intent,
            entities=semantic_rep.entities,
            topic=detected_topic
        )

        # 14. English Translation & Word Glosses
        eng_translation, word_glosses, trans_conf = translator.translate_to_english(
            raw_text=raw_text,
            lang_code=lang_info.language_code,
            tokens=raw_tokens,
            intent=intent_info.intent,
            is_bot_response=False
        )

        # 15. Assemble Complete NLP Analysis Object
        nlp_analysis = NLPAnalysis(
            original_text=raw_text,
            normalized_text=normalized_text,
            language_info=lang_info,
            tokens=token_infos,
            entities=entities,
            intent_info=intent_info,
            semantic_rep=semantic_rep,
            sandhi_analysis=sandhi_items,
            code_switching_tokens=code_switch_records,
            slang_normalized=was_slang_modified,
            slang_transformations=slang_records,
            english_translation=eng_translation,
            word_glosses=word_glosses,
            translation_confidence=trans_conf
        )

        # 16. Build NLP Analysis for the Bot Response (Requirement 1)
        resp_tokens_raw = tokenizer.tokenize(bot_response)
        resp_tagged_tokens = pos_tagger.tag_tokens(resp_tokens_raw, lang_info.language_code)
        resp_token_infos = [
            TokenInfo(
                surface_form=t.get("surface_form", ""),
                normalized_form=t.get("normalized_form", ""),
                lemma=t.get("lemma", t.get("surface_form", "")),
                pos=t.get("pos", "NOUN"),
                morphology=t.get("morphology", {}),
                language=lang_info.language,
                semantic_concept=t.get("concept")
            ) for t in resp_tagged_tokens
        ]
        resp_entities = ner_engine.extract_entities(bot_response, resp_tokens_raw, lang_info.language_code)
        resp_intent_info = IntentInfo(intent=intent_info.intent, confidence=0.98)
        resp_sem_rep = semantic_understander.build_semantic_representation(
            bot_response, lang_info.language, resp_intent_info, resp_entities, resp_tagged_tokens
        )
        resp_eng_trans, resp_word_glosses, resp_trans_conf = translator.translate_to_english(
            raw_text=bot_response,
            lang_code=lang_info.language_code,
            tokens=resp_tokens_raw,
            intent=intent_info.intent,
            is_bot_response=True
        )
        resp_nlp_analysis = NLPAnalysis(
            original_text=bot_response,
            normalized_text=bot_response,
            language_info=lang_info,
            tokens=resp_token_infos,
            entities=resp_entities,
            intent_info=resp_intent_info,
            semantic_rep=resp_sem_rep,
            english_translation=resp_eng_trans,
            word_glosses=resp_word_glosses,
            translation_confidence=resp_trans_conf
        )

        return ChatResponse(
            response_text=bot_response,
            detected_language=lang_info.language,
            response_language=lang_info.language,
            confidence=round(min(lang_info.confidence, intent_info.confidence), 2),
            nlp_analysis=nlp_analysis,
            response_nlp_analysis=resp_nlp_analysis,
            dialogue_state=dialogue_state,
            clarification_requested=requires_clarif
        )

nlp_service = NLPService()
