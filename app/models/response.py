from pydantic import BaseModel
from typing import List, Dict, Any


class GoldenRatioResult(BaseModel):
    score: float
    aspect_ratio: float
    golden_ratio_error: float
    rectangle_score: float
    focal_point_score: float
    spiral_score: float
    detected_rectangles: List[Dict[str, Any]]


class ColorHarmonyResult(BaseModel):
    score: float
    dominant_colors: List[str]
    color_contrast: float
    saturation_score: float
    harmony_type: str


class AnalysisResponse(BaseModel):
    harmony_score: float
    classification: str
    golden_ratio: GoldenRatioResult
    colors: ColorHarmonyResult
    report: str