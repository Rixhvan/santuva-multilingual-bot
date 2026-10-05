import json
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
tu_samples = []

# Greetings (10)
greetings_tu = [
    ("ನಮಸ್ಕಾರ!", "GREETING", {}),
    ("ನಮಸ್ಕಾರೊ", "GREETING", {}),
    ("ಸೊಲ್ಮೆಲು!", "GREETING", {}),
    ("namaskara", "GREETING", {}),
    ("solmelu", "GREETING", {}),
    ("ಎಂಚ ಉಲ್ಲೆರ್?", "GENERAL_QUESTION", {}),
    ("encha uller?", "GENERAL_QUESTION", {}),
    ("ಎಂಚ ಉಲ್ಲಾರ?", "GENERAL_QUESTION", {}),
    ("ದಾನೆ ವಿಶೇಷ?", "GENERAL_QUESTION", {}),
    ("daane vishesha?", "GENERAL_QUESTION", {})
]
for text, intent, ent in greetings_tu:
    tu_samples.append({"text": text, "language": "tcy", "intent": intent, "entities": ent, "category": "greeting"})

# Questions & Location/Time/Info (Kannada script) (20)
q_tu_kn = [
    ("ದೋಕ್ತೆರ್ ವಾಡೆ ಉಲ್ಲೆರ್?", "LOCATION_QUERY", {"medical_term": "ದೋಕ್ತೆರ್"}),
    ("ದವಾಖಾನೆ ವಾಡೆ ಉಂಡು?", "LOCATION_QUERY", {"medical_term": "ದವಾಖಾನೆ"}),
    ("ಆಸ್ಪತ್ರೆ ಓಡೆ ಉಂಡು?", "LOCATION_QUERY", {"medical_term": "ಆಸ್ಪತ್ರೆ"}),
    ("ಕುಡ್ಲಡ್ ದವಾಖಾನೆ ವಾಡೆ ಉಂಡು?", "LOCATION_QUERY", {"location": "ಕುಡ್ಲಡ್", "medical_term": "ದವಾಖಾನೆ"}),
    ("ಮರ್ದ್ ಅಂಗಡಿ ವಾಡೆ ತಿಕ್ಕುಂಡು?", "LOCATION_QUERY", {"medicine": "ಮರ್ದ್"}),
    ("ಏಪ ದೋಕ್ತೆರ್ ಬರ್ಪೆರ್?", "TIME_QUERY", {"medical_term": "ದೋಕ್ತೆರ್"}),
    ("ದೋಕ್ತೆರೆನ ಸಮಯ ಏಪ?", "TIME_QUERY", {"medical_term": "ದೋಕ್ತೆರೆನ"}),
    ("ಇನಿ ದೋಕ್ತೆರ್ ಬರ್ಪೆರಾ?", "TIME_QUERY", {"medical_term": "ದೋಕ್ತೆರ್", "date": "ಇನಿ"}),
    ("ನಾಲೆ ಭೇಟಿ ಆಪುಂಡಾ?", "TIME_QUERY", {"date": "ನಾಲೆ"}),
    ("ಗಂಟೆ ಏತ್ ಆಂಡ್?", "TIME_QUERY", {"time": "ಗಂಟೆ"}),
    ("ವರದಿ ಬಗ್ಗೆ ಮಾಹಿತಿ ಬೋಡು.", "INFORMATION_QUERY", {}),
    ("ತುಳು ಭಾಷೆ ಬಗ್ಗೆ ಪಣ್ಲೆ.", "INFORMATION_QUERY", {"language": "ತುಳು"}),
    ("ಮರ್ದ್‌ದ ಬಗ್ಗೆ ತೆರಿಯೊಡು.", "INFORMATION_QUERY", {"medicine": "ಮರ್ದ್‌ದ"}),
    ("ದೋಕ್ತೆರೆನ್ ತೂವೊಲಿ ವಾ?", "INFORMATION_QUERY", {"medical_term": "ದೋಕ್ತೆರೆನ್"}),
    ("ಎಂಕ್ ವರದಿ ತಿಕ್ಕುಂಡಾ?", "INFORMATION_QUERY", {})
]
for text, intent, ent in q_tu_kn:
    tu_samples.append({"text": text, "language": "tcy", "intent": intent, "entities": ent, "category": "questions_kn_script"})

