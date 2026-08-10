import React, { useRef, useState } from 'react';
import { Upload, Image as ImageIcon } from 'lucide-react';

interface UploadZoneProps {
  onFileSelect: (file: File) => void;
  isLoading: boolean;
  selectedFile: File | null;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onFileSelect, isLoading, selectedFile }) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        onFileSelect(file);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      onFileSelect(file);
    }
  };

  return (
    <div
      className="upload-box"
      style={{
        borderColor: isDragging ? '#a1a1aa' : '#3f3f46',
        backgroundColor: isDragging ? '#1f1f23' : undefined,
      }}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current?.click()}
    >
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*"
        style={{ display: 'none' }}
      />

      {isLoading ? (
        <div style={{ padding: '1rem 0' }}>
          <div className="spinner-small" style={{ marginBottom: '0.75rem' }} />
          <p style={{ fontSize: '0.9rem', color: 'var(--text)', fontWeight: 500 }}>
            Processando visão computacional e gerando parecer...
          </p>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
            Calculando matrizes de proporção áurea, histogramas e modelo Groq.
          </p>
        </div>
      ) : selectedFile ? (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem' }}>
          <ImageIcon size={24} color="var(--text-muted)" />
          <div style={{ textAlign: 'left' }}>
            <p style={{ fontSize: '0.9rem', fontWeight: 500, color: 'var(--text)' }}>
              {selectedFile.name}
            </p>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • Clique ou arraste para substituir
            </p>
          </div>
          <button className="btn-primary" type="button" style={{ marginLeft: '1rem' }}>
            Trocar arquivo
          </button>
        </div>
      ) : (
        <div>
          <Upload size={24} color="var(--text-muted)" style={{ marginBottom: '0.5rem' }} />
          <p style={{ fontSize: '0.9rem', fontWeight: 500, color: 'var(--text)', marginBottom: '0.25rem' }}>
            Selecione uma imagem para analisar
          </p>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
            Arraste um arquivo JPG, PNG ou WEBP até aqui
          </p>
          <button className="btn-primary" type="button">
            Escolher arquivo
          </button>
        </div>
      )}
    </div>
  );
};
