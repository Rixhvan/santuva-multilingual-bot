# Tulu NLP Resource Architecture & Transparency Report

## 1. Overview and Problem Statement

Tulu (ತುಳು / Tulu Bhashe) is an ancient Dravidian language spoken predominantly in coastal Karnataka (Tulu Nadu: Dakshina Kannada, Udupi) and northern Kerala (Kasaragod). Unlike English or Sanskrit, Tulu has significantly fewer digital corpora, open-source computational analyzers, annotated treebanks, or pre-trained models.

To treat Tulu as a **first-class language** without fabricating inaccurate grammatical certainty or pretending high-resource parity, this chatbot implements a **3-Tier Hybrid Computational Architecture**.

---

## 2. Three-Tier Support Declaration

| Capability | Support Tier | Description & Implementation |
| :--- | :--- | :--- |
| **Lexicon Lookup** | **FULL SUPPORT** | Configurable bidirectional lexicon (`data/lexicons/tulu_lexicon.json`) mapping surface forms in both Kannada script and Latin transliteration to canonical lemmas, POS, and semantic concepts. |
| **Script Normalization** | **FULL SUPPORT** | Unicode NFC normalization, Kannada character hygiene, whitespace cleaning, and elongated character reduction. |
| **Rule-Based Morphology** | **FULL SUPPORT** | Systematic Dravidian agglutinative affix stripping for nominal cases (Dative `-g`/`-k`, Locative `-d`/`-odu`, Genitive `-da`/`-ta`, Ablative `-ddu`), plurals (`-kulu`/`-gulu`), and verbal markers (`-pundu`, `-le`, `-ra`). |
| **Intent Mapping** | **FULL SUPPORT** | Direct mapping from Tulu interrogatives and communicative acts into the unified 18-intent ontology. |
| **Slang Normalization** | **FULL SUPPORT** | Normalization of coastal youth slang and colloquial expressions (`bro enna madthiya`, `mast`, `laik`, `enla`, `padchi`, `boduva`). |
| **Code-Switching Detection** | **PARTIAL SUPPORT** | Token-level language identification detecting sentences with mixed English-Tulu medical words (`"Doctor naale appointment idiya?"`). |
| **Dravidian Suffix Stemming** | **PARTIAL SUPPORT** | Morphological heuristic fallback for words not in the lexicon that exhibit regular Dravidian inflectional patterns. |
| **POS Tagging** | **PARTIAL SUPPORT** | Universal POS tagging inferred from morphological markers and closed-class functional particles. |
| **Named Entity Extraction** | **PARTIAL SUPPORT** | Gazetteer and token pattern extraction for coastal locations (`ಕುಡ್ಲ`, `ಉಡುಪಿ`), medical terms, dates, and names. |
| **Deep Statistical / LM** | **FALLBACK SUPPORT** | Subword character n-gram continuous semantic vector similarity mapped to multilingual concept anchors. |
| **Ambiguity Clarification** | **FALLBACK SUPPORT** | When confidence drops below threshold (0.50), the system asks for polite clarification in Tulu (`"ಎಂಕ್ ಸರಿಯಾದ್ ಅರ್ಥ ಆಯಿಜಿ. ದಯಮಲ್ತ್ ಕುಡೊರ ಪಣ್ಲೆ।"`) rather than hallucinating. |

---

## 3. Kannada Script vs Kannada Language Discrimination

A crucial requirement is: **Do NOT assume Kannada script automatically means Tulu.**

Kannada script is the primary contemporary writing system for Tulu, but standard Kannada also uses the same script. Our language detector evaluates lexical markers:

- **Tulu Identifiers**: `ದಾನೆ` (what), `ದಾಲ` (nothing), `ಇಜ್ಜಿ` (is not), `ಬೋಡು` (need), `ಬಲ್ಲಿ` (cannot), `ಎಂಚ` (how), `ಒವ್ವು` (which), `ವಾಡೆ` (where), `ಕುಡ್ಲ` (Mangalore), `ಆಪುಂಡು` (happens), `ಮಲ್ಪುಲೆ` (do).
- **Kannada Distinguishers**: `ಏನು` (what), `ಹೇಗೆ` (how), `ಎಲ್ಲಿ` (where), `ಯಾರು` (who), `ಬೇಕು` (need), `ಮಾಡುತ್ತೇನೆ` (I do), `ಆಗುತ್ತದೆ` (happens).

When standard Kannada is detected in Kannada script, the system alerts that Kannada was identified while Tulu was expected and prompts user confirmation.

---

## 4. Expanding the Tulu Lexicon

New words can be added directly to `data/lexicons/tulu_lexicon.json`:

```json
{
  "surface_forms": ["ಮರ್ದ್", "ಮರ್ದ್‌ನ್", "mard", "mardu"],
  "lemma": "ಮರ್ದ್",
  "pos": "NOUN",
  "concept": "MEDICINE",
  "meaning": "medicine",
  "morphology": {"gender": "neuter"},
  "resource_tier": "FULL"
}
```

The system re-indexes all entries automatically at initialization.
