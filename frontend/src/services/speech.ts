// Unified Multilingual Speech Engine
// Ensures the EXACT same voice is used across every message in the entire conversation.
// Converts Devanagari (Sanskrit) and Kannada (Tulu) characters into phonetic Roman script
// so the unified browser voice can articulate Sanskrit and Tulu flawlessly without requiring
// external language packs or falling silent.

const DEV_CONSONANTS: Record<string, string> = {
  'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
  'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'ny',
  'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
  'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
  'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
  'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v',
  'श': 'sh', 'ष': 'sh', 'स': 's', 'ह': 'h',
  'क्ष': 'ksh', 'त्र': 'tr', 'ज्ञ': 'gy'
};

const DEV_VOWELS: Record<string, string> = {
  'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo',
  'ऋ': 'ri', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au'
};

const DEV_MATRAS: Record<string, string> = {
  'ा': 'aa', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo', 'ृ': 'ri',
  'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au'
};

const DEV_MODIFIERS: Record<string, string> = {
  'ं': 'm', 'ः': 'h', '्': ''
};

const KN_CONSONANTS: Record<string, string> = {
  'ಕ': 'k', 'ಖ': 'kh', 'ಗ': 'g', 'ಘ': 'gh', 'ಙ': 'ng',
  'ಚ': 'ch', 'ಛ': 'chh', 'ಜ': 'j', 'ಝ': 'jh', 'ಞ': 'ny',
  'ಟ': 't', 'ಠ': 'th', 'ಡ': 'd', 'ಢ': 'dh', 'ಣ': 'n',
  'ತ': 't', 'ಥ': 'th', 'ದ': 'd', 'ಧ': 'dh', 'ನ': 'n',
  'ಪ': 'p', 'ಫ': 'ph', 'ಬ': 'b', 'ಭ': 'bh', 'ಮ': 'm',
  'ಯ': 'y', 'ರ': 'ra', 'ಲ': 'la', 'ವ': 'va',
  'ಶ': 'sha', 'ಷ': 'sha', 'ಸ': 'sa', 'ಹ': 'ha', 'ಳ': 'la'
};

const KN_VOWELS: Record<string, string> = {
  'ಅ': 'a', 'ಆ': 'aa', 'ಇ': 'i', 'ಈ': 'ee', 'ಉ': 'u', 'ಊ': 'oo',
  'ಋ': 'ru', 'ಎ': 'e', 'ಏ': 'ae', 'ಐ': 'ai', 'ಒ': 'o', 'ಓ': 'oa', 'ಔ': 'au'
};

const KN_MATRAS: Record<string, string> = {
  'ಾ': 'aa', 'ಿ': 'i', 'ೀ': 'ee', 'ು': 'u', 'ೂ': 'oo', 'ೃ': 'ru',
  'ೆ': 'e', 'ೇ': 'ae', 'ೈ': 'ai', 'ೊ': 'o', 'ೋ': 'oa', 'ೌ': 'au'
};

const KN_MODIFIERS: Record<string, string> = {
  'ಂ': 'm', 'ಃ': 'h', '್': ''
};

export const transliterateIndicToPhonetic = (text: string): string => {
  const res: string[] = [];
  const n = text.length;
  let i = 0;

  while (i < n) {
    const ch = text[i];
    const nextCh = i + 1 < n ? text[i + 1] : null;

    if (ch === '।' || ch === '॥') {
      res.push('. ');
      i += 1;
      continue;
    }

    if (DEV_CONSONANTS[ch]) {
      const base = DEV_CONSONANTS[ch];
      if (nextCh === '्') {
        res.push(base);
        i += 2;
        continue;
      } else if (nextCh && DEV_MATRAS[nextCh]) {
        res.push(base + DEV_MATRAS[nextCh]);
        i += 2;
        continue;
      } else {
        res.push(base + 'a');
        i += 1;
        continue;
      }
    }

    if (KN_CONSONANTS[ch]) {
      const base = KN_CONSONANTS[ch];
      if (nextCh === '್') {
        res.push(base);
        i += 2;
        continue;
      } else if (nextCh && KN_MATRAS[nextCh]) {
        res.push(base + KN_MATRAS[nextCh]);
        i += 2;
        continue;
      } else {
        res.push(base + 'a');
        i += 1;
        continue;
      }
    }

    if (DEV_VOWELS[ch]) {
      res.push(DEV_VOWELS[ch]);
    } else if (KN_VOWELS[ch]) {
      res.push(KN_VOWELS[ch]);
    } else if (DEV_MODIFIERS[ch]) {
      res.push(DEV_MODIFIERS[ch]);
    } else if (KN_MODIFIERS[ch]) {
      res.push(KN_MODIFIERS[ch]);
    } else {
      res.push(ch);
    }
    i += 1;
  }

  return res.join('');
};

let cachedUnifiedVoice: SpeechSynthesisVoice | null = null;

const getUnifiedVoice = (): SpeechSynthesisVoice | null => {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) return null;
  if (cachedUnifiedVoice) return cachedUnifiedVoice;

  const voices = window.speechSynthesis.getVoices();
  if (voices && voices.length > 0) {
    // Pick the primary system default voice
    cachedUnifiedVoice = voices.find((v) => v.default) || voices[0] || null;
    return cachedUnifiedVoice;
  }
  return null;
};

if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
  getUnifiedVoice();
  window.speechSynthesis.onvoiceschanged = () => {
    getUnifiedVoice();
  };
}

export const speechService = {
  speak(text: string, onStateChange?: (speaking: boolean) => void) {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    // Check if text has Indic script (Devanagari or Kannada)
    const hasIndic = /[\u0900-\u097F\u0C80-\u0CFF]/.test(text);
    const spokenText = hasIndic ? transliterateIndicToPhonetic(text) : text;

    const voice = getUnifiedVoice();
    const utterance = new SpeechSynthesisUtterance(spokenText);

    if (voice) {
      utterance.voice = voice;
      utterance.lang = voice.lang || 'en-US';
    } else {
      utterance.lang = 'en-US';
    }

    utterance.rate = 0.90;
    utterance.pitch = 1.0;

    utterance.onstart = () => {
      if (onStateChange) onStateChange(true);
    };

    utterance.onend = () => {
      if (onStateChange) onStateChange(false);
    };

    utterance.onerror = (e) => {
      console.warn('Speech playback notification:', e);
      if (onStateChange) onStateChange(false);
    };

    window.speechSynthesis.speak(utterance);
  },

  stop() {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  },

  getDefaultVoiceName(): string {
    const voice = getUnifiedVoice();
    return voice ? voice.name : 'System Default';
  }
};
