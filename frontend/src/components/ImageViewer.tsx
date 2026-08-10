import React, { useState } from 'react';
import { Eye } from 'lucide-react';
import type { VisualizationData } from '../types/analysis';

interface ImageViewerProps {
  originalImageSrc: string | null;
  visualizacao: VisualizationData;
}

export const ImageViewer: React.FC<ImageViewerProps> = ({ originalImageSrc, visualizacao }) => {
  const [activeTab, setActiveTab] = useState<'overlay' | 'original'>('overlay');

  const overlayBase64Src = visualizacao.base64.startsWith('data:')
    ? visualizacao.base64
    : `data:image/${visualizacao.format || 'jpeg'};base64,${visualizacao.base64}`;

  return (
    <div className="panel">
      <div className="panel-header">
        <span className="panel-title">
          <Eye className="panel-title-icon" size={16} />
          Inspeção Visual
        </span>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'overlay' ? 'active' : ''}`}
            onClick={() => setActiveTab('overlay')}
          >
            Overlay Áureo
          </button>
          {originalImageSrc && (
            <button
              className={`tab ${activeTab === 'original' ? 'active' : ''}`}
              onClick={() => setActiveTab('original')}
            >
              Original
            </button>
          )}
        </div>
      </div>

      <div className="img-container">
        {activeTab === 'overlay' ? (
          <img src={overlayBase64Src} alt="Análise de Proporção Áurea" />
        ) : (
          originalImageSrc && <img src={originalImageSrc} alt="Imagem Original" />
        )}
      </div>
    </div>
  );
};
