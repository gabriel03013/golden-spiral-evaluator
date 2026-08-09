# app/utils/image.py

import cv2
import numpy as np


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/jpg",
}


def decode_image(image_bytes: bytes) -> np.ndarray:
    """
    Converte os bytes recebidos pela API em uma imagem OpenCV.

    Retorna:
        np.ndarray: imagem em formato BGR.

    Raises:
        ValueError: caso os bytes não representem uma imagem válida.
    """

    if not image_bytes:
        raise ValueError("A imagem recebida está vazia.")

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        raise ValueError(
            "Não foi possível interpretar o arquivo como imagem."
        )

    return image


def validate_image_type(content_type: str | None) -> None:
    """
    Valida o MIME type enviado pelo cliente.
    """

    if not content_type:
        raise ValueError(
            "O tipo da imagem não foi informado."
        )

    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(
            "Formato de imagem não suportado. "
            "Utilize JPEG, PNG ou WEBP."
        )


def validate_image_size(
    image: np.ndarray,
    max_width: int = 6000,
    max_height: int = 6000,
) -> None:
    """
    Impede imagens com dimensões excessivamente grandes.
    """

    height, width = image.shape[:2]

    if width > max_width or height > max_height:
        raise ValueError(
            f"Imagem muito grande. "
            f"Dimensão máxima: {max_width}x{max_height}px."
        )

    if width < 100 or height < 100:
        raise ValueError(
            "Imagem muito pequena para uma análise confiável."
        )


def prepare_image(
    image_bytes: bytes,
    content_type: str | None = None,
) -> np.ndarray:
    """
    Pipeline completo de preparação da imagem.
    """

    validate_image_type(content_type)

    image = decode_image(
        image_bytes
    )

    validate_image_size(
        image
    )

    return image