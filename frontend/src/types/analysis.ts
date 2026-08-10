export interface DetectedRectangle {
  x: number;
  y: number;
  width: number;
  height: number;
  ratio: number;
  golden_error: number;
  score: number;
}

export interface GoldenRatioMetrics {
  score: number;
  aspect_ratio: number;
  golden_ratio_error: number;
  rectangle_score: number;
  focal_point_score: number;
  spiral_score: number;
  detected_rectangles: DetectedRectangle[];
}

export interface ColorMetrics {
  score: number;
  dominant_colors: string[];
  color_contrast: number;
  saturation_score: number;
  harmony_type: string;
}

export interface HarmonyScore {
  score: number;
  classificacao: string;
}

export interface VisualizationData {
  format?: string;
  base64: string;
}

export interface AnalysisResponse {
  arquivo: string;
  harmonia: HarmonyScore;
  segmento_aureo: GoldenRatioMetrics;
  cores: ColorMetrics;
  visualizacao: VisualizationData;
  relatorio: string;
}