# Questions & Location/Time (Latin Transliteration) (15)
q_tu_lat = [
    ("dokther vaade uller?", "LOCATION_QUERY", {"medical_term": "dokther"}),
    ("davakhane vaade undu?", "LOCATION_QUERY", {"medical_term": "davakhane"}),
    ("hospital vaade undu?", "LOCATION_QUERY", {"medical_term": "hospital"}),
    ("kudlad doctor vaade uller?", "LOCATION_QUERY", {"location": "kudlad", "medical_term": "doctor"}),
    ("mard vaade tikundu?", "LOCATION_QUERY", {"medicine": "mard"}),
    ("eapa doctor barper?", "TIME_QUERY", {"medical_term": "doctor"}),
    ("portu aeti?", "TIME_QUERY", {"time": "portu"}),
    ("ini doctor ullera?", "TIME_QUERY", {"medical_term": "doctor", "date": "ini"}),
    ("naale doctor sandarshana unda?", "TIME_QUERY", {"medical_term": "doctor", "date": "naale"}),
    ("gante eath aand?", "TIME_QUERY", {"time": "gante"}),
    ("report bage mahiti bodu", "INFORMATION_QUERY", {}),
    ("tulu bage panle", "INFORMATION_QUERY", {"language": "tulu"}),
    ("doctor bage gottunda?", "INFORMATION_QUERY", {"medical_term": "doctor"}),
    ("ovvu room ku pole?", "LOCATION_QUERY", {}),
    ("ini clinic open unda?", "TIME_QUERY", {"date": "ini"})
]
for text, intent, ent in q_tu_lat:
    tu_samples.append({"text": text, "language": "tcy", "intent": intent, "entities": ent, "category": "questions_latin_script"})

# Code-Switching with English (15)
codeswitch_tu = [
    ("Doctor naale appointment idiya?", "INFORMATION_QUERY", {"medical_term": "Doctor", "date": "naale"}),
    ("Doctor ini clinic du ullera?", "TIME_QUERY", {"medical_term": "Doctor", "date": "ini"}),
    ("Hospital vaade ullundu?", "LOCATION_QUERY", {"medical_term": "Hospital"}),
    ("Doctor report check malpera?", "REQUEST", {"medical_term": "Doctor"}),
    ("Appointment time eapa?", "TIME_QUERY", {"time": "time"}),
    ("Emergency ward vaade undu?", "LOCATION_QUERY", {"medical_term": "Emergency"}),
    ("Doctor consultation fee aeth?", "GENERAL_QUESTION", {"medical_term": "Doctor"}),
    ("Ambulance bega barpunda?", "EMERGENCY", {}),
    ("Blood test result ini tikunda?", "INFORMATION_QUERY", {"date": "ini"}),
    ("ICU room ovvu floor du undu?", "LOCATION_QUERY", {}),
    ("Medicine list dayamalth korle", "REQUEST", {"medicine": "Medicine"}),
    ("Doctor cabin vaade undu?", "LOCATION_QUERY", {"medical_term": "Doctor"}),
    ("Scanning report naale tikunda?", "INFORMATION_QUERY", {"date": "naale"}),
    ("Doctor operation theatre du ullera?", "LOCATION_QUERY", {"medical_term": "Doctor"}),
    ("Prescription check malpule please", "REQUEST", {})
]
for text, intent, ent in codeswitch_tu:
    tu_samples.append({"text": text, "language": "tcy", "intent": intent, "entities": ent, "category": "code_switching"})

# Informal Slang & Colloquial (15)
slang_tu = [
    ("bro enna madthiya?", "GENERAL_QUESTION", {}),
    ("mast laik undu", "FEEDBACK", {}),
    ("enla vishesha?", "GENERAL_QUESTION", {}),
    ("padchi tension gethonla", "STATEMENT", {}),
    ("boduva eereg?", "GENERAL_QUESTION", {}),
    ("laik uthara", "FEEDBACK", {}),
    ("machha help malpule", "HELP", {}),
    ("maga daane samachara?", "GENERAL_QUESTION", {}),
    ("enk mast kushi aand", "STATEMENT", {}),
    ("dayamalth help malpu bro", "HELP", {}),
    ("dokther mast edde uller", "STATEMENT", {"medical_term": "dokther"}),
    ("laik aath panle", "REQUEST", {}),
    ("padchi, yan toole", "STATEMENT", {}),
    ("mast bakkela aand", "STATEMENT", {}),
    ("enla samachara kudlad?", "GENERAL_QUESTION", {"location": "kudlad"})
]
for text, intent, ent in slang_tu:
    tu_samples.append({"text": text, "language": "tcy", "intent": intent, "entities": ent, "category": "slang_informal"})

