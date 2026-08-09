import cv2
import numpy as np
import math
import base64


PHI = (1 + math.sqrt(5)) / 2


def draw_dashed_line(
    image,
    p1,
    p2,
    color,
    thickness=2,
    dash_length=10
):
    """
    Desenha uma linha tracejada entre dois pontos.
    """

    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1

    distance = math.sqrt(
        dx ** 2 + dy ** 2
    )

    if distance == 0:
        return

    ux = dx / distance
    uy = dy / distance

    current = 0

    while current < distance:

        start = current
        end = min(
            current + dash_length,
            distance
        )

        sx = int(x1 + ux * start)
        sy = int(y1 + uy * start)

        ex = int(x1 + ux * end)
        ey = int(y1 + uy * end)

        cv2.line(
            image,
            (sx, sy),
            (ex, ey),
            color,
            thickness,
            cv2.LINE_AA
        )

        current += dash_length * 2


def draw_dashed_rectangle(
    image,
    x,
    y,
    w,
    h,
    color=(0, 215, 255),
    thickness=2
):
    """
    Desenha um retângulo tracejado.
    """

    draw_dashed_line(
        image,
        (x, y),
        (x + w, y),
        color,
        thickness
    )

    draw_dashed_line(
        image,
        (x + w, y),
        (x + w, y + h),
        color,
        thickness
    )

    draw_dashed_line(
        image,
        (x + w, y + h),
        (x, y + h),
        color,
        thickness
    )

    draw_dashed_line(
        image,
        (x, y + h),
        (x, y),
        color,
        thickness
    )


def find_best_rectangle(
    image,
    rectangles
):
    """
    Escolhe o retângulo mais relevante.

    Ignora objetos muito pequenos para evitar
    que pequenos detalhes da imagem sejam
    interpretados como a composição principal.
    """

    height, width = image.shape[:2]

    image_area = width * height

    valid = []

    for rectangle in rectangles:

        w = rectangle.get(
            "width",
            0
        )

        h = rectangle.get(
            "height",
            0
        )

        score = rectangle.get(
            "score",
            0
        )

        area = w * h

        # Ignora objetos que ocupam menos de 5%
        # da imagem.
        if area < image_area * 0.05:
            continue

        valid.append(
            rectangle
        )

    if not valid:
        return None

    # Combina tamanho e score.
    return max(
        valid,
        key=lambda r: (
            r.get("score", 0) *
            math.sqrt(
                (
                    r["width"] *
                    r["height"]
                ) / image_area
            )
        )
    )


def fit_golden_rectangle(
    image,
    rectangle
):
    """
    Cria um retângulo áureo dentro do
    retângulo detectado.

    Isso garante que a visualização
    tenha proporção φ mesmo quando o
    retângulo detectado não for perfeito.
    """

    image_height, image_width = image.shape[:2]

    if rectangle is None:

        # Fallback:
        # utiliza uma grande área central
        # da imagem.

        margin_x = image_width * 0.10
        margin_y = image_height * 0.10

        available_width = (
            image_width
            - 2 * margin_x
        )

        available_height = (
            image_height
            - 2 * margin_y
        )

        if available_width >= available_height:

            h = available_height
            w = h * PHI

        else:

            w = available_width
            h = w * PHI

        if w > available_width:

            w = available_width
            h = w / PHI

        if h > available_height:

            h = available_height
            w = h / PHI

        x = (
            image_width - w
        ) / 2

        y = (
            image_height - h
        ) / 2

        return {
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h)
        }

    x = rectangle["x"]
    y = rectangle["y"]

    w = rectangle["width"]
    h = rectangle["height"]

    # Se o candidato é horizontal
    if w >= h:

        golden_height = h
        golden_width = h * PHI

        # Caso não caiba
        if golden_width > w:

            golden_width = w
            golden_height = w / PHI

    else:

        golden_width = w
        golden_height = w * PHI

        # Caso não caiba
        if golden_height > h:

            golden_height = h
            golden_width = h / PHI

    # Centraliza o retângulo áureo
    # dentro do retângulo detectado.

    new_x = (
        x
        +
        (w - golden_width) / 2
    )

    new_y = (
        y
        +
        (h - golden_height) / 2
    )

    return {
        "x": int(new_x),
        "y": int(new_y),
        "width": int(golden_width),
        "height": int(golden_height)
    }


