import React, { useState } from 'react';
import { MessageItem, NLPAnalysis } from '../models/types';
import { User, Bot, Code2, Volume2, VolumeX } from 'lucide-react';
import { speechService } from '../services/speech';

interface ChatMessageItemProps {
  message: MessageItem;
  onInspect: (message: MessageItem, analysis: NLPAnalysis, source: 'request' | 'response') => void;
  isSelected: boolean;
}

export const ChatMessageItem: React.FC<ChatMessageItemProps> = ({
  message,
  onInspect,
  isSelected,
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const isUser = message.sender === 'user';
  
  // Resolve relevant analysis for this message
  // For user: user's request analysis
  // For bot: bot's response analysis (or fallback to response.response_nlp_analysis)
  const analysis: NLPAnalysis | undefined = isUser
    ? (message.nlpAnalysis || message.response?.nlp_analysis)
    : (message.nlpAnalysis || message.response?.response_nlp_analysis || message.response?.nlp_analysis);

  const langCode = analysis?.language_info.language_code || (isUser ? 'en' : 'en');
  const langName = analysis?.language_info.language || '';
  const isCodeSwitched = analysis?.language_info.is_code_switched;
  const switchedLangs = analysis?.language_info.code_switched_languages || [];
  const translation = analysis?.english_translation;

  const fontClass = langCode === 'sa' ? 'sa-font' : langCode === 'tcy' ? 'tcy-font' : '';

  // Use the exact same voice used across the entire conversation
  const handleSpeak = () => {
    if (isPlaying) {
      speechService.stop();
      setIsPlaying(false);
      return;
    }
    speechService.speak(message.text, (speaking) => {
      setIsPlaying(speaking);
    });
  };

  const handleInspectClick = () => {
    if (!analysis) return;
    const source = isUser ? 'request' : 'response';
    onInspect(message, analysis, source);
  };

  return (
    <div className={`message-row ${message.sender}`}>
      {!isUser && (
        <div className="avatar bot-avatar">
          <Bot size={18} />
        </div>
      )}

      <div className="message-content-wrapper">
        <div 
          className={`bubble ${fontClass} ${isSelected ? 'selected-outline' : ''}`}
        >
          {message.text}

          {/* Meaning / English translation preview when text is in Sanskrit or Tulu */}
          {translation && langCode !== 'en' && (
            <div className="bubble-translation-preview">
              <span style={{ opacity: 0.7, marginRight: 4, fontWeight: 500 }}>Meaning:</span>
              "{translation}"
            </div>
          )}
        </div>

        {/* Minimal metadata and actions */}
        <div className="bubble-meta">
          <span>{message.timestamp}</span>

          {/* Audio TTS with consistent voice */}
          <button
            onClick={handleSpeak}
            className="btn-icon"
            style={{ width: 24, height: 24 }}
            title={isPlaying ? 'Stop voice' : 'Listen with unified voice'}
          >
            {isPlaying ? <VolumeX size={13} style={{ color: '#ef4444' }} /> : <Volume2 size={13} />}
          </button>

          {/* Language badge */}
          {analysis && (
            <span className="lang-pill-subtle">
              {isCodeSwitched ? `Mixed (${switchedLangs.join('+')})` : langName}
            </span>
          )}

          {/* NLP Trace button on BOTH User Request and Bot Response */}
          {analysis && (
            <button
              onClick={handleInspectClick}
              className={`btn-trace ${isSelected ? 'active' : ''}`}
              title={isUser ? 'Inspect NLP pipeline trace for user request' : 'Inspect NLP pipeline trace and meaning for bot response'}
            >
              <Code2 size={12} />
              <span>{isUser ? 'Trace (Request)' : 'Trace (Response)'}</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
