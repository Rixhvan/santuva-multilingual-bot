from typing import Dict, Any, Optional
from backend.models.schemas import SemanticRepresentation, DialogueState

class MultilingualResponseGenerator:
    """
    Language-preserving response generation engine.
    Generates culturally appropriate, grammatical, and context-aware responses
    in Sanskrit, English, and Tulu without translation round-tripping.
    """

    RESPONSES = {
        "sa": {
            "GREETING": "नमस्ते! अहं भवतः साहाय्यं कर्तुं सज्जः अस्मि। कथं साहाय्यं करवाणि?",
            "FAREWELL": "पुनर्मिलामः! भवतः दिनं शुभं भवतु। स्वास्थ्यं रक्षतु।",
            "THANKS": "भवते स्वागतम्! साहाय्यं कृत्वा आनन्दः जातः।",
            "LOCATION_QUERY": "चिकित्सकः मुख्यभवने प्रथमतले परामर्शप्रकोष्ठे उपलभ्यते। भवान् कस्य विभागस्य अन्वेषणं करोति?",
            "TIME_QUERY": "परामर्शसमयः प्रातः नववादनात् (9:00 AM) सायङ्काले पञ्चवादनपर्यन्तं (5:00 PM) वर्तते।",
            "HELP": "अवश्यम्, अहं भवतः साहाय्यार्थम् अत्र अस्मि। कृपया स्वस्य प्रश्नं स्पष्टतया वदतु।",
            "COMPLAINT": "अहं भवतः अस्वास्थ्यस्य विषये श्रुत्वा खिन्नः अस्मि। कृपया विश्रामं स्वीकरोतु, योग्यं चिकित्सकं च पश्यतु।",
            "INFORMATION_QUERY": "अवश्यम्, अहं भवतः जिज्ञासितविषये सूचनां दातुं शक्नोमि। कस्य विषये अधिकं ज्ञातुम् इच्छति?",
            "YES": "उत्तमम्! अग्रे कथं साहाय्यं कुर्याम्?",
            "NO": "अवगतम्। यदि अन्यत् किमपि साहाय्यम् आवश्यकं तर्हि कृपया सूचयतु।",
            "EMERGENCY": "आपत्काले कृपया सद्यः आपातकालीनकक्षं (Emergency Room) सम्पर्कयतु अथवा १०८ सङ्ख्यां डायल करोतु!",
            "GENERAL_QUESTION": "अहं कुशलः अस्मि! भवान् कथम् अस्ति?",
            "FALLBACK": "क्षम्यताम्, अहं सम्यक् न अवगच्छम्। कृपया पुनः स्पष्टतया वदतु।"
        },
        "en": {
            "GREETING": "Hello! I am your multilingual assistant. How can I help you today?",
            "FAREWELL": "Goodbye! Take care and have a wonderful day.",
            "THANKS": "You're very welcome! I'm glad I could help.",
            "LOCATION_QUERY": "The doctor is available in the main consultation wing on the first floor. Could you tell me which specialist or department you are looking for?",
            "TIME_QUERY": "Consultation hours are generally from 9:00 AM to 5:00 PM. Would you like timings for a specific doctor?",
            "HELP": "I'm here to help! You can ask about locations, timings, health terminology, or languages (Sanskrit, English, Tulu).",
            "COMPLAINT": "I am sorry to hear that you are not feeling well. Please make sure to consult a licensed medical professional for proper care.",
            "INFORMATION_QUERY": "I would be happy to share information. Could you please specify which topic or report you'd like to discuss?",
            "YES": "Great! How would you like to proceed?",
            "NO": "Understood. Please let me know if there is anything else you need.",
            "EMERGENCY": "For immediate medical emergencies, please call emergency services (like 108 or 911) or visit the nearest emergency department right away!",
            "GENERAL_QUESTION": "I'm doing well, thank you! How are you doing today?",
            "FALLBACK": "I'm not completely sure I understood that. Could you please rephrase or provide a bit more detail?"
        },
        "tcy": {
            "GREETING": "ನಮಸ್ಕಾರ! ಎಂಚ ಉಲ್ಲೆರ್? ಯಾನ್ ಈರೆಗ್ ಎಂಚಿನ ಸಹಾಯ ಮಲ್ಪೊಡು?",
            "FAREWELL": "ಸೊಲ್ಮೆಲು! ಪೋದು ಬರ್ಪೆ, ಎಡ್ಡೆ ದಿನ ಆವಡ್.",
            "THANKS": "ಸೊಲ್ಮೆಲು! ಈರೆಗ್ ಸಹಾಯ ಮಲ್ತಿನೆಕ್ ಎಂಕ್ ಕುಶಿ ಆಂಡ್.",
            "LOCATION_QUERY": "ದೋಕ್ತೆರ್ ಮುಕ್ಯ ಕಟ್ಟೋಣದ ಸುರುತ ಮಹಡಿಡ್ ಉಲ್ಲೆರ್. ಈರೆಗ್ ಒವ್ವು ವಿಭಾಗ ಬೋಡು?",
            "TIME_QUERY": "ದೋಕ್ತೆರೆನ ಭೇಟಿ ಸಮಯ ಕಾಂಡೆ ೯:೦೦ ಗಂಟೆರ್ದ್ ಬಯ್ಯಗ್ ೫:೦೦ ಗಂಟೆ ಮುಟ್ಟ ಉಂಡು.",
            "HELP": "ಯಾನ್ ಈರೆಗ್ ಸಹಾಯ ಮಲ್ಪೆರೆ ಸಿದ್ಧ ಉಲ್ಲೆ! ಈರೆನ ಪ್ರಶ್ನೆ ದಾನೆ ಪಂಡ್ದ್ ಪಣ್ಲೆ.",
            "COMPLAINT": "ಈರೆಗ್ ಬೇನೆ ಆಪುಂಡು ಪಂಡ್ದ್ ಕೇಣ್ ದ್ ಬೇಜಾರಾಂಡ್. ದಯಮಲ್ತ್ ಎಡ್ಡೆ ವಿಶ್ರಾಂತಿ ದೆತೊನ್ಲೆ ಬೊಕ್ಕ ದೋಕ್ತೆರೆನ್ ತೂಲೆ.",
            "INFORMATION_QUERY": "ಅಂದ್, ಈರೆಗ್ ಬೋಡಾಯಿನ ಮಾಹಿತಿ ಯಾನ್ ಪನ್ಪೆ. ಈರೆಗ್ ಒವ್ವೆನ ಬಗ್ಗೆ ತೆರಿಯೊಡು?",
            "YES": "ಎಡ್ಡೆ! ದುಂಬುಗು ದಾನೆ ಮಲ್ಪೊಡು ಪಣ್ಲೆ.",
            "NO": "ಸರಿ, ಈರೆಗ್ ಬೇರೆ ದಾಲ ಮಾಹಿತಿ ಬೋಡಾಂಡ ಕೇಣ್ಲೆ.",
            "EMERGENCY": "ತುರ್ತು ಪರಿಸ್ಥಿತಿ ಇತ್ತ್ಂಡ ದಯಮಲ್ತ್ ತಕ್ಷಣ ತುರ್ತು ಚಿಕಿತ್ಸಾ ವಿಭಾಗಗ್ ಪೋಲೆ ಅತ್ತ್ಂಡ ೧೦೮ ಕರೆ ಮಲ್ಪುಲೆ!",
            "GENERAL_QUESTION": "ಯಾನ್ ಎಡ್ಡೆ ಉಲ್ಲೆ! ಈರ್ ಎಂಚ ಉಲ್ಲೆರ್?",
            "FALLBACK": "ಎಂಕ್ ಸರಿಯಾದ್ ಅರ್ಥ ಆಯಿಜಿ. ದಯಮಲ್ತ್ ಕುಡೊರ ಪಣ್ಲೆ."
        }
    }

    # Transliterated Latin Tulu responses if input was Latin script Tulu
    RESPONSES_TCY_LATIN = {
        "GREETING": "Namaskara! Encha uller? Yan eereg enchina sahaya malpodu?",
        "FAREWELL": "Solmelu! Podu barpe, edde dina aavad.",
        "THANKS": "Solmelu! Eereg sahaya maltinek enk kushi aand.",
        "LOCATION_QUERY": "Dokther mukya building da first floor du uller. Eereg ovvu vibhaga bodu?",
        "TIME_QUERY": "Dokther sandarshana portu kaande 9:00 gante ddu bayyag 5:00 gante mutta undu.",
        "HELP": "Yan eereg sahaya malpere sidha ulle! Eer daane prashne pandd panle.",
        "COMPLAINT": "Eereg bene aapundu pandd kendd sankata aand. Dayamalth rest gethonle and doctor n toole.",
        "INFORMATION_QUERY": "And, naale doctor sandarshana portu tikundu. Eereg ovve vishaya gottavodu?",
        "YES": "Edde! Dumbugu daane malpodu panle.",
        "NO": "Sari, eereg bere daala mahiti bodaanda kenle.",
        "EMERGENCY": "Aapath sthiti ittnda dayamalth emergency room gu pole athnda 108 call malpule!",
        "GENERAL_QUESTION": "Yan edde ulle! Eer encha uller?",
        "FALLBACK": "Enk sariyad artha aayiji. Dayamalth kudora panle."
    }

    def generate_response(
        self,
        semantic_rep: SemanticRepresentation,
        dialogue_state: DialogueState,
        target_lang_code: str,
        script: str = "Latin",
        clarification_msg: Optional[str] = None
    ) -> str:
        """Generates response preserving target language and dialogue state."""
        if clarification_msg:
            return clarification_msg

        intent = semantic_rep.intent
        lang_dict = self.RESPONSES.get(target_lang_code, self.RESPONSES["en"])

        # If user spoke Tulu in Latin script, reply in Latin script Tulu for consistency
        if target_lang_code == "tcy" and script == "Latin":
            lang_dict = self.RESPONSES_TCY_LATIN

        # If user introduced themselves or name entity is present
        if intent == "INTRODUCTION":
            name = semantic_rep.entities.get("person") or dialogue_state.accumulated_entities.get("person")
            if name:
                if target_lang_code == "sa":
                    return f"नमस्ते {name} महोदय! भवतः स्वागतम् अस्ति। अहं कथं साहाय्यं करवाणि?"
                elif target_lang_code == "tcy":
                    if script == "Latin":
                        return f"Namaskara {name} avar! Eerna swagatha. Yan eereg enchina sahaya malpodu?"
                    return f"ನಮಸ್ಕಾರ {name} ಅವರೇ! ಈರೆಗ್ ಸ್ವಾಗತ. ಯಾನ್ ಈರೆಗ್ ಎಂಚಿನ ಸಹಾಯ ಮಲ್ಪೊಡು?"
                else:
                    return f"Hello {name}! Nice to meet you. How can I assist you today?"

        # If user asks about their name and it is remembered
        if semantic_rep.intent in ("INFORMATION_QUERY", "GENERAL_QUESTION"):
            has_name_inquiry = "name" in semantic_rep.concepts or "pudar" in semantic_rep.concepts or any("name" in str(v).lower() for v in semantic_rep.entities.values())
            # Also check text if available in dialogue act
            name = dialogue_state.accumulated_entities.get("person")
            if has_name_inquiry and name:
                if target_lang_code == "sa":
                    return f"भवतः नाम {name} अस्ति।"
                elif target_lang_code == "tcy":
                    if script == "Latin":
                        return f"Eerna pudar {name} undu."
                    return f"ಈರೆನ ಪುದರ್ {name} ಉಂಡು."
                else:
                    return f"Your name is {name}."

        # Topic-sensitive response for Sanskrit query (Section 16 example)
        if dialogue_state.current_topic == "Sanskrit" and intent == "TIME_QUERY":
            if target_lang_code == "en":
                return "Sanskrit is an ancient classical language dating back over 3,500 years to the Vedic period (c. 1500 BCE)."
            elif target_lang_code == "sa":
                return "संस्कृतभाषायाः प्रयोगः वैदिककालात् प्रायः ३५०० वर्षेभ्यः पूर्वम् आरब्धः।"
            elif target_lang_code == "tcy":
                return "ಸಂಸ್ಕೃತ ಭಾಷೆ ಸುಮಾರು ೩೫೦೦ ವರ್ಷ ದುಂಬುದ ವೈದಿಕ ಕಾಲರ್ದ್ ಬಳಕೆಡ್ ಉಂಡು."

        # Fetch standard response
        return lang_dict.get(intent, lang_dict.get("FALLBACK", self.RESPONSES["en"]["FALLBACK"]))

response_generator = MultilingualResponseGenerator()
