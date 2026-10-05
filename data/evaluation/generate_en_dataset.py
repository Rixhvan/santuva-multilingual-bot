import json
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
en_samples = []

# Greetings (10)
greetings_en = [
    ("Hello!", "GREETING", {}),
    ("Hi there", "GREETING", {}),
    ("Hey", "GREETING", {}),
    ("Good morning", "GREETING", {}),
    ("Good afternoon", "GREETING", {}),
    ("Good evening", "GREETING", {}),
    ("Greetings to you", "GREETING", {}),
    ("Hey buddy", "GREETING", {}),
    ("Hello assistant", "GREETING", {}),
    ("Hi, how are you?", "GENERAL_QUESTION", {})
]
for text, intent, ent in greetings_en:
    en_samples.append({"text": text, "language": "en", "intent": intent, "entities": ent, "category": "greeting"})

# Questions & Location/Time/Info (25)
q_en = [
    ("Where is the doctor?", "LOCATION_QUERY", {"medical_term": "doctor"}),
    ("Where is the hospital?", "LOCATION_QUERY", {"medical_term": "hospital"}),
    ("Can you tell me where the clinic is located?", "LOCATION_QUERY", {"medical_term": "clinic"}),
    ("Which floor is the cardiology ward on?", "LOCATION_QUERY", {}),
    ("Where can I find the pharmacy?", "LOCATION_QUERY", {}),
    ("When does the doctor come?", "TIME_QUERY", {"medical_term": "doctor"}),
    ("What are the hospital visiting hours?", "TIME_QUERY", {"medical_term": "hospital"}),
    ("What time is my appointment?", "TIME_QUERY", {"medical_term": "appointment"}),
    ("When is Dr. Rao available?", "TIME_QUERY", {"person": "Dr. Rao"}),
    ("What time does the OPD open?", "TIME_QUERY", {}),
    ("Can I talk to someone about my report?", "INFORMATION_QUERY", {"medical_term": "report"}),
    ("Tell me about Sanskrit.", "INFORMATION_QUERY", {"language": "Sanskrit"}),
    ("What does this medicine do?", "INFORMATION_QUERY", {"medicine": "medicine"}),
    ("Can you give me information about health tips?", "INFORMATION_QUERY", {}),
    ("Tell me about Tulu language.", "INFORMATION_QUERY", {"language": "Tulu"}),
    ("Who is the head physician?", "GENERAL_QUESTION", {"medical_term": "physician"}),
    ("How does this consultation work?", "GENERAL_QUESTION", {"medical_term": "consultation"}),
    ("What is your name?", "INFORMATION_QUERY", {}),
    ("How are you today?", "GENERAL_QUESTION", {}),
    ("Is the laboratory open now?", "TIME_QUERY", {}),
    ("How long will the test take?", "TIME_QUERY", {"medical_term": "test"}),
    ("Where should I submit the blood sample?", "LOCATION_QUERY", {}),
    ("Can you explain my diagnosis?", "INFORMATION_QUERY", {"medical_term": "diagnosis"}),
    ("Who is on duty tonight?", "GENERAL_QUESTION", {}),
    ("Where is the emergency room located?", "LOCATION_QUERY", {"medical_term": "emergency"})
]
for text, intent, ent in q_en:
    en_samples.append({"text": text, "language": "en", "intent": intent, "entities": ent, "category": "questions"})

# Requests & Help (15)
req_en = [
    ("Can you help me?", "HELP", {}),
    ("I need help please.", "HELP", {}),
    ("I don't know where to go.", "HELP", {}),
    ("Please assist me with directions.", "HELP", {}),
    ("Could you please help?", "HELP", {}),
    ("Please call a doctor.", "REQUEST", {"medical_term": "doctor"}),
    ("Please check my appointment status.", "REQUEST", {"medical_term": "appointment"}),
    ("Please repeat what you said.", "REQUEST", {}),
    ("Could you clarify that point?", "REQUEST", {}),
    ("Please provide the contact number.", "REQUEST", {}),
    ("Give me some water please.", "REQUEST", {}),
    ("Help me find the room.", "HELP", {}),
    ("Please explain this in simple words.", "REQUEST", {}),
    ("Kindly guide me.", "HELP", {}),
    ("Can you show me the route?", "HELP", {})
]
for text, intent, ent in req_en:
    en_samples.append({"text": text, "language": "en", "intent": intent, "entities": ent, "category": "request_help"})

