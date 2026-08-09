from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from app.services.image_analyzer import (
    analyze_image
)

from app.services.report_generator import (
    create_report
)


app = FastAPI(
    title="Golden Harmony Analyzer",
    description=(
        "Analisador de harmonia visual baseado "
        "em proporção áurea e harmonia cromática."
    ),
    version="1.0.0"
)


@app.post("/analisar")
async def analisar(
    file: UploadFile = File(...)
):

    if not file.content_type:

        raise HTTPException(
            status_code=400,
            detail="Tipo de arquivo inválido."
        )

    if not file.content_type.startswith(
        "image/"
    ):

        raise HTTPException(
            status_code=400,
            detail="O arquivo precisa ser uma imagem."
        )

    try:

        image_bytes = await file.read()

        analysis = analyze_image(
            image_bytes,
            file.content_type
        )


        report_data = {
            "harmony_score": analysis["harmony_score"],
            "classification": analysis["classification"],

            "golden_ratio": {
                "score": analysis["golden_ratio"]["score"],
                "aspect_ratio": analysis["golden_ratio"]["aspect_ratio"],
                "golden_ratio_error": analysis["golden_ratio"]["golden_ratio_error"],
                "rectangle_score": analysis["golden_ratio"]["rectangle_score"],
                "focal_point_score": analysis["golden_ratio"]["focal_point_score"],
                "spiral_score": analysis["golden_ratio"]["spiral_score"],
                "number_of_rectangles": len(
                    analysis["golden_ratio"]["detected_rectangles"]
                )
            },

    "colors": analysis["colors"]
}
        
        report = create_report(
            report_data,
        )

        return {
            "arquivo": file.filename,

            "harmonia": {
                "score": analysis["harmony_score"],
                "classificacao": analysis["classification"]
            },

            "segmento_aureo": analysis["golden_ratio"],

            "cores": analysis["colors"],

            "visualizacao": analysis["visualization"],

            "relatorio": report
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Erro durante análise: {error}"
        )