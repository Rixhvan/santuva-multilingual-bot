import React, { useState } from 'react';
import { NLPAnalysis, DialogueState } from '../models/types';
import { TuluTierCard } from './TuluTierCard';
import { 
  Cpu, Layers, Tag, HelpCircle, 
  Workflow, Database, Shuffle, Sparkles, X,
  Languages, Download, Check, MessageSquare
} from 'lucide-react';

interface NLPDeveloperPanelProps {
  analysis: NLPAnalysis | null;
  dialogueState: DialogueState | null;
  source: 'request' | 'response';
  hasRequestAnalysis?: boolean;
  hasResponseAnalysis?: boolean;
  onSelectSource?: (source: 'request' | 'response') => void;
  onClose: () => void;
}

export const NLPDeveloperPanel: React.FC<NLPDeveloperPanelProps> = ({
  analysis,
  dialogueState,
  source,
  hasRequestAnalysis,
  hasResponseAnalysis,
  onSelectSource,
  onClose,
}) => {
  const [copied, setCopied] = useState(false);

  if (!analysis) {
    return (
      <div className="dev-panel">
        <div className="dev-panel-header">
          <span style={{ fontWeight: 500, fontSize: '0.86rem', color: 'var(--text-muted)' }}>
            Learn How Santuva Understands You
          </span>
          <button onClick={onClose} className="btn-icon">
            <X size={16} />
          </button>
        </div>
        <div style={{ padding: 32, textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          <div style={{ marginBottom: 8 }}>See how Santuva understands your message step by step.</div>
          Select any message in the chat to see how Santuva understands it, step by step, along with its English meaning.
        </div>
      </div>
    );
  }

  const lang = analysis.language_info;
  const intent = analysis.intent_info;
  const sem = analysis.semantic_rep;

  const handleExportJson = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(analysis, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `nlp_${source}_trace_${Date.now()}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="dev-panel">
      {/* Header with Source Switcher & Actions */}
      <div className="dev-panel-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontWeight: 600, fontSize: '0.88rem', color: 'var(--text-main)' }}>
            Learn How Santuva Understands You
          </span>

          {/* Request vs Response Switcher */}
          {onSelectSource && (hasRequestAnalysis || hasResponseAnalysis) && (
            <div style={{ display: 'flex', background: '#262626', padding: '2px', borderRadius: '8px', border: '1px solid #333333', marginLeft: '6px' }}>
              <button
                onClick={() => onSelectSource('request')}
                disabled={!hasRequestAnalysis}
                style={{
                  background: source === 'request' ? '#383838' : 'transparent',
                  color: source === 'request' ? '#ffffff' : '#888888',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '3px 8px',
                  fontSize: '0.72rem',
                  fontWeight: 500,
                  cursor: hasRequestAnalysis ? 'pointer' : 'default',
                  opacity: hasRequestAnalysis ? 1 : 0.4,
                  transition: 'all 0.15s ease'
                }}
              >
                Your Message
              </button>
              <button
                onClick={() => onSelectSource('response')}
                disabled={!hasResponseAnalysis}
                style={{
                  background: source === 'response' ? '#383838' : 'transparent',
                  color: source === 'response' ? '#ffffff' : '#888888',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '3px 8px',
                  fontSize: '0.72rem',
                  fontWeight: 500,
                  cursor: hasResponseAnalysis ? 'pointer' : 'default',
                  opacity: hasResponseAnalysis ? 1 : 0.4,
                  transition: 'all 0.15s ease'
                }}
              >
                Santuva's Reply
              </button>
            </div>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <button
            onClick={handleExportJson}
            className="btn-icon"
            title="Export JSON Trace"
          >
            {copied ? <Check size={14} color="#10b981" /> : <Download size={14} />}
          </button>
          <button onClick={onClose} className="btn-icon" title="Close Panel">
            <X size={16} />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="dev-panel-content">
        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', padding: '2px 4px' }}>
          See how Santuva understands your message step by step.
        </div>

        {/* Source banner */}
        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 6, padding: '2px 4px' }}>
          <MessageSquare size={13} />
          <span>Showing how Santuva understood: <strong style={{ color: 'var(--text-main)' }}>{source === 'request' ? 'Your message' : "Santuva's reply"}</strong></span>
        </div>

        {/* 1. Language & Script */}
        <div className="nlp-card">
          <div className="nlp-card-title">
            <Cpu size={13} />
            1. Which language is this?
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '0.82rem' }}>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Language:</span>{' '}
              <strong style={{ color: 'var(--text-main)' }}>{lang.language}</strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Script:</span>{' '}
              <strong style={{ color: 'var(--text-main)' }}>{lang.script}</strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Confidence:</span>{' '}
              <strong style={{ color: 'var(--text-main)' }}>
                {(lang.confidence * 100).toFixed(1)}%
              </strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Mixed languages:</span>{' '}
              <strong style={{ color: 'var(--text-main)' }}>
                {lang.is_code_switched ? 'Yes (Mixed)' : 'No'}
              </strong>
            </div>
          </div>
        </div>

        {/* 2. Slang & Informal Handling */}
        {analysis.slang_normalized && (
          <div className="nlp-card">
            <div className="nlp-card-title">
              <Sparkles size={13} />
              2. Casual words made clear
            </div>
            {analysis.slang_transformations.map((t, idx) => (
              <div key={idx} style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: 4 }}>
                <span style={{ textDecoration: 'line-through', opacity: 0.7 }}>{t.slang}</span>
                {' → '}
                <span style={{ color: 'var(--text-main)', fontWeight: 600 }}>{t.normalized}</span>
                <span style={{ marginLeft: 8, fontSize: '0.72rem', color: 'var(--text-muted)' }}>({t.concept})</span>
              </div>
            ))}
          </div>
        )}

        {/* 3. Code-Switching Token Attribution */}
        {lang.is_code_switched && (
          <div className="nlp-card">
            <div className="nlp-card-title">
              <Shuffle size={13} />
              3. Mixed languages in your message
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {analysis.code_switching_tokens.map((tok, idx) => (
                <span
                  key={idx}
                  style={{
                    padding: '3px 8px',
                    borderRadius: '6px',
                    fontSize: '0.75rem',
                    background: '#262626',
                    color: 'var(--text-main)',
                    border: '1px solid #383838',
                  }}
                >
                  <strong>{tok.token}</strong> ({tok.language})
                </span>
              ))}
            </div>
          </div>
        )}

        {/* 4. Sanskrit Sandhi Decomposition */}
        {analysis.sandhi_analysis && analysis.sandhi_analysis.length > 0 && (
          <div className="nlp-card">
            <div className="nlp-card-title">
              <Layers size={13} />
              4. Sanskrit joined words split apart
            </div>
            {analysis.sandhi_analysis.map((s, idx) => (
              <div key={idx} style={{ fontSize: '0.8rem', marginBottom: 6 }}>
                <div>
                  <strong style={{ color: 'var(--text-main)' }}>{s.compound}</strong>
                  {' = '}
                  <span style={{ color: 'var(--text-secondary)' }}>{s.components.join(' + ')}</span>
                </div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                  Rule: {s.rule_type} | Confidence: {(s.confidence * 100).toFixed(0)}%
                </div>
              </div>
            ))}
          </div>
        )}

        {/* 5. Tokens, Lemmas, POS, Morphology Table */}
        <div className="nlp-card">
          <div className="nlp-card-title">
            <Workflow size={13} />
            2. Words, base forms and word types
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table className="token-table">
              <thead>
                <tr>
                  <th>Word</th>
                  <th>Base form</th>
                  <th>Word type</th>
                  <th>Grammar details / Concept</th>
                </tr>
              </thead>
              <tbody>
                {analysis.tokens.map((t, idx) => (
                  <tr key={idx}>
                    <td><strong>{t.surface_form}</strong></td>
                    <td style={{ color: 'var(--text-secondary)' }}>{t.lemma}</td>
                    <td><span className="pos-tag-pill">{t.pos}</span></td>
                    <td>
                      {t.semantic_concept && (
                        <span style={{ fontSize: '0.72rem', background: '#2a2a2a', padding: '1px 5px', borderRadius: '4px', marginRight: 4 }}>
                          {t.semantic_concept}
                        </span>
                      )}
                      {t.morphology && Object.keys(t.morphology).length > 0 && (
                        <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', display: 'block', marginTop: 2 }}>
                          {JSON.stringify(t.morphology).replace(/[{"}]/g, '').replace(/:/g, '=')}
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* === REQUIREMENT: Complete English Translation & Semantic Gloss placed DIRECTLY after Tokens, Morphology & Lemmatization === */}
        <div className="nlp-card">
          <div className="nlp-card-title">
            <Languages size={13} />
            3. What it means in English
          </div>

          {/* Full Sentence Translation Box */}
          <div className="translation-box">
            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.04em', color: 'var(--text-muted)', marginBottom: 4, fontWeight: 600 }}>
              Complete English Meaning ({source === 'request' ? 'Your message' : "Santuva's reply"})
            </div>
            <div className="translation-quote">
              "{analysis.english_translation || 'Direct English input'}"
            </div>
            {analysis.translation_confidence && (
              <div style={{ marginTop: 6, fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                Confidence: <strong>{(analysis.translation_confidence * 100).toFixed(0)}%</strong>
              </div>
            )}
          </div>

          {/* Word-by-word gloss table */}
          {analysis.word_glosses && analysis.word_glosses.length > 0 && (
            <div style={{ marginTop: 8 }}>
              <div style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6, textTransform: 'uppercase' }}>
                Word-by-Word Meaning:
              </div>
              <div style={{ overflowX: 'auto' }}>
                <table className="token-table">
                  <thead>
                    <tr>
                      <th>Word</th>
                      <th>Role in sentence</th>
                      <th>English Meaning</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analysis.word_glosses.map((g, idx) => (
                      <tr key={idx}>
                        <td><strong>{g.token}</strong></td>
                        <td style={{ color: 'var(--text-muted)', fontSize: '0.72rem' }}>{g.grammar_note}</td>
                        <td style={{ color: 'var(--text-main)', fontWeight: 500 }}>{g.gloss}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>

        {/* 7. Named Entity Recognition */}
        <div className="nlp-card">
          <div className="nlp-card-title">
            <Tag size={13} />
            4. Names and important things found
          </div>
          {analysis.entities.length === 0 ? (
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>No names or important things found.</div>
          ) : (
            <div>
              {analysis.entities.map((e, idx) => (
                <span key={idx} className="entity-tag-pill">
                  <strong>{e.text}</strong>
                  <span style={{ opacity: 0.65, fontSize: '0.68rem' }}>[{e.label}]</span>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* 8. Intent & Semantic Understanding */}
        <div className="nlp-card">
          <div className="nlp-card-title">
            <HelpCircle size={13} />
            5. What you want to do (your intent)
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '0.82rem' }}>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>What you want:</span>{' '}
              <strong style={{ color: 'var(--text-main)' }}>{intent.intent}</strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Confidence:</span>{' '}
              <strong style={{ color: 'var(--text-main)' }}>
                {(intent.confidence * 100).toFixed(1)}%
              </strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Type of message:</span>{' '}
              <strong style={{ color: 'var(--text-main)' }}>{sem.dialogue_act}</strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Concept:</span>{' '}
              <strong style={{ color: 'var(--text-secondary)' }}>{sem.shared_concept_id || 'N/A'}</strong>
            </div>
          </div>
        </div>

        {/* 9. Dialogue State Memory */}
        {dialogueState && (
          <div className="nlp-card">
            <div className="nlp-card-title">
              <Database size={13} />
              6. What Santuva remembers in this chat
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: 4 }}>
              <div>Messages so far: <strong>{dialogueState.turn_count}</strong></div>
              <div>Current Topic: <strong>{dialogueState.current_topic || 'None'}</strong></div>
              <div>
                Things mentioned so far:{' '}
                <code>{JSON.stringify(dialogueState.accumulated_entities)}</code>
              </div>
            </div>
          </div>
        )}

        {/* 10. Tulu Architecture Transparency */}
        {lang.language_code === 'tcy' && <TuluTierCard />}
      </div>
    </div>
  );
};
