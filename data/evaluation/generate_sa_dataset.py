import json
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent

# --- 100 SANSKRIT EXAMPLES ---
sa_samples = []

# Greetings (10)
greetings_sa = [
    ("नमस्ते", "GREETING", {}),
    ("नमो नमः", "GREETING", {}),
    ("सुप्रभातम्", "GREETING", {}),
    ("शुभदिनम्", "GREETING", {}),
    ("शुभरात्रिः", "GREETING", {}),
    ("प्रणामः", "GREETING", {}),
    ("सर्वेभ्यः नमस्कारः", "GREETING", {}),
    ("भो मित्र, नमो नमः", "GREETING", {}),
    ("सुस्वागतम्", "GREETING", {}),
    ("नमस्ते भवतः", "GREETING", {})
]
for text, intent, ent in greetings_sa:
    sa_samples.append({"text": text, "language": "sa", "intent": intent, "entities": ent, "category": "greeting"})

# Questions & Location/Time (25)
q_sa = [
    ("चिकित्सकः कुत्र अस्ति?", "LOCATION_QUERY", {"medical_term": "चिकित्सकः"}),
    ("चिकित्सालयः कुत्र अस्ति?", "LOCATION_QUERY", {"medical_term": "चिकित्सालयः"}),
    ("मार्गः कुत्र अस्ति?", "LOCATION_QUERY", {}),
    ("औषधालयः कुत्र वर्तते?", "LOCATION_QUERY", {}),
    ("प्रवेशद्वारं कुत्र अस्ति?", "LOCATION_QUERY", {}),
    ("कदा चिकित्सकः आगमिष्यति?", "TIME_QUERY", {"medical_term": "चिकित्सकः"}),
    ("चिकित्सालयस्य समयः कः?", "TIME_QUERY", {"medical_term": "चिकित्सालयस्य"}),
    ("परामर्शस्य समयः कति?", "TIME_QUERY", {}),
    ("कदा औषधं स्वीकर्तव्यम्?", "TIME_QUERY", {"medicine": "औषधं"}),
    ("कः समयः अस्ति?", "TIME_QUERY", {}),
    ("चिकित्सकस्य विषये ज्ञातुम् इच्छामि।", "INFORMATION_QUERY", {"medical_term": "चिकित्सकस्य"}),
    ("संस्कृतभाषायाः विषये वदतु।", "INFORMATION_QUERY", {"language": "संस्कृतभाषायाः"}),
    ("औषधस्य विषये सूचनां ददातु।", "INFORMATION_QUERY", {"medicine": "औषधस्य"}),
    ("मम विवरणं किम् अस्ति?", "INFORMATION_QUERY", {}),
    ("स्वास्थ्यस्य विषये किं कर्तव्यम्?", "INFORMATION_QUERY", {}),
    ("किं भवान् मां जानाति?", "GENERAL_QUESTION", {}),
    ("कथम् अस्ति भवान्?", "GENERAL_QUESTION", {}),
    ("अद्य कः दिवसः?", "TIME_QUERY", {}),
    ("कः अत्र अधिकारी?", "GENERAL_QUESTION", {}),
    ("चिकित्सकः उपलभ्यते वा?", "INFORMATION_QUERY", {"medical_term": "चिकित्सकः"}),
    ("किं मया अत्र प्रतीक्षणीयं वा?", "GENERAL_QUESTION", {}),
    ("रुग्णालयः कदा उद्घाट्यते?", "TIME_QUERY", {"medical_term": "रुग्णालयः"}),
    ("कति वैद्याः सन्ति?", "GENERAL_QUESTION", {"medical_term": "वैद्याः"}),
    ("परीक्षणस्य फलं कदा आगमिष्यति?", "TIME_QUERY", {}),
    ("मम प्रतिवेदनं कुत्र अस्ति?", "LOCATION_QUERY", {})
]
for text, intent, ent in q_sa:
    sa_samples.append({"text": text, "language": "sa", "intent": intent, "entities": ent, "category": "question"})

# Requests & Help (15)
req_sa = [
    ("कृपया साहाय्यं करोतु।", "HELP", {}),
    ("अहं साहाय्यम् इच्छामि।", "HELP", {}),
    ("मां साहाय्यं कुरु।", "HELP", {}),
    ("कृपया मार्गं दर्शयतु।", "HELP", {}),
    ("कृपया चिकित्सकं सूचयतु।", "REQUEST", {"medical_term": "चिकित्सकं"}),
    ("कृपया औषधं ददातु।", "REQUEST", {"medicine": "औषधं"}),
    ("कृपया जलं ददातु।", "REQUEST", {}),
    ("कृपया पुनः वदतु।", "REQUEST", {}),
    ("मां विवरणं ददातु।", "REQUEST", {}),
    ("कृपया अत्र आगच्छतु।", "REQUEST", {}),
    ("कृपया प्रतीक्षां करोतु।", "REQUEST", {}),
    ("साहाय्यार्थं प्रार्थये।", "HELP", {}),
    ("कृपया इदं पठतु।", "REQUEST", {}),
    ("कृपया उच्चैः वदतु।", "REQUEST", {}),
    ("कृपया स्पष्टीकरोतु।", "REQUEST", {})
]
for text, intent, ent in req_sa:
    sa_samples.append({"text": text, "language": "sa", "intent": intent, "entities": ent, "category": "request_help"})

