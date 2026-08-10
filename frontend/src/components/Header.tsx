import React from 'react';
import { Sliders } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="brand">
        <div className="brand-icon">
          <Sliders size={18} />
        </div>
        <div>
          <h1 className="brand-title">Golden Ratio Visual Analyzer</h1>
          <p className="brand-subtitle">Análise de proporção áurea e harmonia cromática</p>
        </div>
      </div>
    </header>
  );
};
