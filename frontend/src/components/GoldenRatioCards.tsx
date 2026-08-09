import React from 'react';
import { Grid } from 'lucide-react';
import type { GoldenRatioMetrics } from '../types/analysis';

interface GoldenRatioCardsProps {
  metrics: GoldenRatioMetrics;
}

export const GoldenRatioCards: React.FC<GoldenRatioCardsProps> = ({ metrics }) => {
  return (
    <div className="panel">
      <div className="panel-header">
        <span className="panel-title">
          <Grid className="panel-title-icon" size={16} />
          Métricas de Proporção Áurea
        </span>
        <span className="badge-outline">Peso 90%</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.75rem' }}>
        <div className="metric-row">
          <span className="metric-name">Score Áureo</span>
          <span className="metric-val">{metrics.score.toFixed(1)}</span>
        </div>

        <div className="metric-row">
          <span className="metric-name">Aspect Ratio</span>
          <span className="metric-val">{metrics.aspect_ratio.toFixed(4)}</span>
        </div>

        <div className="metric-row">
          <span className="metric-name">Erro Relativo</span>
          <span className="metric-val">{(metrics.golden_ratio_error * 100).toFixed(2)}%</span>
        </div>

        <div className="metric-row">
          <span className="metric-name">Retângulos</span>
          <span className="metric-val">{metrics.rectangle_score.toFixed(1)} ({metrics.detected_rectangles.length})</span>
        </div>

        <div className="metric-row">
          <span className="metric-name">Pontos Focais</span>
          <span className="metric-val">{metrics.focal_point_score.toFixed(1)}</span>
        </div>

        <div className="metric-row">
          <span className="metric-name">Espiral Áurea</span>
          <span className="metric-val">{metrics.spiral_score.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );
};