# Sandhi & Classical Compounds (15)
sandhi_sa = [
    ("सूर्योदयः कदा भवति?", "TIME_QUERY", {}),
    ("चिकित्सालयं गच्छामि।", "INFORMATION_QUERY", {"medical_term": "चिकित्सालयं"}),
    ("मम शिरोवेदना अस्ति।", "COMPLAINT", {"disease": "शिरोवेदना"}),
    ("उदरवेदना बाधते।", "COMPLAINT", {"disease": "उदरवेदना"}),
    ("अत्र कोऽपि नास्ति।", "GENERAL_QUESTION", {}),
    ("रामोऽस्ति मम सखा।", "INTRODUCTION", {"person": "रामोऽस्ति"}),
    ("कृतज्ञोऽस्मि भवतः साहाय्येन।", "THANKS", {}),
    ("पुनर्मिलामः सर्वे।", "FAREWELL", {}),
    ("महौषधं दातव्यम्।", "REQUEST", {"medicine": "महौषधं"}),
    ("इत्याह वैद्यः।", "STATEMENT", {"medical_term": "वैद्यः"}),
    ("अहं श्रान्तः अस्मि।", "COMPLAINT", {}),
    ("मम ज्वरः अस्ति।", "COMPLAINT", {"disease": "ज्वरः"}),
    ("नेत्रवेदना अस्ति।", "COMPLAINT", {}),
    ("दन्तपीडा अस्ति।", "COMPLAINT", {}),
    ("पादवेदना अस्ति।", "COMPLAINT", {})
]
for text, intent, ent in sandhi_sa:
    sa_samples.append({"text": text, "language": "sa", "intent": intent, "entities": ent, "category": "sandhi_morphology"})

# Introductions & Gratitude & Farewell (15)
intro_sa = [
    ("मम नाम रामः।", "INTRODUCTION", {"person": "रामः"}),
    ("मम नाम रमेशः।", "INTRODUCTION", {"person": "रमेशः"}),
    ("अहं कृष्णः अस्मि।", "INTRODUCTION", {"person": "कृष्णः"}),
    ("मम नाम प्रिया।", "INTRODUCTION", {}),
    ("अहं वैद्यः अस्मि।", "INTRODUCTION", {"medical_term": "वैद्यः"}),
    ("धन्यवादः भवतः।", "THANKS", {}),
    ("अतीव धन्यवादः।", "THANKS", {}),
    ("अनुगृहीतोऽस्मि।", "THANKS", {}),
    ("पुनर्मिलामः।", "FAREWELL", {}),
    ("शुभं भवतु।", "FAREWELL", {}),
    ("गमिष्यामि।", "FAREWELL", {}),
    ("आम्, सत्यम्।", "YES", {}),
    ("नहि नहि।", "NO", {}),
    ("एवमेव अस्ति।", "CONFIRMATION", {}),
    ("इदं न सम्यक्।", "DENIAL", {})
]
for text, intent, ent in intro_sa:
    sa_samples.append({"text": text, "language": "sa", "intent": intent, "entities": ent, "category": "intro_dialogue"})

# Transliteration / IAST / Variations (10)
translit_sa = [
    ("namaste", "GREETING", {}),
    ("katham asti bhavan?", "GENERAL_QUESTION", {}),
    ("mama nama Ramah.", "INTRODUCTION", {"person": "Ramah"}),
    ("chikitsakah kutra asti?", "LOCATION_QUERY", {"medical_term": "chikitsakah"}),
    ("dhanyavadah", "THANKS", {}),
    ("punarmilamah", "FAREWELL", {}),
    ("kripaya sahayyam karotu", "HELP", {}),
    ("aham shrantah asmi", "COMPLAINT", {}),
    ("aushadham kutra asti?", "LOCATION_QUERY", {"medicine": "aushadham"}),
    ("shubhadiinam", "GREETING", {})
]
for text, intent, ent in translit_sa:
    sa_samples.append({"text": text, "language": "sa", "intent": intent, "entities": ent, "category": "transliteration"})

# Emergency & Complaints (10)
emerg_sa = [
    ("आपत्कालः अस्ति!", "EMERGENCY", {}),
    ("शीघ्रं साहाय्यं कुरु!", "EMERGENCY", {}),
    ("त्राणम् त्राणम्!", "EMERGENCY", {}),
    ("रुग्णः अचेतनः जातः!", "EMERGENCY", {"medical_term": "रुग्णः"}),
    ("अतीव रक्तस्रावः भवति!", "EMERGENCY", {}),
    ("तीव्रज्वरः बाधते।", "COMPLAINT", {"disease": "तीव्रज्वरः"}),
    ("अहं कष्टे अस्मि।", "COMPLAINT", {}),
    ("श्वासकष्टम् अस्ति।", "COMPLAINT", {}),
    ("मम हृदयवेदना वर्तते।", "COMPLAINT", {}),
    ("अतीव दुर्बलः अस्मि।", "COMPLAINT", {})
]
for text, intent, ent in emerg_sa:
    sa_samples.append({"text": text, "language": "sa", "intent": intent, "entities": ent, "category": "emergency_complaint"})

assert len(sa_samples) == 100, f"Expected 100 Sanskrit samples, got {len(sa_samples)}"
with open(EVAL_DIR / "sa_100.json", "w", encoding="utf-8") as f:
    json.dump(sa_samples, f, ensure_ascii=False, indent=2)
print("Generated sa_100.json with 100 Sanskrit examples.")
