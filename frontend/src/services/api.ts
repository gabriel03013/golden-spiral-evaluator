import type { AnalysisResponse } from '../types/analysis';

export async function analyzeImageFile(file: File): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/analisar', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errorMessage = 'Erro ao processar imagem';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
      }
    } catch {
      // Use fallback error string
    }
    throw new Error(errorMessage);
  }

  const data: AnalysisResponse = await response.json();
  return data;
}