def draw_golden_decomposition(
    image,
    rectangle,
    color=(0, 215, 255),
    thickness=2
):
    """
    Divide o retângulo áureo em quadrados
    sucessivos.
    """

    x = float(rectangle["x"])
    y = float(rectangle["y"])

    w = float(rectangle["width"])
    h = float(rectangle["height"])

    squares = []

    # Começamos removendo quadrados
    # alternadamente dos lados.

    for _ in range(8):

        if w <= 2 or h <= 2:
            break

        if w >= h:

            size = h

            square = {
                "x": x,
                "y": y,
                "size": size,
                "side": "left"
            }

            squares.append(square)

            x += size
            w -= size

        else:

            size = w

            square = {
                "x": x,
                "y": y,
                "size": size,
                "side": "top"
            }

            squares.append(square)

            y += size
            h -= size

    # Agora desenhamos os quadrados.

    for square in squares:

        sx = int(square["x"])
        sy = int(square["y"])
        size = int(square["size"])

        draw_dashed_rectangle(
            image,
            sx,
            sy,
            size,
            size,
            color,
            thickness
        )

    return squares


def draw_golden_spiral(
    image,
    rectangle,
    color=(0, 215, 255),
    thickness=5
):
    """
    Desenha uma espiral áurea baseada na
    decomposição do retângulo em quadrados.
    """

    x = float(rectangle["x"])
    y = float(rectangle["y"])

    w = float(rectangle["width"])
    h = float(rectangle["height"])

    # Determina por qual lado começamos.

    if w >= h:

        side = "left"

    else:

        side = "top"

    for _ in range(10):

        if w <= 3 or h <= 3:
            break

        if side == "left":

            size = h

            # Centro no canto inferior direito
            # do quadrado.

            center_x = x + size
            center_y = y + size

            cv2.ellipse(
                image,
                (
                    int(center_x),
                    int(center_y)
                ),
                (
                    int(size),
                    int(size)
                ),
                0,
                180,
                270,
                color,
                thickness,
                cv2.LINE_AA
            )

            x += size
            w -= size

            side = "top"

        elif side == "top":

            size = w

            # Centro no canto inferior esquerdo.

            center_x = x
            center_y = y + size

            cv2.ellipse(
                image,
                (
                    int(center_x),
                    int(center_y)
                ),
                (
                    int(size),
                    int(size)
                ),
                0,
                270,
                360,
                color,
                thickness,
                cv2.LINE_AA
            )

            y += size
            h -= size

            side = "right"

        elif side == "right":

            size = h

            # Centro no canto superior esquerdo.

            center_x = x
            center_y = y

            cv2.ellipse(
                image,
                (
                    int(center_x),
                    int(center_y)
                ),
                (
                    int(size),
                    int(size)
                ),
                0,
                0,
                90,
                color,
                thickness,
                cv2.LINE_AA
            )

            x += 0
            w -= size

            side = "bottom"

        elif side == "bottom":

            size = w

            # Centro no canto superior direito.

            center_x = x + size
            center_y = y

            cv2.ellipse(
                image,
                (
                    int(center_x),
                    int(center_y)
                ),
                (
                    int(size),
                    int(size)
                ),
                0,
                90,
                180,
                color,
                thickness,
                cv2.LINE_AA
            )

            y += 0
            h -= size

            side = "left"

    return image


def create_harmony_visualization(
    image,
    golden_analysis
):
    """
    Cria a visualização final da análise áurea.

    Mostra:

    - retângulo áureo;
    - decomposição em quadrados;
    - espiral áurea.

    Não mostra scores, números ou pontos.
    """

    result = image.copy()

    rectangles = golden_analysis.get(
        "detected_rectangles",
        []
    )

    best_rectangle = find_best_rectangle(
        result,
        rectangles
    )

    golden_rectangle = fit_golden_rectangle(
        result,
        best_rectangle
    )

    # --------------------------------------------------
    # 1. Retângulo principal
    # --------------------------------------------------

    draw_dashed_rectangle(
        result,
        golden_rectangle["x"],
        golden_rectangle["y"],
        golden_rectangle["width"],
        golden_rectangle["height"],
        color=(0, 215, 255),
        thickness=2
    )

    # --------------------------------------------------
    # 2. Decomposição
    # --------------------------------------------------

    draw_golden_decomposition(
        result,
        golden_rectangle,
        color=(0, 215, 255),
        thickness=2
    )

    # --------------------------------------------------
    # 3. Espiral
    # --------------------------------------------------

    draw_golden_spiral(
        result,
        golden_rectangle,
        color=(0, 215, 255),
        thickness=5
    )

    return result


def image_to_base64(
    image
):
    """
    Converte a imagem OpenCV para Base64.
    """

    success, buffer = cv2.imencode(
        ".jpg",
        image,
        [
            cv2.IMWRITE_JPEG_QUALITY,
            90
        ]
    )

    if not success:

        raise ValueError(
            "Não foi possível gerar a visualização."
        )

    return base64.b64encode(
        buffer
    ).decode("utf-8")