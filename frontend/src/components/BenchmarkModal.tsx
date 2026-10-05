import React, { useState, useEffect } from 'react';
import { BenchmarkMetric } from '../models/types';
import { chatApi } from '../services/api';
import { Award, CheckCircle, RefreshCw, X, AlertCircle } from 'lucide-react';

interface BenchmarkModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const BenchmarkModal: React.FC<BenchmarkModalProps> = ({ isOpen, onClose }) => {
  const [metrics, setMetrics] = useState<BenchmarkMetric[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMetrics = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await chatApi.getEvaluationMetrics();
      setMetrics(data.metrics);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch evaluation metrics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchMetrics();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.75)',
        backdropFilter: 'blur(4px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: 20,
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: '#0f172a',
          border: '1px solid #334155',
          borderRadius: 16,
          width: '100%',
          maxWidth: 820,
          boxShadow: '0 20px 40px rgba(0,0,0,0.5)',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div
          style={{
            padding: '18px 24px',
            borderBottom: '1px solid #1e293b',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: '#131b2e',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <Award size={22} color="#f59e0b" />
            <div>
              <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc' }}>
                Multilingual NLP Benchmark Evaluation
              </h2>
              <p style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                Standardized Evaluation across 300 Curated Sentences (100 Sanskrit, 100 English, 100 Tulu)
              </p>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <button
              onClick={fetchMetrics}
              disabled={loading}
              className="btn-icon"
              style={{ width: 32, height: 32 }}
              title="Re-run evaluation benchmark"
            >
              <RefreshCw size={15} className={loading ? 'animate-spin' : ''} />
            </button>
            <button
              onClick={onClose}
              className="btn-icon"
              style={{ width: 32, height: 32 }}
              title="Close modal"
            >
              <X size={18} />
            </button>
          </div>
        </div>

        {/* Content */}
        <div style={{ padding: 24, maxHeight: '70vh', overflowY: 'auto' }}>
          {loading && (
            <div style={{ textAlign: 'center', padding: 40, color: '#94a3b8' }}>
              <RefreshCw size={28} className="animate-spin" style={{ margin: '0 auto 12px' }} />
              <div>Running evaluation benchmark across 300 test sentences...</div>
            </div>
          )}

          {error && (
            <div style={{ padding: 16, background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: 8, color: '#fca5a5', display: 'flex', gap: 10 }}>
              <AlertCircle size={20} color="#ef4444" />
              <div>{error}</div>
            </div>
          )}

          {!loading && !error && metrics.length > 0 && (
            <div>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid #334155', color: '#94a3b8' }}>
                    <th style={{ textAlign: 'left', padding: '10px 12px' }}>Language</th>
                    <th style={{ textAlign: 'center', padding: '10px 12px' }}>Samples</th>
                    <th style={{ textAlign: 'center', padding: '10px 12px' }}>Language ID</th>
                    <th style={{ textAlign: 'center', padding: '10px 12px' }}>Intent Acc</th>
                    <th style={{ textAlign: 'center', padding: '10px 12px' }}>NER Recall</th>
                    <th style={{ textAlign: 'center', padding: '10px 12px' }}>NER F1</th>
                    <th style={{ textAlign: 'center', padding: '10px 12px' }}>Code-Switch Acc</th>
                  </tr>
                </thead>
                <tbody>
                  {metrics.map((m, idx) => (
                    <tr key={idx} style={{ borderBottom: '1px solid #1e293b' }}>
                      <td style={{ padding: '12px', fontWeight: 600, color: '#f8fafc' }}>
                        {m.language}
                        <span style={{ marginLeft: 6, fontSize: '0.74rem', color: '#64748b' }}>({m.language_code})</span>
                      </td>
                      <td style={{ textAlign: 'center', padding: '12px', color: '#94a3b8' }}>{m.total_samples}</td>
                      <td style={{ textAlign: 'center', padding: '12px', color: '#4ade80', fontWeight: 600 }}>{m.language_accuracy}%</td>
                      <td style={{ textAlign: 'center', padding: '12px', color: '#38bdf8', fontWeight: 600 }}>{m.intent_accuracy}%</td>
                      <td style={{ textAlign: 'center', padding: '12px', color: '#a78bfa' }}>{m.entity_recall}%</td>
                      <td style={{ textAlign: 'center', padding: '12px', color: '#f472b6', fontWeight: 600 }}>{m.entity_f1}%</td>
                      <td style={{ textAlign: 'center', padding: '12px', color: '#fbbf24' }}>
                        {m.code_switching_accuracy !== 'N/A' ? `${m.code_switching_accuracy}%` : 'N/A'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div style={{ marginTop: 24, padding: 16, background: 'rgba(30, 41, 59, 0.5)', borderRadius: 10, fontSize: '0.8rem', color: '#94a3b8', lineHeight: 1.5 }}>
                <div style={{ fontWeight: 600, color: '#e2e8f0', marginBottom: 4 }}>Benchmark Criteria (Section 31):</div>
                <ul style={{ paddingLeft: 18 }}>
                  <li><strong>Language Identification</strong>: Validated against Devanagari, Kannada, and Latin scripts, including Tulu vs Kannada disambiguation.</li>
                  <li><strong>Intent Accuracy</strong>: Evaluated against the 18 language-independent intents.</li>
                  <li><strong>NER</strong>: Named Entity Recognition across medical terms, diseases, medicines, locations, and proper nouns.</li>
                  <li><strong>Code-Switching</strong>: Evaluated on mixed sentences (e.g. <em>"Doctor naale appointment idiya?"</em>).</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
