import React from 'react';
import { Globe } from 'lucide-react';

interface LanguageSelectorProps {
  selectedLanguage: string;
  onChange: (lang: string) => void;
}

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({ selectedLanguage, onChange }) => {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
      <Globe size={16} color="#94a3b8" />
      <select
        value={selectedLanguage}
        onChange={(e) => onChange(e.target.value)}
        style={{
          background: '#1e293b',
          color: '#f1f5f9',
          border: '1px solid #334155',
          borderRadius: '8px',
          padding: '6px 10px',
          fontSize: '0.85rem',
          outline: 'none',
          cursor: 'pointer',
        }}
      >
        <option value="">Auto-Detect Language</option>
        <option value="sa">Sanskrit (संस्कृतम्)</option>
        <option value="en">English</option>
        <option value="tcy">Tulu (ತುಳು)</option>
      </select>
    </div>
  );
};
