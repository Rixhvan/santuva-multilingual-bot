import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.nlp.language_detection.detector import language_detector
from backend.nlp.normalization.normalizer import normalizer
from backend.nlp.normalization.slang import slang_normalizer
from backend.nlp.tokenization.tokenizer import tokenizer
from backend.nlp.languages.sanskrit.sandhi import sandhi_engine
from backend.nlp.languages.sanskrit.morphology import sa_morphology
from backend.nlp.languages.tulu.morphology import tulu_morphology
from backend.nlp.languages.english.morphology import en_morphology
from backend.nlp.pos.tagger import pos_tagger
from backend.nlp.ner.recognizer import ner_engine
from backend.nlp.intent.classifier import intent_classifier
from backend.nlp.dialogue.memory import conversation_memory
from backend.nlp.languages.code_switching import code_switching_handler

class TestMultilingualNLP(unittest.TestCase):

    def test_language_detection_sanskrit(self):
        res = language_detector.identify_language("मम नाम रामः।")
        self.assertEqual(res.language_code, "sa")
        self.assertEqual(res.script, "Devanagari")
        self.assertGreater(res.confidence, 0.8)

    def test_language_detection_english(self):
        res = language_detector.identify_language("Where is the hospital?")
        self.assertEqual(res.language_code, "en")
        self.assertEqual(res.script, "Latin")

    def test_language_detection_tulu_kannada(self):
        res = language_detector.identify_language("ದೋಕ್ತೆರ್ ವಾಡೆ ಉಲ್ಲೆರ್?")
        self.assertEqual(res.language_code, "tcy")
        self.assertEqual(res.script, "Kannada")

    def test_tulu_vs_kannada_discrimination(self):
        # Standard Kannada markers should trigger Kannada and request clarification
        res = language_detector.identify_language("ನೀವು ಎಲ್ಲಿ ಹೋಗುತ್ತೀರಿ?")
        self.assertEqual(res.language_code, "kn")
        self.assertTrue(res.needs_clarification)

    def test_normalization_repeated_chars(self):
        text, _ = normalizer.normalize("heyyyy doc! pleaaase help")
        self.assertEqual(text, "hey doc! please help")

    def test_tokenization_sanskrit_danda(self):
        toks = tokenizer.tokenize_raw("मम नाम रामः।")
        self.assertEqual(toks, ["मम", "नाम", "रामः", "।"])

    def test_sanskrit_sandhi_splitting(self):
        item = sandhi_engine.analyze_word("सूर्योदयः")
        self.assertIsNotNone(item)
        self.assertEqual(item.components, ["सूर्य", "उदयः"])
        self.assertIn("guna_sandhi", item.rule_type)

    def test_sanskrit_morphology_cases(self):
        # Genitive case test: रामस्य
        res = sa_morphology.analyze("रामस्य")
        self.assertEqual(res["lemma"], "राम")
        self.assertEqual(res["morphology"].get("case"), "genitive")

    def test_tulu_morphology_locative(self):
        res = tulu_morphology.analyze("ಕುಡ್ಲಡ್")
        self.assertEqual(res["lemma"], "ಕುಡ್ಲ")
        self.assertEqual(res["concept"], "MANGALORE")

    def test_english_lemmatization(self):
        res = en_morphology.analyze("feeling")
        self.assertEqual(res["lemma"], "feel")
        self.assertEqual(res["pos"], "VERB")

    def test_pos_tagger_universal(self):
        tok = {"surface_form": "doctor", "token_type": "WORD"}
        res = pos_tagger.tag_token(tok, "en")
        self.assertEqual(res["pos"], "NOUN")

    def test_named_entity_recognition(self):
        toks = tokenizer.tokenize("Where is the hospital?")
        entities = ner_engine.extract_entities("Where is the hospital?", toks, "en")
        labels = [e.label for e in entities]
        self.assertIn("MEDICAL_TERM", labels)

    def test_code_switching_detection(self):
        toks = tokenizer.tokenize("Doctor naale appointment idiya?")
        is_switched, langs, _ = code_switching_handler.analyze_tokens(toks)
        self.assertTrue(is_switched)
        self.assertIn("English", langs)
        self.assertIn("Tulu", langs)

    def test_slang_normalization(self):
        norm_text, modified, _ = slang_normalizer.normalize_slang("bro enna madthiya?")
        self.assertTrue(modified)
        self.assertIn("malpuva", norm_text)

    def test_anaphora_resolution(self):
        conversation_memory.clear("test_session")
        conversation_memory.update_state(
            session_id="test_session",
            user_text="Tell me about Sanskrit.",
            bot_response="Sanskrit is an ancient language.",
            lang="English",
            intent="INFORMATION_QUERY",
            entities={},
            topic="Sanskrit"
        )
        resolved, was_res, ant = conversation_memory.resolve_anaphora("When was it used?", "test_session")
        self.assertTrue(was_res)
        self.assertEqual(ant, "Sanskrit")
        self.assertIn("Sanskrit", resolved)

if __name__ == "__main__":
    unittest.main()
