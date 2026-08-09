from app.utils.image import prepare_image

from app.services.golden_ratio import (
    analyze_golden_ratio
)

from app.services.color_harmony import (
    calculate_color_harmony
)

from app.services.visualization import (
    create_harmony_visualization,
    image_to_base64
)


def analyze_image(
    image_bytes: bytes,
    content_type: str,
):

    image = prepare_image(
        image_bytes,
        content_type
    )

    golden = analyze_golden_ratio(
        image
    )

    colors = calculate_color_harmony(
        image
    )

    visualization = create_harmony_visualization(
        image,
        golden
    )

    visualization_base64 = image_to_base64(
        visualization
    )

    harmony_score = (
        golden["score"] * 0.90
        +
        colors["score"] * 0.10
    )

    if harmony_score >= 90:
        classification = "Harmonia excepcional"

    elif harmony_score >= 75:
        classification = "Alta harmonia"

    elif harmony_score >= 60:
        classification = "Harmonia moderada"

    elif harmony_score >= 40:
        classification = "Baixa harmonia"

    else:
        classification = "Baixa aderência ao segmento áureo"

    return {
        "harmony_score": round(
            harmony_score,
            2
        ),

        "classification": classification,

        "golden_ratio": golden,

        "colors": colors,

        "visualization": {
            "format": "jpg",
            "base64": visualization_base64
        }
    }