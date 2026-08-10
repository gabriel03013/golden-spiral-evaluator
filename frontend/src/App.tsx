import { useState } from 'react';
import { Header } from './components/Header';
import { UploadZone } from './components/UploadZone';
import { HarmonyScoreGauge } from './components/HarmonyScoreGauge';
import { GoldenRatioCards } from './components/GoldenRatioCards';
import { ColorPaletteViewer } from './components/ColorPaletteViewer';
import { ImageViewer } from './components/ImageViewer';
import { ReportViewer } from './components/ReportViewer';
import { analyzeImageFile } from './services/api';
import type { AnalysisResponse } from './types/analysis';
import { AlertCircle, RefreshCw } from 'lucide-react';

export function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [originalImageSrc, setOriginalImageSrc] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = async (file: File) => {
    setSelectedFile(file);
    setError(null);

    const objectUrl = URL.createObjectURL(file);
    setOriginalImageSrc(objectUrl);

    setIsLoading(true);
    try {
      const data = await analyzeImageFile(file);
      setAnalysis(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Ocorreu um erro inesperado ao analisar a imagem.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setOriginalImageSrc(null);
    setAnalysis(null);
    setError(null);
  };

  return (
    <div className="app-container">
      <Header />

      <main>
        <section style={{ marginBottom: '1.5rem' }}>
          <UploadZone
            onFileSelect={handleFileSelect}
            isLoading={isLoading}
            selectedFile={selectedFile}
          />
        </section>

        {error && (
          <div
            className="panel"
            style={{
              borderColor: '#7f1d1d',
              background: '#181010',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '1.5rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#fca5a5' }}>
              <AlertCircle size={20} color="#ef4444" />
              <div>
                <h4 style={{ color: '#ef4444', fontSize: '0.9rem' }}>Falha na Análise</h4>
                <p style={{ fontSize: '0.85rem' }}>{error}</p>
              </div>
            </div>

            <button className="btn-primary" onClick={handleReset}>
              <RefreshCw size={14} />
              Tentar novamente
            </button>
          </div>
        )}

        {analysis && !isLoading && (
          <div className="grid">
            <div className="col-4">
              <HarmonyScoreGauge harmonia={analysis.harmonia} />
            </div>

            <div className="col-8">
              <GoldenRatioCards metrics={analysis.segmento_aureo} />
            </div>

            <div className="col-5">
              <ColorPaletteViewer cores={analysis.cores} />
            </div>

            <div className="col-7">
              <ImageViewer
                originalImageSrc={originalImageSrc}
                visualizacao={analysis.visualizacao}
              />
            </div>

            <div className="col-12">
              <ReportViewer relatorio={analysis.relatorio} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
