import React, { useState } from 'react';
import { Palette } from 'lucide-react';
import type { ColorMetrics } from '../types/analysis';

interface ColorPaletteViewerProps {
  cores: ColorMetrics;
}

export const ColorPaletteViewer: React.FC<ColorPaletteViewerProps> = ({ cores }) => {
  const [copiedHex, setCopiedHex] = useState<string | null>(null);

  const handleCopyHex = (hex: string) => {
    navigator.clipboard.writeText(hex);
    setCopiedHex(hex);
    setTimeout(() => setCopiedHex(null), 1200);
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <span className="panel-title">
          <Palette className="panel-title-icon" size={16} />
          Análise Cromática
        </span>
        <span className="badge-outline">{cores.harmony_type}</span>
      </div>

      <div>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
          Cores Dominantes
        </span>
        <div className="swatch-grid">
          {cores.dominant_colors.map((hex, index) => (
            <div
              key={index}
              className="swatch-card"
              onClick={() => handleCopyHex(hex)}
              title="Clique para copiar"
            >
              <div className="swatch-box" style={{ backgroundColor: hex }} />
              <span className="swatch-code">
                {copiedHex === hex ? 'Copiado!' : hex}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div style={{ marginTop: '1rem', paddingTop: '0.75rem', borderTop: '1px solid var(--border-subtle)' }}>
        <div className="metric-row">
          <span className="metric-name">Score Cromático</span>
          <span className="metric-val">{cores.score.toFixed(1)} / 100</span>
        </div>
        <div className="metric-row">
          <span className="metric-name">Contraste de Cor</span>
          <span className="metric-val">{cores.color_contrast.toFixed(1)}</span>
        </div>
        <div className="metric-row">
          <span className="metric-name">Saturação Média</span>
          <span className="metric-val">{cores.saturation_score.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );
};