# Informal / Slang / SMS abbreviations (15)
slang_en = [
    ("bro what are you doing?", "GENERAL_QUESTION", {}),
    ("hey doc, need some advice", "INFORMATION_QUERY", {"medical_term": "doc"}),
    ("plz help me out", "HELP", {}),
    ("pls tell me the time", "TIME_QUERY", {}),
    ("thx for the help!", "THANKS", {}),
    ("idk what to do next", "HELP", {}),
    ("r u there?", "GENERAL_QUESTION", {}),
    ("heyyyy assistant", "GREETING", {}),
    ("sooooo tired today", "COMPLAINT", {}),
    ("pleaaase help me", "HELP", {}),
    ("wbu?", "GENERAL_QUESTION", {}),
    ("hiii there", "GREETING", {}),
    ("yup, got it", "CONFIRMATION", {}),
    ("nope, not that", "DENIAL", {}),
    ("doc appointment tomorrow plz", "INFORMATION_QUERY", {"medical_term": "doc", "date": "tomorrow"})
]
for text, intent, ent in slang_en:
    en_samples.append({"text": text, "language": "en", "intent": intent, "entities": ent, "category": "slang_informal"})

# Introductions & Dialogue (15)
intro_en = [
    ("My name is Ramesh.", "INTRODUCTION", {"person": "Ramesh"}),
    ("I am John Smith.", "INTRODUCTION", {"person": "John"}),
    ("Call me Priya.", "INTRODUCTION", {}),
    ("Myself David.", "INTRODUCTION", {}),
    ("Thank you very much!", "THANKS", {}),
    ("Thanks a lot!", "THANKS", {}),
    ("Many thanks for your support.", "THANKS", {}),
    ("Goodbye!", "FAREWELL", {}),
    ("Bye, see you later!", "FAREWELL", {}),
    ("Take care!", "FAREWELL", {}),
    ("Yes, exactly.", "CONFIRMATION", {}),
    ("No, that is incorrect.", "DENIAL", {}),
    ("Yes", "YES", {}),
    ("No", "NO", {}),
    ("Sure, that works.", "YES", {})
]
for text, intent, ent in intro_en:
    en_samples.append({"text": text, "language": "en", "intent": intent, "entities": ent, "category": "intro_dialogue"})

# Complaints & Health (10)
complaint_en = [
    ("I am feeling tired.", "COMPLAINT", {}),
    ("I have a severe headache.", "COMPLAINT", {"disease": "headache"}),
    ("My stomach hurts badly.", "COMPLAINT", {"body_part": "stomach"}),
    ("I have high fever.", "COMPLAINT", {"disease": "fever"}),
    ("My chest is paining.", "COMPLAINT", {"body_part": "chest"}),
    ("I feel very dizzy.", "COMPLAINT", {}),
    ("I have back pain.", "COMPLAINT", {"body_part": "back"}),
    ("My throat is sore.", "COMPLAINT", {"body_part": "throat"}),
    ("I am experiencing fatigue.", "COMPLAINT", {}),
    ("My leg is swollen.", "COMPLAINT", {"body_part": "leg"})
]
for text, intent, ent in complaint_en:
    en_samples.append({"text": text, "language": "en", "intent": intent, "entities": ent, "category": "complaints"})

# Emergency (10)
emerg_en = [
    ("Emergency! Please call an ambulance!", "EMERGENCY", {}),
    ("Urgent medical assistance required immediately!", "EMERGENCY", {}),
    ("The patient is unconscious!", "EMERGENCY", {"medical_term": "patient"}),
    ("Heart attack emergency!", "EMERGENCY", {}),
    ("Heavy bleeding, need immediate help!", "EMERGENCY", {}),
    ("Accident victim needs emergency room now!", "EMERGENCY", {"medical_term": "emergency"}),
    ("Child is choking, emergency!", "EMERGENCY", {}),
    ("Critical patient in distress!", "EMERGENCY", {"medical_term": "patient"}),
    ("Call 108 right now!", "EMERGENCY", {}),
    ("Emergency doctor needed!", "EMERGENCY", {"medical_term": "doctor"})
]
for text, intent, ent in emerg_en:
    en_samples.append({"text": text, "language": "en", "intent": intent, "entities": ent, "category": "emergency"})

assert len(en_samples) == 100, f"Expected 100 English samples, got {len(en_samples)}"
with open(EVAL_DIR / "en_100.json", "w", encoding="utf-8") as f:
    json.dump(en_samples, f, ensure_ascii=False, indent=2)
print("Generated en_100.json with 100 English examples.")
