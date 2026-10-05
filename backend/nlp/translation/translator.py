import re
from typing import Dict, Any, List, Optional, Tuple
from backend.nlp.languages.sanskrit.morphology import sa_morphology
from backend.nlp.languages.tulu.morphology import tulu_morphology

class MultilingualEnglishTranslator:
    """
    Translates Sanskrit and Tulu utterances into natural, grammatical English,
    providing both sentence-level translation and word-by-word linguistic glossing.
    Combines rule-based morphological synthesis, lexicon lookup, and syntax templates.
    """

    # Sanskrit Word Glosses
    SA_WORD_GLOSSES = {
        "मम": ("my", "pronoun genitive 1st sing"),
        "मे": ("my / to me", "pronoun enclitic"),
        "नाम": ("name", "noun neuter nominative"),
        "रामः": ("Rama", "proper noun masculine nominative"),
        "राम": ("Rama", "proper noun vocative"),
        "रामस्य": ("of Rama", "proper noun genitive"),
        "रमेशः": ("Ramesh", "proper noun masculine nominative"),
        "कृष्णः": ("Krishna", "proper noun masculine nominative"),
        "महोदय": ("respected sir / Mr.", "noun vocative honorific"),
        "महोदयः": ("respected sir / gentleman", "noun masculine nominative"),
        "स्वागतम्": ("welcome", "noun neuter nominative"),
        "चिकित्सकः": ("doctor / physician", "noun masculine nominative"),
        "चिकित्सकम्": ("the doctor", "noun masculine accusative"),
        "चिकित्सकस्य": ("of the doctor", "noun masculine genitive"),
        "चिकित्सकाय": ("to/for the doctor", "noun masculine dative"),
        "चिकित्सालयः": ("hospital", "noun masculine nominative"),
        "चिकित्सालयम्": ("to the hospital", "noun masculine accusative"),
        "चिकित्सालये": ("in the hospital", "noun masculine locative"),
        "चिकित्सालयस्य": ("of the hospital", "noun masculine genitive"),
        "कुत्र": ("where", "interrogative adverb"),
        "कदा": ("when", "interrogative adverb"),
        "कथम्": ("how", "interrogative adverb"),
        "कथं": ("how", "interrogative adverb"),
        "किम्": ("what", "interrogative pronoun"),
        "कः": ("who", "interrogative pronoun masculine"),
        "का": ("who", "interrogative pronoun feminine"),
        "अस्ति": ("is", "verb present 3rd sing"),
        "सन्ति": ("are", "verb present 3rd plur"),
        "असि": ("you are", "verb present 2nd sing"),
        "अस्मि": ("I am", "verb present 1st sing"),
        "आगमिष्यति": ("will arrive / come", "verb future 3rd sing"),
        "गच्छामि": ("I go", "verb present 1st sing"),
        "इच्छामि": ("I want / wish", "verb present 1st sing"),
        "इच्छति": ("wants / wishes", "verb present 3rd sing"),
        "द्रष्टुम्": ("to see / consult", "infinitive"),
        "ज्ञातुम्": ("to know", "infinitive"),
        "वदतु": ("please speak / tell", "verb imperative 3rd sing"),
        "कृपया": ("please", "courtesy particle"),
        "धन्यवादः": ("thank you", "courtesy noun"),
        "पुनर्मिलामः": ("we will meet again", "verb present 1st plur"),
        "शुभदिनम्": ("good day", "noun phrase"),
        "सुप्रभातम्": ("good morning", "noun phrase"),
        "नमस्ते": ("greetings", "salutation"),
        "सूर्योदयः": ("sunrise", "compound noun nominative"),
        "समयः": ("time / schedule", "noun masculine nominative"),
        "औषधम्": ("medicine", "noun neuter nominative"),
        "औषधस्य": ("of the medicine", "noun neuter genitive"),
        "स्वास्थ्यम्": ("health", "noun neuter nominative"),
        "श्रान्तः": ("tired / fatigued", "adjective masculine"),
        "वेदना": ("pain / ache", "noun feminine"),
        "शिरोवेदना": ("headache", "compound noun feminine"),
        "उदरवेदना": ("stomach ache", "compound noun feminine"),
        "ज्वरः": ("fever", "noun masculine"),
        "आपत्कालः": ("emergency", "noun masculine"),
        "शीघ्रम्": ("quickly", "adverb"),
        "शीघ्रं": ("quickly", "adverb"),
        "साहाय्यम्": ("help / assistance", "noun neuter nominative"),
        "साहाय्यं": ("help / assistance", "noun neuter accusative"),
        "साहाय्यार्थम्": ("for assistance", "compound adverbial"),
        "करवाणि": ("may I do", "verb imperative 1st sing"),
        "करोतु": ("please do", "verb imperative 3rd sing"),
        "कुर्याम्": ("may I do", "verb optative 1st sing"),
        "कर्तुम्": ("to do / render", "infinitive"),
        "सज्जः": ("ready / prepared", "adjective masculine"),
        "भवतः": ("your (honorific)", "pronoun genitive"),
        "भवते": ("to you", "pronoun dative"),
        "भवान्": ("you (masc honorific)", "pronoun nominative"),
        "अहम्": ("I", "pronoun nominative 1st sing"),
        "अहं": ("I", "pronoun nominative 1st sing"),
        "त्वम्": ("you", "pronoun nominative 2nd sing"),
        "मार्गः": ("route / way", "noun masculine"),
        "मुख्यभवने": ("in the main building", "compound locative"),
        "प्रथमतले": ("on the first floor", "compound locative"),
        "परामर्शप्रकोष्ठे": ("in the consultation room", "compound locative"),
        "उपलभ्यते": ("is available", "verb present passive 3rd sing"),
        "अन्वेषणं": ("searching for", "noun accusative"),
        "करोति": ("is doing", "verb present 3rd sing"),
        "विभागस्य": ("of the department", "noun genitive"),
        "परामर्शसमयः": ("consultation hours", "compound noun"),
        "प्रातः": ("in the morning", "adverb"),
        "सायङ्काले": ("in the evening", "noun locative"),
        "अत्र": ("here", "adverb"),
        "स्वस्य": ("your own", "pronoun genitive"),
        "प्रश्नं": ("question", "noun accusative"),
        "स्पष्टतया": ("clearly", "adverb"),
        "अस्वास्थ्यस्य": ("of illness", "noun genitive"),
        "श्रुत्वा": ("having heard", "gerund"),
        "खिन्नः": ("concerned / saddened", "adjective"),
        "विश्रामं": ("rest", "noun accusative"),
        "स्वीकरोतु": ("please take", "verb imperative 3rd sing"),
        "योग्यं": ("qualified / appropriate", "adjective"),
        "पश्यतु": ("please see / consult", "verb imperative 3rd sing"),
        "जिज्ञासितविषये": ("regarding the query", "compound locative"),
        "सूचनां": ("information", "noun accusative"),
        "दातुं": ("to provide", "infinitive"),
        "शक्नोमि": ("I can", "verb present 1st sing"),
        "अधिकं": ("more", "adverb"),
        "उत्तमम्": ("excellent / great", "adjective"),
        "अग्रे": ("further / next", "adverb"),
        "अवगतम्": ("understood", "participle"),
        "अन्यत्": ("other / any other", "adjective"),
        "आवश्यकं": ("required", "adjective"),
        "तर्हि": ("then", "adverb"),
        "सूचयतु": ("please inform", "verb imperative"),
        "आपत्काले": ("during an emergency", "compound locative"),
        "सद्यः": ("immediately", "adverb"),
        "सम्पर्कयतु": ("please contact", "verb imperative"),
        "अथवा": ("or", "conjunction"),
        "कुशलः": ("well / fine", "adjective"),
        "क्षम्यताम्": ("excuse me / pardon", "passive imperative"),
        "सम्यक्": ("properly / well", "adverb"),
        "अवगच्छम्": ("understood", "verb past 1st sing"),
        "पुनः": ("again", "adverb"),
        "प्रयोगः": ("use / practice", "noun masculine"),
        "वैदिककालात्": ("from the Vedic era", "noun ablative"),
        "प्रायः": ("approximately", "adverb"),
        "वर्षेभ्यः": ("years", "noun ablative plural"),
        "पूर्वम्": ("ago / before", "adverb"),
        "आरब्धः": ("began", "participle")
    }

    # Tulu Word Glosses
    TU_WORD_GLOSSES = {
        "ನಮಸ್ಕಾರ": ("greetings", "salutation"),
        "namaskara": ("greetings", "salutation"),
        "ಸೊಲ್ಮೆಲು": ("thank you", "courtesy noun"),
        "solmelu": ("thank you", "courtesy noun"),
        "ದೋಕ್ತೆರ್": ("doctor", "noun honorific"),
        "dokther": ("doctor", "noun honorific"),
        "doctor": ("doctor", "noun"),
        "ದವಾಖಾನೆ": ("hospital", "noun"),
        "davakhane": ("hospital", "noun"),
        "hospital": ("hospital", "noun"),
        "ವಾಡೆ": ("where", "interrogative adverb"),
        "vaade": ("where", "interrogative adverb"),
        "ode": ("where", "interrogative adverb"),
        "ಉಲ್ಲೆರ್": ("is / are", "verb present honorific"),
        "uller": ("is / are", "verb present honorific"),
        "ಉಂಡು": ("is", "verb present neuter"),
        "undu": ("is", "verb present neuter"),
        "ullundu": ("is located", "verb present neuter"),
        "ಉಲ್ಲೆರಾ": ("are you available?", "verb present interrogative"),
        "ullera": ("are you available?", "verb present interrogative"),
        "ಏಪ": ("when", "interrogative adverb"),
        "aepa": ("when", "interrogative adverb"),
        "eapa": ("when", "interrogative adverb"),
        "ಬರ್ಪೆರ್": ("will come", "verb future honorific"),
        "barper": ("will come", "verb future honorific"),
        "ಎಂಚ": ("how", "interrogative adverb"),
        "encha": ("how", "interrogative adverb"),
        "ದಾನೆ": ("what", "interrogative pronoun"),
        "daane": ("what", "interrogative pronoun"),
        "ದಾಲ": ("anything", "indefinite pronoun"),
        "daala": ("anything", "indefinite pronoun"),
        "ಎನ್ನ": ("my", "pronoun genitive 1st"),
        "enna": ("my", "pronoun genitive 1st"),
        "ಪುದರ್": ("name", "noun"),
        "pudar": ("name", "noun"),
        "ಎಂಕ್": ("to me / for me", "pronoun dative 1st"),
        "enk": ("to me / for me", "pronoun dative 1st"),
        "ಈರೆಗ್": ("to you", "pronoun dative 2nd honorific"),
        "eereg": ("to you", "pronoun dative 2nd honorific"),
        "ಈರೆನ": ("your", "pronoun genitive 2nd honorific"),
        "eerna": ("your", "pronoun genitive 2nd honorific"),
        "ಈರ್": ("you", "pronoun nominative 2nd honorific"),
        "eer": ("you", "pronoun nominative 2nd honorific"),
        "ಯಾನ್": ("I", "pronoun nominative 1st"),
        "yan": ("I", "pronoun nominative 1st"),
        "ಸಹಾಯ": ("help / assistance", "noun"),
        "sahaya": ("help", "noun"),
        "help": ("help", "noun"),
        "ಬೋಡು": ("want / need", "modal auxiliary"),
        "bodu": ("want / need", "modal auxiliary"),
        "ಬಲ್ಲಿ": ("do not want / cannot", "negative modal"),
        "balli": ("do not want / cannot", "negative modal"),
        "ಇಜ್ಜಿ": ("is not / no", "negative existential"),
        "ijji": ("is not / no", "negative existential"),
        "ನಾಲೆ": ("tomorrow", "temporal adverb"),
        "naale": ("tomorrow", "temporal adverb"),
        "ಇನಿ": ("today", "temporal adverb"),
        "ini": ("today", "temporal adverb"),
        "ಕೊಡೆ": ("yesterday", "temporal adverb"),
        "kode": ("yesterday", "temporal adverb"),
        "appointment": ("appointment", "noun"),
        "idiya": ("is it available?", "interrogative existential"),
        "ಕುಡ್ಲ": ("Mangalore", "proper noun location"),
        "kudla": ("Mangalore", "proper noun location"),
        "ಕುಡ್ಲಡ್": ("in Mangalore", "noun locative"),
        "kudlad": ("in Mangalore", "noun locative"),
        "ಮರ್ದ್": ("medicine", "noun"),
        "mard": ("medicine", "noun"),
        "ತರೆಬೇನೆ": ("headache", "noun disease"),
        "tarebene": ("headache", "noun disease"),
        "ಬಂಜಿಬೇನೆ": ("stomach ache", "noun disease"),
        "banjibene": ("stomach ache", "noun disease"),
        "ಸೀಕ್": ("illness", "noun disease"),
        "seek": ("illness", "noun disease"),
        "ದಯಮಲ್ತ್": ("please", "courtesy particle"),
        "dayamalth": ("please", "courtesy particle"),
        "ಮಲ್ಪುಲೆ": ("please do", "verb imperative"),
        "malpule": ("please do", "verb imperative"),
        "ಮಲ್ಪೊಡು": ("may I do / should do", "modal verb"),
        "malpodu": ("may I do / should do", "modal verb"),
        "ಪಣ್ಲೆ": ("please tell", "verb imperative"),
        "panle": ("please tell", "verb imperative"),
        "ತೂಲೆ": ("please see / consult", "verb imperative"),
        "toole": ("please see / consult", "verb imperative"),
        "ಪೋದು": ("having gone", "participle"),
        "podu": ("having gone", "participle"),
        "ಬರ್ಪೆ": ("I will come / farewell", "verb future 1st"),
        "barpe": ("I will come / farewell", "verb future 1st"),
        "bro": ("brother / friend", "informal vocative"),
        "madthiya": ("are you doing?", "verb informal"),
        "mast": ("very / great", "intensifier adverb"),
        "laik": ("good / fine", "adjective"),
        "enla": ("what / greetings", "informal salutation"),
        "padchi": ("no need", "colloquial particle"),
        "aapath": ("emergency", "noun"),
        "ಆಪತ್ತ್": ("emergency", "noun"),
        "ತುರ್ತು": ("emergency", "adjective"),
        "ವರದಿ": ("report", "noun"),
        "report": ("report", "noun"),
        "ಬಗ್ಗೆ": ("about", "postposition"),
        "bage": ("about", "postposition"),
        "ಮಾಹಿತಿ": ("information", "noun"),
        "mahiti": ("information", "noun"),
        "ತಿಕ್ಕುಂಡು": ("is available", "verb present neuter"),
        "tikundu": ("is available", "verb present neuter"),
        "ಅವರೇ": ("respected Mr./Ms.", "honorific suffix"),
        "avar": ("respected Mr./Ms.", "honorific suffix"),
        "ಸ್ವಾಗತ": ("welcome", "noun"),
        "swagatha": ("welcome", "noun"),
        "ಎಂಚಿನ": ("what kind of / what", "interrogative"),
        "enchina": ("what kind of / what", "interrogative"),
        "ಎಡ್ಡೆ": ("well / good", "adjective/adverb"),
        "edde": ("well / good", "adjective/adverb"),
        "ದಿನ": ("day", "noun"),
        "dina": ("day", "noun"),
        "ಆವಡ್": ("have a", "optative verb"),
        "aavad": ("have a", "optative verb"),
        "ಮಲ್ತಿನೆಕ್": ("for helping", "verbal noun dative"),
        "maltinek": ("for helping", "verbal noun dative"),
        "ಕುಶಿ": ("pleasure / happiness", "noun"),
        "kushi": ("pleasure / happiness", "noun"),
        "ಆಂಡ್": ("it was", "verb past neuter"),
        "aand": ("it was", "verb past neuter"),
        "ಮುಕ್ಯ": ("main", "adjective"),
        "mukya": ("main", "adjective"),
        "ಕಟ್ಟೋಣದ": ("of the building", "noun genitive"),
        "ಸುರುತ": ("first", "ordinal adjective"),
        "ಮಹಡಿಡ್": ("on the floor", "noun locative"),
        "ಒವ್ವು": ("which", "interrogative"),
        "ovvu": ("which", "interrogative"),
        "ವಿಭಾಗ": ("department", "noun"),
        "vibhaga": ("department", "noun"),
        "ಭೇಟಿ": ("consultation", "noun"),
        "sandarshana": ("consultation", "noun"),
        "portu": ("timing / hours", "noun"),
        "ಕಾಂಡೆ": ("in the morning", "adverb"),
        "kaande": ("in the morning", "adverb"),
        "ಬಯ್ಯಗ್": ("in the evening", "adverb"),
        "bayyag": ("in the evening", "adverb"),
        "ಮುಟ್ಟ": ("until", "postposition"),
        "mutta": ("until", "postposition"),
        "ಸಿದ್ಧ": ("ready", "adjective"),
        "sidha": ("ready", "adjective"),
        "ಪ್ರಶ್ನೆ": ("question", "noun"),
        "prashne": ("question", "noun"),
        "ಪಂಡ್ದ್": ("saying / that", "particle"),
        "pandd": ("saying / that", "particle"),
        "ಕೇಣ್ ದ್": ("having heard", "gerund"),
        "kendd": ("having heard", "gerund"),
        "ಬೇಜಾರಾಂಡ್": ("saddened", "predicate"),
        "sankata aand": ("saddened", "predicate"),
        "ವಿಶ್ರಾಂತಿ": ("rest", "noun"),
        "ದೆತೊನ್ಲೆ": ("please take", "verb imperative"),
        "gethonle": ("please take", "verb imperative"),
        "ತೆರಿಯೊಡು": ("want to know", "verb modal"),
        "gottavodu": ("want to know", "verb modal"),
        "ದುಂಬುಗು": ("next", "adverb"),
        "dumbugu": ("next", "adverb"),
        "ಬೇರೆ": ("other", "adjective"),
        "bere": ("other", "adjective"),
        "ಬೋಡಾಂಡ": ("if needed", "conditional"),
        "bodaanda": ("if needed", "conditional"),
        "ಕೇಣ್ಲೆ": ("please ask", "verb imperative"),
        "kenle": ("please ask", "verb imperative")
    }

    # High-precision Idiomatic Sentence Translation Dictionary
    IDIOMATIC_TRANSLATIONS = {
        # Sanskrit Sentences
        "मम नाम रामः।": "My name is Rama.",
        "मम नाम रामः": "My name is Rama.",
        "मम नाम रमेशः।": "My name is Ramesh.",
        "अहं कृष्णः अस्मि।": "I am Krishna.",
        "चिकित्सकः कुत्र अस्ति?": "Where is the doctor?",
        "चिकित्सालयः कुत्र अस्ति?": "Where is the hospital?",
        "मार्गः कुत्र अस्ति?": "Where is the route / way?",
        "कदा चिकित्सकः आगमिष्यति?": "When will the doctor arrive?",
        "चिकित्सालयस्य समयः कः?": "What are the hospital hours?",
        "चिकित्सकस्य विषये ज्ञातुम् इच्छामि।": "I want to know about the doctor.",
        "संस्कृतभाषायाः विषये वदतु।": "Please tell me about the Sanskrit language.",
        "औषधस्य विषये सूचनां ददातु।": "Please provide information about the medicine.",
        "कृपया साहाय्यं करोतु।": "Please help me.",
        "अहं साहाय्यम् इच्छामि।": "I need assistance / help.",
        "मां साहाय्यं कुरु।": "Please assist me.",
        "मम शिरोवेदना अस्ति।": "I have a headache.",
        "उदरवेदना बाधते।": "I am suffering from a stomach ache.",
        "अहं श्रान्तः अस्मि।": "I am feeling tired.",
        "मम ज्वरः अस्ति।": "I have a fever.",
        "सूर्योदयः कदा भवति?": "When does the sunrise occur?",
        "आपत्कालः अस्ति!": "This is an emergency!",
        "शीघ्रं साहाय्यं कुरु!": "Provide help quickly!",
        "पुनर्मिलामः।": "We will meet again.",
        "शुभं भवतु।": "Best wishes to you.",
        "धन्यवादः।": "Thank you.",
        "नमस्ते": "Greetings / Hello.",
        "सुप्रभातम्": "Good morning.",
        "शुभदिनम्": "Good day.",
        "आम्, सत्यम्।": "Yes, that is true.",
        "नहि नहि।": "No, not at all.",
        "कथम् अस्ति भवान्?": "How are you?",
        "संस्कृतेन उत्तरं ददातु।": "Please reply in Sanskrit.",

        # Sanskrit Transliterated
        "mama nama Ramah.": "My name is Rama.",
        "chikitsakah kutra asti?": "Where is the doctor?",
        "katham asti bhavan?": "How are you?",
        "dhanyavadah": "Thank you.",
        "punarmilamah": "We will meet again.",
        "kripaya sahayyam karotu": "Please help me.",
        "aham shrantah asmi": "I am feeling tired.",

        # Tulu Sentences (Kannada Script)
        "ನಮಸ್ಕಾರ!": "Greetings! / Hello!",
        "ಸೊಲ್ಮೆಲು!": "Thank you!",
        "ಎಂಚ ಉಲ್ಲೆರ್?": "How are you?",
        "ದಾನೆ ವಿಶೇಷ?": "What's new / special?",
        "ದೋಕ್ತೆರ್ ವಾಡೆ ಉಲ್ಲೆರ್?": "Where is the doctor?",
        "ದವಾಖಾನೆ ವಾಡೆ ಉಂಡು?": "Where is the hospital?",
        "ಕುಡ್ಲಡ್ ದವಾಖಾನೆ ವಾಡೆ ಉಂಡು?": "Where is the hospital in Mangalore?",
        "ಏಪ ದೋಕ್ತೆರ್ ಬರ್ಪೆರ್?": "When will the doctor come?",
        "ದೋಕ್ತೆರೆನ ಸಮಯ ಏಪ?": "When is the doctor's timing?",
        "ಇನಿ ದೋಕ್ತೆರ್ ಬರ್ಪೆರಾ?": "Will the doctor come today?",
        "ನಾಲೆ ಭೇಟಿ ಆಪುಂಡಾ?": "Will the appointment take place tomorrow?",
        "ಎನ್ನ ಪುದರ್ ರಮೇಶ್.": "My name is Ramesh.",
        "ದಯಮಲ್ತ್ ಸಹಾಯ ಮಲ್ಪುಲೆ.": "Please help me.",
        "ಎಂಕ್ ಸಹಾಯ ಬೋಡು.": "I need help.",
        "ಎಂಕ್ ತರೆಬೇನೆ ಉಂಡು.": "I have a headache.",
        "ಬಂಜಿಬೇನೆ ಆಪುಂಡು.": "I have a stomach ache.",
        "ವರದಿ ಬಗ್ಗೆ ಮಾಹಿತಿ ಬೋಡು.": "I need information regarding the report.",
        "ತುಳು ಭಾಷೆ ಬಗ್ಗೆ ಪಣ್ಲೆ.": "Please tell me about the Tulu language.",
        "ಆಪತ್ತ್ ಉಂಡು ಬೇಗ ಬಲೆ!": "There is an emergency, please come quickly!",
        "ತುರ್ತು ಸಹಾಯ ಬೋಡು!": "Urgent assistance is needed!",
        "ಪೋದು ಬರ್ಪೆ!": "I will take your leave / Goodbye!",
        "ಆಂಡ್, ಅಂದ್.": "Yes, exactly.",
        "ಇಜ್ಜಿ, ತಪ್ಪು.": "No, that is incorrect.",

        # Tulu Sentences (Latin Script & Code-Switching & Slang)
        "namaskara": "Greetings / Hello.",
        "solmelu": "Thank you.",
        "encha uller?": "How are you?",
        "daane vishesha?": "What's new / special?",
        "dokther vaade uller?": "Where is the doctor?",
        "davakhane vaade undu?": "Where is the hospital?",
        "hospital vaade undu?": "Where is the hospital?",
        "kudlad doctor vaade uller?": "Where is the doctor in Mangalore?",
        "Doctor naale appointment idiya?": "Doctor, is an appointment available tomorrow?",
        "Doctor ini clinic du ullera?": "Doctor, are you in the clinic today?",
        "Hospital vaade ullundu?": "Where is the hospital located?",
        "bro enna madthiya?": "Brother/Friend, what are you doing?",
        "mast laik undu": "It is very good / great.",
        "enla vishesha?": "What's the news?",
        "padchi tension gethonla": "No need to worry, don't take tension.",
        "enk tarebene undu": "I have a headache.",
        "enna pudar Ramesh": "My name is Ramesh.",
        "enk help bodu": "I need help.",
        "dayamalth sahaya malpule": "Please help me.",

        # Standard Bot Response Sentences (Sanskrit)
        "नमस्ते! अहं भवतः साहाय्यं कर्तुं सज्जः अस्मि। कथं साहाय्यं करवाणि?": "Greetings! I am ready to assist you. How may I help you?",
        "पुनर्मिलामः! भवतः दिनं शुभं भवतु। स्वास्थ्यं रक्षतु।": "Farewell! Have a wonderful day and take care of your health.",
        "भवते स्वागतम्! साहाय्यं कृत्वा आनन्दः जातः।": "You are welcome! It was a pleasure to assist you.",
        "चिकित्सकः मुख्यभवने प्रथमतले परामर्शप्रकोष्ठे उपलभ्यते। भवान् कस्य विभागस्य अन्वेषणं करोति?": "The doctor is available in the consultation room on the first floor of the main building. Which department are you looking for?",
        "परामर्शसमयः प्रातः नववादनात् (9:00 AM) सायङ्काले पञ्चवादनपर्यन्तं (5:00 PM) वर्तते।": "Consultation hours are from 9:00 AM morning to 5:00 PM evening.",
        "अवश्यम्, अहं भवतः साहाय्यार्थम् अत्र अस्मि। कृपया स्वस्य प्रश्नं स्पष्टतया वदतु।": "Certainly, I am here to help you. Please state your question clearly.",
        "अहं भवतः अस्वास्थ्यस्य विषये श्रुत्वा खिन्नः अस्मि। कृपया विश्रामं स्वीकरोतु, योग्यं चिकित्सकं च पश्यतु।": "I am concerned to hear that you are unwell. Please rest well and consult a qualified physician.",
        "अवश्यम्, अहं भवतः जिज्ञासितविषये सूचनां दातुं शक्नोमि। कस्य विषये अधिकं ज्ञातुम् इच्छति?": "Certainly, I can provide information. Which topic would you like to know more about?",
        "उत्तमम्! अग्रे कथं साहाय्यं कुर्याम्?": "Great! How may I assist you further?",
        "अवगतम्। यदि अन्यत् किमपि साहाय्यम् आवश्यकं तर्हि कृपया सूचयतु।": "Understood. Please let me know if you need any other assistance.",
        "आपत्काले कृपया सद्यः आपातकालीनकक्षं (Emergency Room) सम्पर्कयतु अथवा १०८ सङ्ख्यां डायल करोतु!": "In an emergency, please contact the Emergency Room immediately or dial 108!",
        "अहं कुशलः अस्मि! भवान् कथम् अस्ति?": "I am doing well! How are you?",
        "क्षम्यताम्, अहं सम्यक् न अवगच्छम्। कृपया पुनः स्पष्टतया वदतु।": "Excuse me, I did not understand properly. Could you please rephrase clearly?",
        "संस्कृतभाषायाः प्रयोगः वैदिककालात् प्रायः ३५०० वर्षेभ्यः पूर्वम् आरब्धः।": "The Sanskrit language has been in use since the Vedic period, dating back over 3,500 years.",

        # Standard Bot Response Sentences (Tulu - Kannada Script)
        "ನಮಸ್ಕಾರ! ಎಂಚ ಉಲ್ಲೆರ್? ಯಾನ್ ಈರೆಗ್ ಎಂಚಿನ ಸಹಾಯ ಮಲ್ಪೊಡು?": "Greetings! How are you? How may I help you?",
        "ಸೊಲ್ಮೆಲು! ಪೋದು ಬರ್ಪೆ, ಎಡ್ಡೆ ದಿನ ಆವಡ್.": "Thank you! I will take your leave, have a great day.",
        "ಸೊಲ್ಮೆಲು! ಈರೆಗ್ ಸಹಾಯ ಮಲ್ತಿನೆಕ್ ಎಂಕ್ ಕುಶಿ ಆಂಡ್.": "Thank you! It was my pleasure to help you.",
        "ದೋಕ್ತೆರ್ ಮುಕ್ಯ ಕಟ್ಟೋಣದ ಸುರುತ ಮಹಡಿಡ್ ಉಲ್ಲೆರ್. ಈರೆಗ್ ಒವ್ವು ವಿಭಾಗ ಬೋಡು?": "The doctor is on the first floor of the main building. Which department do you need?",
        "ದೋಕ್ತೆರೆನ ಭೇಟಿ ಸಮಯ ಕಾಂಡೆ ೯:೦೦ ಗಂಟೆರ್ದ್ ಬಯ್ಯಗ್ ೫:೦೦ ಗಂಟೆ ಮುಟ್ಟ ಉಂಡು.": "Doctor consultation timings are from 9:00 AM morning to 5:00 PM evening.",
        "ಯಾನ್ ಈರೆಗ್ ಸಹಾಯ ಮಲ್ಪೆರೆ ಸಿದ್ಧ ಉಲ್ಲೆ! ಈರೆನ ಪ್ರಶ್ನೆ ದಾನೆ ಪಂಡ್ದ್ ಪಣ್ಲೆ.": "I am ready to assist you! Please tell me your question.",
        "ಈರೆಗ್ ಬೇನೆ ಆಪುಂಡು ಪಂಡ್ದ್ ಕೇಣ್ ದ್ ಬೇಜಾರಾಂಡ್. ದಯಮಲ್ತ್ ಎಡ್ಡೆ ವಿಶ್ರಾಂತಿ ದೆತೊನ್ಲೆ ಬೊಕ್ಕ ದೋಕ್ತೆರೆನ್ ತೂಲೆ.": "Sad to hear you are unwell. Please take good rest and consult a doctor.",
        "ಅಂದ್, ಈರೆಗ್ ಬೋಡಾಯಿನ ಮಾಹಿತಿ ಯಾನ್ ಪನ್ಪೆ. ಈರೆಗ್ ಒವ್ವೆನ ಬಗ್ಗೆ ತೆರಿಯೊಡು?": "Yes, I will provide the information you need. What would you like to know about?",
        "ಎಡ್ಡೆ! ದುಂಬುಗು ದಾನೆ ಮಲ್ಪೊಡು ಪಣ್ಲೆ.": "Good! Please tell me what to do next.",
        "ಸರಿ, ಈರೆಗ್ ಬೇರೆ ದಾಲ ಮಾಹಿತಿ ಬೋಡಾಂಡ ಕೇಣ್ಲೆ.": "All right, let me know if you need any other information.",
        "ತುರ್ತು ಪರಿಸ್ಥಿತಿ ಇತ್ತ್ಂಡ ದಯಮಲ್ತ್ ತಕ್ಷಣ ತುರ್ತು ಚಿಕಿತ್ಸಾ ವಿಭಾಗಗ್ ಪೋಲೆ ಅತ್ತ್ಂಡ ೧೦೮ ಕರೆ ಮಲ್ಪುಲೆ!": "If it is an emergency, please go to the emergency department immediately or call 108!",
        "ಯಾನ್ ಎಡ್ಡೆ ಉಲ್ಲೆ! ಈರ್ ಎಂಚ ಉಲ್ಲೆರ್?": "I am doing well! How are you?",
        "ಎಂಕ್ ಸರಿಯಾದ್ ಅರ್ಥ ಆಯಿಜಿ. ದಯಮಲ್ತ್ ಕುಡೊರ ಪಣ್ಲೆ.": "I didn't understand clearly. Could you please say it again?",
        "ಸಂಸ್ಕೃತ ಭಾಷೆ ಸುಮಾರು ೩೫೦೦ ವರ್ಷ ದುಂಬುದ ವೈದಿಕ ಕಾಲರ್ದ್ ಬಳಕೆಡ್ ಉಂಡು.": "The Sanskrit language has been in use since the Vedic period around 3,500 years ago.",

        # Standard Bot Response Sentences (Tulu - Latin Script)
        "Namaskara! Encha uller? Yan eereg enchina sahaya malpodu?": "Greetings! How are you? How may I help you?",
        "Solmelu! Podu barpe, edde dina aavad.": "Thank you! I will take your leave, have a great day.",
        "Solmelu! Eereg sahaya maltinek enk kushi aand.": "Thank you! It was my pleasure to help you.",
        "Dokther mukya building da first floor du uller. Eereg ovvu vibhaga bodu?": "The doctor is on the first floor of the main building. Which department do you need?",
        "Dokther sandarshana portu kaande 9:00 gante ddu bayyag 5:00 gante mutta undu.": "Doctor consultation timings are from 9:00 AM morning to 5:00 PM evening.",
        "Yan eereg sahaya malpere sidha ulle! Eer daane prashne pandd panle.": "I am ready to assist you! Please tell me your question.",
        "Eereg bene aapundu pandd kendd sankata aand. Dayamalth rest gethonle and doctor n toole.": "Sad to hear you are unwell. Please take good rest and consult a doctor.",
        "And, naale doctor sandarshana portu tikundu. Eereg ovve vishaya gottavodu?": "Yes, consultation is available tomorrow with the doctor. What would you like to know?",
        "Edde! Dumbugu daane malpodu panle.": "Good! Please tell me what to do next.",
        "Sari, eereg bere daala mahiti bodaanda kenle.": "All right, let me know if you need any other information.",
        "Aapath sthiti ittnda dayamalth emergency room gu pole athnda 108 call malpule!": "In an emergency, please go to the emergency room immediately or call 108!",
        "Yan edde ulle! Eer encha uller?": "I am doing well! How are you?",
        "Enk sariyad artha aayiji. Dayamalth kudora panle.": "I didn't understand clearly. Could you please say it again?"
    }

    def generate_word_gloss(self, token: str, lang_code: str) -> Dict[str, str]:
        """Looks up or generates linguistic gloss for a single token."""
        clean = re.sub(r'[^\w\s\u0900-\u097F\u0C80-\u0CFF]', '', token).strip()
        clean_lower = clean.lower()

        if lang_code == "sa":
            if clean in self.SA_WORD_GLOSSES:
                gloss, grammar = self.SA_WORD_GLOSSES[clean]
                return {"token": token, "lemma": clean, "gloss": gloss, "grammar_note": grammar}
            elif clean_lower in self.SA_WORD_GLOSSES:
                gloss, grammar = self.SA_WORD_GLOSSES[clean_lower]
                return {"token": token, "lemma": clean_lower, "gloss": gloss, "grammar_note": grammar}

            # Check morphology analyzer
            morph = sa_morphology.analyze(clean)
            pos = morph.get("pos", "NOUN")
            case = morph.get("morphology", {}).get("case", "")
            concept = morph.get("concept", "")
            meaning = concept.lower().replace("_", " ") if concept else clean
            if case == "genitive":
                meaning = f"of {meaning}"
            elif case == "dative":
                meaning = f"to/for {meaning}"
            elif case == "locative":
                meaning = f"in/at {meaning}"
            return {"token": token, "lemma": morph.get("lemma", clean), "gloss": meaning, "grammar_note": f"{pos} {case}".strip()}

        elif lang_code == "tcy":
            if clean in self.TU_WORD_GLOSSES:
                gloss, grammar = self.TU_WORD_GLOSSES[clean]
                return {"token": token, "lemma": clean, "gloss": gloss, "grammar_note": grammar}
            elif clean_lower in self.TU_WORD_GLOSSES:
                gloss, grammar = self.TU_WORD_GLOSSES[clean_lower]
                return {"token": token, "lemma": clean_lower, "gloss": gloss, "grammar_note": grammar}

            # Check morphology analyzer
            morph = tulu_morphology.analyze(clean)
            pos = morph.get("pos", "NOUN")
            case = morph.get("morphology", {}).get("case", "")
            concept = morph.get("concept", "")
            meaning = concept.lower().replace("_", " ") if concept else clean
            if "locative" in case:
                meaning = f"in/at {meaning}"
            elif "dative" in case:
                meaning = f"to/for {meaning}"
            return {"token": token, "lemma": morph.get("lemma", clean), "gloss": meaning, "grammar_note": f"{pos} {case}".strip()}

        else:
            return {"token": token, "lemma": clean_lower, "gloss": clean_lower, "grammar_note": "English"}

    def _clean_name(self, name_str: str) -> str:
        """Cleans honorifics, visarga, and maps to English transliteration if known."""
        clean = re.sub(r'[:।!?]', '', name_str).strip()
        # Clean Sanskrit visarga if present
        if clean.endswith('ः'):
            clean = clean[:-1]
        
        # Check direct glosses in Sanskrit and Tulu lexicons
        if clean in self.SA_WORD_GLOSSES:
            return self.SA_WORD_GLOSSES[clean][0]
        if f"{clean}ः" in self.SA_WORD_GLOSSES:
            return self.SA_WORD_GLOSSES[f"{clean}ः"][0]
        if clean in self.TU_WORD_GLOSSES:
            return self.TU_WORD_GLOSSES[clean][0]

        # Common name transliterations
        name_map = {
            "राम": "Rama",
            "रमेश": "Ramesh",
            "कृष्ण": "Krishna",
            "ಶಿವ": "Shiva",
            "ರಮೇಶ್": "Ramesh",
            "ರಾಮ": "Rama"
        }
        return name_map.get(clean, clean)

    def translate_to_english(
        self,
        raw_text: str,
        lang_code: str,
        tokens: List[Dict[str, Any]],
        intent: str,
        is_bot_response: bool = False
    ) -> Tuple[str, List[Dict[str, str]], float]:
        """
        Translates Sanskrit or Tulu utterance into complete, grammatical English.
        Returns: (full_english_translation, word_glosses, confidence)
        """
        clean_text = raw_text.strip()
        word_glosses = []

        # Generate word-by-word glosses for all tokens
        for tok in tokens:
            surface = tok.get("surface_form", "")
            tok_type = tok.get("token_type", "WORD")
            if tok_type in ("PUNCT", "DANDA"):
                continue
            gloss_entry = self.generate_word_gloss(surface, lang_code)
            word_glosses.append(gloss_entry)

        # 1. Exact match in Idiomatic Translations Dictionary
        if clean_text in self.IDIOMATIC_TRANSLATIONS:
            return self.IDIOMATIC_TRANSLATIONS[clean_text], word_glosses, 0.98

        clean_lower = clean_text.lower()
        for k, v in self.IDIOMATIC_TRANSLATIONS.items():
            if k.lower() == clean_lower:
                return v, word_glosses, 0.96

        # 2. English input passthrough
        if lang_code == "en":
            return raw_text, word_glosses, 1.0

        # 3. Dynamic Bot Response Pattern Matches
        if is_bot_response:
            # Sanskrit Greeting with Name
            # e.g. "नमस्ते रामः महोदय! भवतः स्वागतम् अस्ति। अहं कथं साहाय्यं करवाणि?"
            m_sa_greet = re.match(
                r'नमस्ते\s+(.+?)\s+महोदय[!]?\s+भवतः\s+स्वागतम्\s+अस्ति[।.]?\s+अहं\s+कथं\s+साहाय्यं\s+करवाणि[?]?',
                clean_text
            )
            if m_sa_greet:
                raw_name = m_sa_greet.group(1)
                clean_name = self._clean_name(raw_name)
                return f"Greetings, Mr. {clean_name}! You are welcome. How may I help you?", word_glosses, 0.96

            # Tulu Latin Greeting with Name
            # e.g. "Namaskara Rama avar! Eerna swagatha. Yan eereg enchina sahaya malpodu?"
            m_tu_lat_greet = re.match(
                r'Namaskara\s+(.+?)\s+avar[!]?\s+Eerna\s+swagatha[.]?\s+Yan\s+eereg\s+enchina\s+sahaya\s+malpodu[?]?',
                clean_text,
                re.IGNORECASE
            )
            if m_tu_lat_greet:
                clean_name = self._clean_name(m_tu_lat_greet.group(1))
                return f"Greetings, {clean_name}! Welcome. How may I assist you?", word_glosses, 0.96

            # Tulu Kannada Greeting with Name
            # e.g. "ನಮಸ್ಕಾರ ರಮೇಶ್ ಅವರೇ! ಈರೆಗ್ ಸ್ವಾಗತ. ಯಾನ್ ಈರೆಗ್ ಎಂಚಿನ ಸಹಾಯ ಮಲ್ಪೊಡು?"
            m_tu_kn_greet = re.match(
                r'ನಮಸ್ಕಾರ\s+(.+?)\s+ಅವರೇ[!]?\s+ಈರೆಗ್\s+ಸ್ವಾಗತ[.]?\s+ಯಾನ್\s+ಈರೆಗ್\s+ಎಂಚಿನ\s+ಸಹಾಯ\s+ಮಲ್ಪೊಡು[?]?',
                clean_text
            )
            if m_tu_kn_greet:
                clean_name = self._clean_name(m_tu_kn_greet.group(1))
                return f"Greetings, {clean_name}! Welcome. How may I help you?", word_glosses, 0.96

            # "Your name is {name}."
            m_sa_name = re.match(r'भवतः\s+नाम\s+(.+?)\s+अस्ति[।.]?', clean_text)
            if m_sa_name:
                return f"Your name is {self._clean_name(m_sa_name.group(1))}.", word_glosses, 0.95

            m_tu_lat_name = re.match(r'Eerna\s+pudar\s+(.+?)\s+undu[.]?', clean_text, re.IGNORECASE)
            if m_tu_lat_name:
                return f"Your name is {self._clean_name(m_tu_lat_name.group(1))}.", word_glosses, 0.95

            m_tu_kn_name = re.match(r'ಈರೆನ\s+ಪುದರ್\s+(.+?)\s+ಉಂಡು[.]?', clean_text)
            if m_tu_kn_name:
                return f"Your name is {self._clean_name(m_tu_kn_name.group(1))}.", word_glosses, 0.95

        # 4. Dynamic User Request Pattern Matches
        if not is_bot_response:
            # Sanskrit User Introduction: "मम नाम {name}।" or "अहं {name} अस्मि।"
            m_sa_intro = re.match(r'मम\s+नाम\s+(.+?)[।.]?$', clean_text)
            if m_sa_intro:
                clean_name = self._clean_name(m_sa_intro.group(1))
                return f"My name is {clean_name}.", word_glosses, 0.96

            m_sa_iam = re.match(r'अहं\s+(.+?)\s+अस्मि[।.]?$', clean_text)
            if m_sa_iam:
                clean_name = self._clean_name(m_sa_iam.group(1))
                return f"I am {clean_name}.", word_glosses, 0.96

            # Tulu User Introduction: "ಎನ್ನ ಪುದರ್ {name}." or "enna pudar {name}"
            m_tu_intro_kn = re.match(r'ಎನ್ನ\s+ಪುದರ್\s+(.+?)[.]?$', clean_text)
            if m_tu_intro_kn:
                clean_name = self._clean_name(m_tu_intro_kn.group(1))
                return f"My name is {clean_name}.", word_glosses, 0.96

            m_tu_intro_lat = re.match(r'enna\s+pudar\s+(.+?)[.]?$', clean_text, re.IGNORECASE)
            if m_tu_intro_lat:
                clean_name = self._clean_name(m_tu_intro_lat.group(1))
                return f"My name is {clean_name}.", word_glosses, 0.96

            # User Location Query
            if intent == "LOCATION_QUERY":
                subject = "the doctor / hospital"
                for w in word_glosses:
                    g = w["gloss"].lower()
                    if "doctor" in g:
                        subject = "the doctor"
                        break
                    elif "hospital" in g:
                        subject = "the hospital"
                        break
                loc_str = " in Mangalore" if any("mangalore" in w["gloss"].lower() or "kudla" in w["token"].lower() for w in word_glosses) else ""
                return f"Where is {subject}{loc_str}?", word_glosses, 0.92

            # User Time / Appointment Query
            if intent == "TIME_QUERY":
                has_appt = any("appointment" in w["token"].lower() or "idiya" in w["token"].lower() for w in word_glosses)
                has_naale = any("naale" in w["token"].lower() or "tomorrow" in w["gloss"].lower() or "ನಾಲೆ" in w["token"] for w in word_glosses)
                if has_appt:
                    time_mod = "tomorrow" if has_naale else ""
                    return f"Doctor, is an appointment available {time_mod}?".strip(), word_glosses, 0.94
                return "When will the consultation take place / What are the timings?", word_glosses, 0.90

            # User Complaint
            if intent == "COMPLAINT":
                for w in word_glosses:
                    g = w["gloss"].lower()
                    if "headache" in g:
                        return "I have a headache.", word_glosses, 0.94
                    elif "stomach" in g:
                        return "I am suffering from a stomach ache.", word_glosses, 0.94
                    elif "fever" in g:
                        return "I have a fever.", word_glosses, 0.94
                    elif "tired" in g:
                        return "I am feeling tired / fatigued.", word_glosses, 0.94
                return "I am experiencing pain / feeling unwell.", word_glosses, 0.90

            # User Help
            if intent == "HELP":
                return "Please provide help and guidance.", word_glosses, 0.92

            # User Emergency
            if intent == "EMERGENCY":
                return "Emergency! Please provide urgent medical assistance immediately!", word_glosses, 0.95

            # User Slang Greeting e.g. "bro enna madthiya?"
            if "bro" in clean_lower:
                return "Brother/Friend, what are you doing?", word_glosses, 0.95

        # 5. Natural Sentence Synthesis Fallback
        # Clean glosses: remove meta-annotations like "noun", "verb", "term", slashes
        clean_gloss_tokens = []
        for w in word_glosses:
            g = w["gloss"].strip()
            # Strip multiple options if separated by slash (e.g. "is / exists" -> "is")
            if " / " in g:
                g = g.split(" / ")[0].strip()
            if g.lower() in ("term", "particle", "obj", "suffix"):
                continue
            clean_gloss_tokens.append(g)

        if clean_gloss_tokens:
            assembled = " ".join(clean_gloss_tokens).strip()
            # Punctuate cleanly
            if not assembled.endswith(('.', '?', '!')):
                assembled += '.'
            return assembled[0].upper() + assembled[1:], word_glosses, 0.80

        return raw_text, word_glosses, 0.60

translator = MultilingualEnglishTranslator()
