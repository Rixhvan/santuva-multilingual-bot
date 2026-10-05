# Multilingual NLP Evaluation Report (Benchmark Across 300 Sentences)

This report presents empirical evaluation results for the standalone Level 1 Multilingual Conversational Chatbot across **Sanskrit**, **English**, and **Tulu**.

---

## 1. Evaluation Methodology

A dedicated evaluation dataset consisting of **300 curated examples** (100 Sanskrit, 100 English, 100 Tulu) was constructed in `data/evaluation/`:
- `sa_100.json`: Classical Sanskrit in Devanagari, IAST transliteration, Sandhi compounds, noun case inflections (1-8), verb lakaras, and medical queries.
- `en_100.json`: Standard English, medical terminology, SMS slang abbreviations, syntax variations, and health complaints.
- `tu_100.json`: Tulu in Kannada script, Latin transliteration, code-switching with English (`"Doctor naale appointment idiya?"`), coastal informal slang (`"bro enna madthiya"`), and Dravidian morphological inflections.

The evaluation runner (`tests/evaluate_pipeline.py`) runs the complete end-to-end NLP pipeline on all 300 sentences and computes:
1. **Language Identification Accuracy (%)**
2. **Intent Classification Accuracy (%)**
3. **Named Entity Recognition (NER) Precision, Recall, and F1 Score (%)**
4. **Code-Switching Detection Accuracy (%)**

---

## 2. Summary Results Table

| Language | Test Samples | Language ID Accuracy | Intent Accuracy | NER Recall | NER Precision | NER F1 Score | Code-Switching Accuracy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sanskrit** (`sa`) | 100 | **99.0%** | **87.0%** | **96.55%** | 65.12% | **77.78%** | N/A |
| **English** (`en`) | 100 | **98.0%** | **76.0%** | **94.12%** | 59.26% | **72.73%** | N/A |
| **Tulu** (`tcy`) | 100 | **90.0%** | **72.0%** | **89.66%** | 80.00% | **84.55%** | **73.33%** |

---

## 3. Analysis by Language

### 3.1 Sanskrit (`sa`)
- **Language ID (99.0%)**: Unicode block identification combined with Sanskrit-specific phonological and morphological markers (visarga `ः`, avagraha `ऽ`, noun case markers `-स्य`, `-म्`, verb endings `-ति`, `-सि`, `-मि`) delivers near-perfect discrimination.
- **Intent Accuracy (87.0%)**: Strong semantic recognition of classical inquiries, health queries, greetings, and polite requests (`कृपया`, `ददातु`).
- **NER (F1: 77.78%)**: High recall (96.55%) across medical terminology (`चिकित्सकः`, `चिकित्सालयः`), deities/names (`रामः`, `कृष्णः`), and diseases (`शिरोवेदना`, `ज्वरः`).

### 3.2 English (`en`)
- **Language ID (98.0%)**: Accurate Latin script character distribution and functional word frequency analysis.
- **Intent Accuracy (76.0%)**: Robust classification across location queries, time queries, help requests, and informal SMS abbreviations.
- **NER (F1: 72.73%)**: 94.12% recall capturing doctor names, departments, body parts, and medical terminology.

### 3.3 Tulu (`tcy`)
- **Language ID (90.0%)**: Effectively discriminates Tulu from standard Kannada when written in Kannada script, and detects transliterated Latin-script Tulu.
- **Code-Switching (73.33%)**: Accurately flags mixed sentences like `"Doctor naale appointment idiya?"` as containing both English medical vocabulary and Tulu functional grammar.
- **NER (F1: 84.55%)**: High precision (80.0%) and recall (89.66%) on Tulu locations (`ಕುಡ್ಲ`, `ಉಡುಪಿ`), medical terms (`ದೋಕ್ತೆರ್`, `ದವಾಖಾನೆ`), and diseases (`ತರೆಬೇನೆ`, `ಬಂಜಿಬೇನೆ`).

---

## 4. Reproducing the Evaluation

Run the evaluation script from the repository root:

```powershell
$env:PYTHONIOENCODING = "utf-8"
python tests/evaluate_pipeline.py
```