# Requests & Help (10)
req_tu = [
    ("ದಯಮಲ್ತ್ ಸಹಾಯ ಮಲ್ಪುಲೆ.", "HELP", {}),
    ("dayamalth sahaya malpule", "HELP", {}),
    ("ಎಂಕ್ ಸಹಾಯ ಬೋಡು.", "HELP", {}),
    ("enk help bodu", "HELP", {}),
    ("ದಯಮಲ್ತ್ ದೋಕ್ತೆರೆನ್ ಲೆಪ್ಪಿಲೆ.", "REQUEST", {"medical_term": "ದೋಕ್ತೆರೆನ್"}),
    ("ದಯಮಲ್ತ್ ಈ ಮಾಹಿತಿನ್ ಓದುಲೆ.", "REQUEST", {}),
    ("ಕುಡೊರ ಪಣ್ಲೆ ದಯಮಲ್ತ್.", "REQUEST", {}),
    ("ಎಂಕ್ ದಾರಿ ತೊಜಿಪಾಲೆ.", "HELP", {}),
    ("ದಯಮಲ್ತ್ ನೀರ್ ಕೊರ್ಲೆ.", "REQUEST", {}),
    ("dayamalth explain malpule", "REQUEST", {})
]
for text, intent, ent in req_tu:
    tu_samples.append({"text": text, "language": "tcy", "intent": intent, "entities": ent, "category": "request_help"})

# Introductions & Dialogue (10)
intro_tu = [
    ("ಎನ್ನ ಪುದರ್ ರಮೇಶ್.", "INTRODUCTION", {"person": "ರಮೇಶ್"}),
    ("enna pudar Ramesh", "INTRODUCTION", {"person": "Ramesh"}),
    ("ಯಾನ್ ದಿನೇಶ್.", "INTRODUCTION", {"person": "ದಿನೇಶ್"}),
    ("yan Suresh", "INTRODUCTION", {"person": "Suresh"}),
    ("ಸೊಲ್ಮೆಲು ಈರೆಗ್.", "THANKS", {}),
    ("solmelu eereg", "THANKS", {}),
    ("ಪೋದು ಬರ್ಪೆ!", "FAREWELL", {}),
    ("podu barpe", "FAREWELL", {}),
    ("ಆಂಡ್, ಅಂದ್.", "YES", {}),
    ("ಇಜ್ಜಿ, ತಪ್ಪು.", "NO", {})
]
for text, intent, ent in intro_tu:
    tu_samples.append({"text": text, "language": "tcy", "intent": intent, "entities": ent, "category": "intro_dialogue"})

# Complaints & Emergency (10)
emerg_tu = [
    ("ಎಂಕ್ ತರೆಬೇನೆ ಉಂಡು.", "COMPLAINT", {"disease": "ತರೆಬೇನೆ"}),
    ("enk tarebene undu", "COMPLAINT", {"disease": "tarebene"}),
    ("ಬಂಜಿಬೇನೆ ಆಪುಂಡು.", "COMPLAINT", {"disease": "ಬಂಜಿಬೇನೆ"}),
    ("ಯಾನ್ ಮಸ್ತ್ tired ಉಲ್ಲೆ.", "COMPLAINT", {}),
    ("ಕಾರ್ಡ್ ಬೇನೆ ಉಂಡು.", "COMPLAINT", {"body_part": "ಕಾರ್ಡ್"}),
    ("ಆಪತ್ತ್ ಉಂಡು ಬೇಗ ಬಲೆ!", "EMERGENCY", {}),
    ("ತುರ್ತು ಸಹಾಯ ಬೋಡು!", "EMERGENCY", {}),
    ("emergency undu ambulance ಲೆಪ್ಪುಲೆ!", "EMERGENCY", {}),
    ("ನೆತ್ತೆರ್ ಬರ್ಪೊಂಡು ಬೇಗ ಬಲೆ!", "EMERGENCY", {"body_part": "ನೆತ್ತೆರ್"}),
    ("aapath sthiti, doctor bodu!", "EMERGENCY", {"medical_term": "doctor"})
]
for text, intent, ent in emerg_tu:
    tu_samples.append({"text": text, "language": "tcy", "intent": intent, "entities": ent, "category": "complaint_emergency"})

assert len(tu_samples) == 100, f"Expected 100 Tulu samples, got {len(tu_samples)}"
with open(EVAL_DIR / "tu_100.json", "w", encoding="utf-8") as f:
    json.dump(tu_samples, f, ensure_ascii=False, indent=2)
print("Generated tu_100.json with 100 Tulu examples.")
