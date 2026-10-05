import React, { useState, useEffect, useRef } from 'react';
import { MessageItem, NLPAnalysis, DialogueState } from './models/types';
import { chatApi } from './services/api';
import { LanguageSelector } from './components/LanguageSelector';
import { ChatMessageItem } from './components/ChatMessageItem';
import { NLPDeveloperPanel } from './components/NLPDeveloperPanel';
import { BenchmarkModal } from './components/BenchmarkModal';
import { speechService } from './services/speech';
import { 
  ArrowUp, Mic, MicOff, RotateCcw, Sliders, 
  Sparkles 
} from 'lucide-react';
import './style.css';

export const App: React.FC = () => {
  const [messages, setMessages] = useState<MessageItem[]>([
    {
      id: 'welcome',
      sender: 'bot',
      text: 'Welcome! I am Santuva, a multilingual conversational chatbot for Sanskrit, English, and Tulu. You can converse naturally in any of these languages, use code-switching, or informal coastal slang.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [showDevPanel, setShowDevPanel] = useState(true);
  const [showBenchmarkModal, setShowBenchmarkModal] = useState(false);

  // Dual analysis states for current active turn
  const [activeRequestAnalysis, setActiveRequestAnalysis] = useState<NLPAnalysis | null>(null);
  const [activeResponseAnalysis, setActiveResponseAnalysis] = useState<NLPAnalysis | null>(null);
  const [activeSource, setActiveSource] = useState<'request' | 'response'>('request');
  const [activeDialogueState, setActiveDialogueState] = useState<DialogueState | null>(null);
  const [selectedMessageId, setSelectedMessageId] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize Speech Recognition if supported
  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInputText(transcript);
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const toggleSpeechRecognition = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge.');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      if (selectedLanguage === 'sa') {
        recognitionRef.current.lang = 'hi-IN';
      } else if (selectedLanguage === 'tcy') {
        recognitionRef.current.lang = 'kn-IN';
      } else {
        recognitionRef.current.lang = 'en-US';
      }
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (err) {
        setIsListening(false);
      }
    }
  };

  const handleSend = async (overrideText?: string) => {
    const textToSend = overrideText || inputText;
    if (!textToSend.trim() || isProcessing) return;

    const userMessageId = `user-${Date.now()}`;
    const userMessage: MessageItem = {
      id: userMessageId,
      sender: 'user',
      text: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      analysisSource: 'request',
    };

    setMessages((prev) => [...prev, userMessage]);
    if (!overrideText) setInputText('');
    setIsProcessing(true);

    try {
      const response = await chatApi.sendMessage(
        textToSend,
        'default',
        selectedLanguage || undefined
      );

      const botMessageId = `bot-${Date.now()}`;
      const botMessage: MessageItem = {
        id: botMessageId,
        sender: 'bot',
        text: response.response_text,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        response: response,
        nlpAnalysis: response.response_nlp_analysis || undefined,
        dialogueState: response.dialogue_state,
        analysisSource: 'response',
      };

      // Update user message with its request NLP analysis
      setMessages((prev) => [
        ...prev.map((msg) =>
          msg.id === userMessageId
            ? {
                ...msg,
                nlpAnalysis: response.nlp_analysis,
                dialogueState: response.dialogue_state,
                response: response,
              }
            : msg
        ),
        botMessage,
      ]);

      // Cache both request and response analyses for rapid switching
      setActiveRequestAnalysis(response.nlp_analysis);
      setActiveResponseAnalysis(response.response_nlp_analysis || null);
      setActiveDialogueState(response.dialogue_state);
      setActiveSource('request');
      setSelectedMessageId(userMessageId);
      setShowDevPanel(true);
    } catch (err: any) {
      const errorMessage: MessageItem = {
        id: `bot-err-${Date.now()}`,
        sender: 'bot',
        text: `Error connecting to NLP service: ${err.message || 'Server error'}. Please ensure FastAPI backend is running.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleClear = async () => {
    speechService.stop();
    await chatApi.resetConversation('default').catch(() => {});
    setMessages([
      {
        id: 'reset',
        sender: 'bot',
        text: 'Conversation memory cleared. Ready for a new dialogue.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);
    setActiveRequestAnalysis(null);
    setActiveResponseAnalysis(null);
    setActiveDialogueState(null);
    setSelectedMessageId(null);
  };

  const handleInspect = (message: MessageItem, analysis: NLPAnalysis, source: 'request' | 'response') => {
    setSelectedMessageId(message.id);
    setActiveSource(source);
    setShowDevPanel(true);

    if (source === 'request') {
      setActiveRequestAnalysis(analysis);
      if (message.response?.response_nlp_analysis) {
        setActiveResponseAnalysis(message.response.response_nlp_analysis);
      }
    } else {
      setActiveResponseAnalysis(analysis);
      if (message.response?.nlp_analysis) {
        setActiveRequestAnalysis(message.response.nlp_analysis);
      }
    }

    const diag = message.dialogueState || message.response?.dialogue_state;
    if (diag) {
      setActiveDialogueState(diag);
    }
  };

  const exemplarPrompts = [
    { label: 'मम नाम रामः।', text: 'मम नाम रामः।' },
    { label: 'चिकित्सकः कुत्र अस्ति?', text: 'चिकित्सकः कुत्र अस्ति?' },
    { label: 'Can you tell me where the doctor is?', text: 'Can you tell me where the doctor is?' },
    { label: 'Doctor naale appointment idiya?', text: 'Doctor naale appointment idiya?' },
    { label: 'bro enna madthiya?', text: 'bro enna madthiya?' },
    { label: 'Tell me about Sanskrit', text: 'Tell me about Sanskrit.' },
    { label: 'When was it used?', text: 'When was it used?' },
  ];

  const currentDisplayedAnalysis = activeSource === 'request' ? activeRequestAnalysis : (activeResponseAnalysis || activeRequestAnalysis);

  return (
    <div className="app-container">
      {/* Benchmark Results Modal */}
      <BenchmarkModal
        isOpen={showBenchmarkModal}
        onClose={() => setShowBenchmarkModal(false)}
      />

      {/* Main Chat Section (ChatGPT Aesthetic) */}
      <section className="chat-section">
        {/* Top Header */}
        <header className="app-header">
          <div className="brand-title">
            <h1 style={{ fontWeight: 600 }}>
              Santuva
            </h1>
            <div style={{ display: 'flex', gap: '4px', marginLeft: 8 }}>
              <span className="lang-pill-subtle">Sanskrit</span>
              <span className="lang-pill-subtle">English</span>
              <span className="lang-pill-subtle">Tulu</span>
            </div>
          </div>

          <div className="header-controls">
            <LanguageSelector
              selectedLanguage={selectedLanguage}
              onChange={setSelectedLanguage}
            />

            <button
              onClick={handleClear}
              className="btn-icon"
              title="Clear conversation context"
            >
              <RotateCcw size={15} />
            </button>

            <button
              onClick={() => setShowDevPanel(!showDevPanel)}
              className={`btn-icon ${showDevPanel ? 'active' : ''}`}
              title="Toggle 'Learn How Santuva Understands You' panel"
            >
              <Sliders size={15} />
            </button>
          </div>
        </header>

        {/* Suggestions Bar */}
        <div className="suggestions-bar">
          <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', fontWeight: 500, display: 'flex', alignItems: 'center', gap: 4 }}>
            <Sparkles size={12} /> Try:
          </span>
          {exemplarPrompts.map((p, idx) => (
            <button
              key={idx}
              className="suggestion-chip"
              onClick={() => handleSend(p.text)}
            >
              {p.label}
            </button>
          ))}
        </div>

        {/* Messages Stream */}
        <div className="messages-container">
          {messages.map((m) => (
            <ChatMessageItem
              key={m.id}
              message={m}
              onInspect={handleInspect}
              isSelected={m.id === selectedMessageId}
            />
          ))}
          {isProcessing && (
            <div className="message-row bot">
              <div className="message-content-wrapper">
                <div className="bubble" style={{ color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.88rem' }}>
                  Santuva is understanding your message...
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Floating Input Area (ChatGPT Style Pill) */}
        <div className="input-area-wrapper">
          <div className="input-pill-container">
            <input
              type="text"
              className="chat-input"
              placeholder="Ask anything in Sanskrit, English, or Tulu (e.g., 'Doctor naale appointment idiya?')..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleSend();
              }}
              disabled={isProcessing}
            />

            <button
              className={`btn-mic-chat ${isListening ? 'listening' : ''}`}
              title={isListening ? 'Stop listening' : 'Speech input (Microphone)'}
              onClick={toggleSpeechRecognition}
            >
              {isListening ? <MicOff size={18} /> : <Mic size={18} />}
            </button>

            <button
              className="btn-round-send"
              onClick={() => handleSend()}
              disabled={!inputText.trim() || isProcessing}
              title="Send message"
            >
              <ArrowUp size={18} strokeWidth={2.5} />
            </button>
          </div>
          <div className="disclaimer-text">
            Santuva · Multilingual chatbot for Sanskrit, English, and Tulu
          </div>
        </div>
      </section>

      {/* Right Side: Developer NLP Dashboard (ChatGPT Drawer Style) */}
      {showDevPanel && (
        <NLPDeveloperPanel
          analysis={currentDisplayedAnalysis}
          dialogueState={activeDialogueState}
          source={activeSource}
          hasRequestAnalysis={Boolean(activeRequestAnalysis)}
          hasResponseAnalysis={Boolean(activeResponseAnalysis)}
          onSelectSource={(source) => setActiveSource(source)}
          onClose={() => setShowDevPanel(false)}
        />
      )}
    </div>
  );
};
