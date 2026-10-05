import React from 'react';
import { Info, CheckCircle2, AlertTriangle, ShieldAlert } from 'lucide-react';

export const TuluTierCard: React.FC = () => {
  return (
    <div className="nlp-card">
      <div className="nlp-card-title">
        <Info size={14} color="#10b981" />
        Tulu NLP Resource Architecture (Section 32)
      </div>
      <p style={{ fontSize: '0.78rem', color: '#94a3b8', marginBottom: '10px', lineHeight: 1.4 }}>
        Tulu is a low-resource Dravidian language. The system transparently operates on a 3-tier hybrid architecture:
      </p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.76rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '4px 6px', background: 'rgba(16, 185, 129, 0.08)', borderRadius: '6px' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#34d399' }}>
            <CheckCircle2 size={13} /> FULL SUPPORT
          </span>
          <span style={{ color: '#cbd5e1' }}>Lexicon Lookup, Morphology, Slang Normalization</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '4px 6px', background: 'rgba(245, 158, 11, 0.08)', borderRadius: '6px' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#fbbf24' }}>
            <AlertTriangle size={13} /> PARTIAL SUPPORT
          </span>
          <span style={{ color: '#cbd5e1' }}>Suffix Stemming, POS Tagging, Code-Switching</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '4px 6px', background: 'rgba(239, 68, 68, 0.08)', borderRadius: '6px' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#f87171' }}>
            <ShieldAlert size={13} /> FALLBACK SUPPORT
          </span>
          <span style={{ color: '#cbd5e1' }}>Semantic Vector Similarity, Dialogue Clarification</span>
        </div>
      </div>
    </div>
  );
};
