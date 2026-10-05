# Santuva
### Sanskrit (संस्कृतम्) • English • Tulu (ತುಳು)

**Santuva** is a multilingual conversational chatbot focused on **Sanskrit**, **English**, and **Tulu**.

> **Strict Scope Restriction Compliance**:
> This project builds **ONLY Level 1** of a multilingual conversational chatbot. It is a standalone NLP system and deliberately contains **NO Hospital Management System (HMS), hospital database, appointment booking module, doctor database, billing module, patient management module, or clinical integration**. All dialogue is educational/general and can later be interfaced to external systems via REST APIs.

---

## Key Features

1. **Language Identification**: Script detection (Devanagari, Kannada, Latin, IAST), character n-grams, vocabulary frequency, and discriminative differentiation between **Tulu and Kannada**.
2. **Text & Unicode Normalization**: NFC normalization, elongated typing reduction (e.g. `heyyy` → `hey`), whitespace cleaning, preserving Sanskrit Danda (`।` / `॥`).
3. **Language-Aware Tokenization**: Segments words, numbers (Arabic, Devanagari, Kannada), dates, abbreviations, and Sanskrit punctuation.
4. **Sanskrit Computational Linguistics**:
   - Sandhi splitting (Dirgha, Guna, Vriddhi, Yan, Visarga, Anusvara) with confidence scores.
   - Noun case declensions (1 to 8: Nominative through Vocative).
   - Verb conjugations across Lat (present), Lot (imperative), and Lrt (future) Lakaras.
5. **Tulu Computational Linguistics**:
   - Both Kannada script and Latin transliteration support.
   - Dravidian agglutinative case morphology (dative, locative, genitive, ablative) and plural markers.
   - Transparent 3-tier resource architecture (FULL, PARTIAL, FALLBACK support).
6. **Code-Switching Support**: Token-level language attribution for mixed queries like `"Doctor naale appointment idiya?"`.
7. **Slang & Colloquial Normalization**: Coastal slang (`"bro enna madthiya"`, `"mast"`, `"laik"`) and SMS abbreviations.
8. **Language-Independent Intent Ontology**: 18 universal intents (`GREETING`, `LOCATION_QUERY`, `TIME_QUERY`, `INFORMATION_QUERY`, `HELP`, `EMERGENCY`, `COMPLAINT`, `INTRODUCTION`, `YES`, `NO`, etc.).
9. **Multilingual Semantic Vector Space**: Character and subword n-gram vector representations with cross-lingual concept centroids.
10. **Dialogue State & Short-Term Memory**: Turn tracking, accumulated entity memory, and anaphora resolution (resolving ambiguous pronouns like `"it"`).
11. **Language-Preserving Response Generation**: Responds in the user's detected language without crude round-trip translation.
12. **Learn How Santuva Understands You**: A friendly, step-by-step panel that shows how Santuva understands each message (words, base forms, word types, names, intent, sandhi splits, and confidence scores).

---

## Project Structure

```
multilingual_nlp_bot/
├── backend/
│   ├── api/                     # FastAPI REST API (app.py)
│   ├── config/                  # Settings and threshold configurations
│   ├── models/                  # Pydantic schemas (NLPAnalysis, ChatResponse, etc.)
│   ├── nlp/
│   │   ├── language_detection/  # Language & script identification
│   │   ├── normalization/       # Unicode, whitespace, and slang normalizer
│   │   ├── tokenization/        # Language-aware tokenizer & segmenter
│   │   ├── pos/                 # Multilingual POS tagger
│   │   ├── ner/                 # Modular Multilingual NER engine
│   │   ├── intent/              # 18-intent classification engine
│   │   ├── embeddings/          # Multilingual vector space & cosine similarity
│   │   ├── semantic/            # Unified semantic understanding & dialogue acts
│   │   ├── dialogue/            # Short-term memory, state tracking, anaphora
│   │   ├── response/            # Language-preserving response generator
│   │   └── languages/
│   │       ├── sanskrit/        # Sandhi splitting & noun/verb morphology
│   │       ├── english/         # English morphology & lemmatizer
│   │       ├── tulu/            # Tulu morphology & Dravidian suffix analyzer
│   │       └── code_switching.py# Token-level language attribution
│   └── services/                # Master NLP pipeline service (nlp_service.py)
├── data/
│   ├── lexicons/                # Curated Sanskrit, Tulu, English, and Slang lexicons
│   ├── intents/                 # Language-independent intent ontology
│   └── evaluation/              # 300 test sentences (sa_100.json, en_100.json, tu_100.json)
├── frontend/                    # Modern React + Vite + TypeScript Chat UI & Dashboard
├── tests/                       # Automated pipeline evaluation benchmark
└── docs/                        # Architecture, Tulu resources, and evaluation report
```

---

## Quickstart Guide

### 1. Start the Backend API (FastAPI)

```powershell
# In project root
$env:PYTHONIOENCODING = "utf-8"
uvicorn backend.api.app:app --reload --port 8000
```
API Documentation will be accessible at: `http://localhost:8000/docs`

### 2. Start the Frontend (React + Vite)

```powershell
cd frontend
npm run dev
```
Web Chatbot UI & Developer Dashboard will be accessible at: `http://localhost:5173`

### 3. Run Benchmark Evaluation (300 Sentences)

```powershell
$env:PYTHONIOENCODING = "utf-8"
python tests/evaluate_pipeline.py
```

Benchmark output:
- **Sanskrit Language ID**: 99.0% | **Intent Accuracy**: 87.0% | **NER Recall**: 96.55%
- **English Language ID**: 98.0% | **Intent Accuracy**: 76.0% | **NER Recall**: 94.12%
- **Tulu Language ID**: 90.0% | **Intent Accuracy**: 72.0% | **NER F1**: 84.55% | **Code-Switching**: 73.33%

---

## API Endpoints

- `POST /api/chat`: Processes a user message through the complete NLP pipeline and returns bot response, detected language, and full `nlp_analysis` metadata.
- `POST /api/reset`: Resets conversational memory for a given session.
- `GET /api/info`: Returns supported languages, scripts, confidence thresholds, and Tulu resource tiers.
