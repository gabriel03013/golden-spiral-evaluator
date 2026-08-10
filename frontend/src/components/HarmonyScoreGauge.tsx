import React from 'react';
import { Activity } from 'lucide-react';
import type { HarmonyScore } from '../types/analysis';

interface HarmonyScoreGaugeProps {
  harmonia: HarmonyScore;
}

export const HarmonyScoreGauge: React.FC<HarmonyScoreGaugeProps> = ({ harmonia }) => {
  const score = Math.min(100, Math.max(0, harmonia.score));

  return (
    <div className="panel" style={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div className="panel-header">
        <span className="panel-title">
          <Activity className="panel-title-icon" size={16} />
          Score de Harmonia
        </span>
        <span className="badge-outline">Geral</span>
      </div>

      <div style={{ margin: '1rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem' }}>
          <span className="score-number">{score.toFixed(1)}</span>
          <span style={{ fontSize: '1rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>/ 100</span>
        </div>

        <div className="score-progress-bar">
          <div
            className="score-progress-fill"
            style={{ width: `${score}%` }}
          />
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '0.75rem', borderTop: '1px solid var(--border-subtle)' }}>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Classificação</span>
        <span style={{ fontSize: '0.85rem', fontWeight: 500, color: 'var(--text)' }}>
          {harmonia.classificacao}
        </span>
      </div>
    </div>
  );
};
