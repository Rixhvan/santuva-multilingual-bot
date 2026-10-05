# Multilingual NLP Chatbot Architecture (Level 1)

This document provides a comprehensive technical overview of the computational linguistics and NLP pipeline implemented for **Sanskrit**, **English**, and **Tulu**.

---

## 1. High-Level Pipeline Flow

```
User Input
    ↓
Language Identification (Script + Character n-grams + Lexical Markers + Kannada vs Tulu Differentiator)
    ↓
Unicode & Text Normalization (NFC, Whitespace, Diacritics, Elongated Character Compression)
    ↓
Slang & Informal Normalization (bro, enna madthiya, mast, laik, plz, idk)
    ↓
Language-Aware Tokenization & Sentence Segmentation (Devanagari, Kannada, Latin, Sanskrit Danda ।/॥, Numbers)
    ↓
Code-Switching Detection & Token-Level Language Attribution
    ↓
Morphological & Lexical Analysis / Lemmatization:
    ├── Sanskrit: Case declensions (1-8), Verb conjugations (Lat/Lot/Lrt), Sandhi splitting
    ├── English: Irregular verbs, Pluralization, Verb inflections (-ed, -ing)
    └── Tulu: Dravidian agglutinative suffixes (cases, plurals, verb endings, question particles)
    ↓
Part-of-Speech Tagging (Universal POS: NOUN, VERB, ADJ, ADV, PRON, PARTICLE, CONJ, DET, INTJ, PROPN, NUM)
    ↓
Named Entity Recognition (Modular Multilingual: PERSON, LOCATION, MEDICAL_TERM, DISEASE, MEDICINE, etc.)
    ↓
Intent Classification (18 Language-Independent Intents + Confidence Scoring)
    ↓
Multilingual Semantic Understanding (Dialogue Act, Cross-Lingual Concept Anchors, Vector Space)
    ↓
Context Tracking & Short-Term Memory (Turn buffer, accumulated entities, anaphora resolution for 'it')
    ↓
Dialogue State Management (Language switch directives, ambiguity detection, clarification requests)
    ↓
Response Generation (Language-preserving: Sanskrit→Sanskrit, English→English, Tulu→Tulu)
    ↓
Response Validation & Metadata Packaging
```

---

## 2. Component Details

### 2.1 Language Identification (`backend/nlp/language_detection/detector.py`)
- **Script Analysis**: Identifies Unicode blocks for Devanagari (`0x0900 - 0x097F`), Kannada (`0x0C80 - 0x0CFF`), and Latin (`0x0041 - 0x007A` + IAST diacritics).
- **Kannada Script Distinction**: Explicitly does **not** assume Kannada script implies Kannada. Differentiates Tulu lexical markers (`ದಾನೆ`, `ದಾಲ`, `ಇಜ್ಜಿ`, `ಬೋಡು`, `ಎಂಚ`, `ವಾಡೆ`, `ಕುಡ್ಲ`, etc.) from Kannada markers (`ಏನು`, `ಹೇಗೆ`, `ಎಲ್ಲಿ`, `ಬೇಕು`, `ಮಾಡುತ್ತೇನೆ`). When standard Kannada is detected, flags low confidence and requests clarification.
- **Latin Transliteration**: Detects Latin-script Sanskrit (IAST), Latin-script Tulu (`encha uller`, `daane`, `bodu`, `kudla`, `mard`), and English.
- **Code-Switching Detection**: Detects sentences containing vocabulary from multiple languages (e.g., `"Doctor naale appointment idiya?"`).

### 2.2 Text Normalization (`backend/nlp/normalization/normalizer.py`)
- **Unicode NFC**: Normalizes precomposed and combining characters.
- **Repeated Character Reduction**: Compresses informal elongation (`heyyyy` → `hey`, `pleaaase` → `please`) while preserving geminated consonants critical to Sanskrit and Dravidian morphology.
- **Punctuation Hygiene**: Replaces typographic smart quotes and dashes while preserving Sanskrit Danda (`।` U+0964) and double danda (`॥` U+0965).

### 2.3 Tokenization (`backend/nlp/tokenization/tokenizer.py`)
- Language-aware regular expressions recognizing words across Devanagari, Kannada, and Latin scripts.
- Preserves numbers in Arabic (`0-9`), Devanagari (`०-९`), and Kannada (`೦-೯`).
- Recognizes dates, medical terminology, and abbreviations (`Dr.`, `Prof.`).

### 2.4 Sanskrit Morphological & Sandhi Processing (`backend/nlp/languages/sanskrit/`)
- **Sandhi Splitting**: Handles Dirgha, Guna, Vriddhi, Yan, Visarga, and Anusvara Sandhi (e.g., `सूर्योदयः` → `सूर्य + उदयः`, `चिकित्सालयः` → `चिकित्सा + आलयः`, `रामोऽस्ति` → `रामः + अस्ति`, `नमस्ते` → `नमः + ते`).
- **Nominal Cases**: Maps a-stem masculine, neuter, and ā-stem feminine noun forms across nominative through vocative (e.g., `रामस्य` → lemma: `राम`, case: `genitive`, number: `singular`, gender: `masculine`).
- **Verb Conjugations**: Analyzes Lat Lakara (present), Lot Lakara (imperative), and Lrt Lakara (future) person and number endings.

### 2.5 Tulu Morphological Processing (`backend/nlp/languages/tulu/`)
- Supports Kannada script and Latin transliteration.
- Analyzes Dravidian agglutinative case endings:
  - Dative: `-ಗ್` / `-g`, `-ರೆಗ್` / `-reg`
  - Locative: `-ಡ್` / `-d`, `-ೊಡು` / `-odu`
  - Genitive: `-ದ` / `-da`, `-ತ` / `-ta`
  - Ablative: `-ಡ್ದ್` / `-ddu`
  - Plural: `-ಕುಲು` / `-kulu`, `-ಗುಲು` / `-gulu`
  - Question marker: `-ರಾ` / `-ra`, `-ಡಾ` / `-da`

### 2.6 Intent Classification (`backend/nlp/intent/classifier.py`)
Maps all three languages into 18 language-independent intents:
- `GREETING`, `FAREWELL`, `THANKS`, `INTRODUCTION`, `HELP`, `GENERAL_QUESTION`, `LOCATION_QUERY`, `TIME_QUERY`, `INFORMATION_QUERY`, `REQUEST`, `CONFIRMATION`, `DENIAL`, `YES`, `NO`, `COMPLAINT`, `FEEDBACK`, `EMERGENCY`, `UNKNOWN`.

### 2.7 Multilingual Semantic Vector Space (`backend/nlp/embeddings/vector_space.py`)
- Sparse subword and character n-gram continuous representations.
- Aligned cross-lingual semantic concept centroids (FATIGUE, DOCTOR, HOSPITAL, HELP, TIME, LOCATION).
- Real cosine similarity calculations providing language-independent semantic similarity.

### 2.8 Dialogue Management & Context Memory (`backend/nlp/dialogue/`)
- Tracks session conversation turns, current topic, and accumulated entities.
- Performs anaphora resolution (e.g. resolving `"When was it used?"` to `"When was Sanskrit used?"` based on topic).
- Triggers clarification when ambiguous pronouns have no antecedent.
- Detects explicit language-switching commands (e.g. `"संस्कृतेन उत्तरं ददातु"`).

### 2.9 Language-Preserving Response Generation (`backend/nlp/response/generator.py`)
- Sanskrit query → Sanskrit response.
- English query → English response.
- Tulu query → Tulu response (in Kannada script or Latin script matching user input).
- Maintains polite, respectful chatbot persona without unsupported clinical claims.
