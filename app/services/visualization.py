import cv2
import numpy as np
import math
import base64
from app.services.golden_ratio import decompose_golden_rectangle


PHI = (1 + math.sqrt(5)) / 2
GOLD_COLOR = (0, 215, 255)       # Amarelo Ouro vibrante em BGR (#FFD700)
DARK_GOLD_OUTLINE = (0, 50, 100)  # Contorno escuro para contraste em fundos claros


def draw_dashed_line(
    image,
    p1,
    p2,
    color=GOLD_COLOR,
    thickness=2,
    dash_length=10
):
    """
    Desenha uma linha tracejada antialiased entre dois pontos.
    """
    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)

    if distance == 0:
        return

    ux = dx / distance
    uy = dy / distance
    current = 0

    while current < distance:
        start = current
        end = min(current + dash_length, distance)

        sx = int(x1 + ux * start)
        sy = int(y1 + uy * start)
        ex = int(x1 + ux * end)
        ey = int(y1 + uy * end)

        cv2.line(image, (sx, sy), (ex, ey), color, thickness, cv2.LINE_AA)
        current += dash_length * 2


def draw_dashed_rectangle(
    image,
    x,
    y,
    w,
    h,
    color=GOLD_COLOR,
    thickness=2
):
    """
    Desenha um retângulo tracejado com cantos destacados.
    """
    draw_dashed_line(image, (x, y), (x + w, y), color, thickness)
    draw_dashed_line(image, (x + w, y), (x + w, y + h), color, thickness)
    draw_dashed_line(image, (x + w, y + h), (x, y + h), color, thickness)
    draw_dashed_line(image, (x, y + h), (x, y), color, thickness)


def draw_golden_grid(
    image,
    rectangle,
    color=GOLD_COLOR,
    thickness=1
):
    """
    Desenha a Grade do Segmento Áureo (Linhas de Seção Áurea em 0.382 e 0.618).
    """
    x = rectangle["x"]
    y = rectangle["y"]
    w = rectangle["width"]
    h = rectangle["height"]

    gx1 = int(x + w * 0.381966)
    gx2 = int(x + w * 0.618034)
    gy1 = int(y + h * 0.381966)
    gy2 = int(y + h * 0.618034)

    # Linhas verticais do segmento áureo
    draw_dashed_line(image, (gx1, y), (gx1, y + h), color, thickness, dash_length=6)
    draw_dashed_line(image, (gx2, y), (gx2, y + h), color, thickness, dash_length=6)

    # Linhas horizontais do segmento áureo
    draw_dashed_line(image, (x, gy1), (x + w, gy1), color, thickness, dash_length=6)
    draw_dashed_line(image, (x, gy2), (x + w, gy2), color, thickness, dash_length=6)

    # Marcadores dos 4 Pontos Focais Áureos (Olhos do Segmento Áureo)
    for px, py in [(gx1, gy1), (gx2, gy1), (gx1, gy2), (gx2, gy2)]:
        cv2.circle(image, (px, py), 5, (0, 0, 0), -1, cv2.LINE_AA)
        cv2.circle(image, (px, py), 4, color, -1, cv2.LINE_AA)


def draw_golden_spiral(
    image,
    squares,
    color=GOLD_COLOR,
    thickness=4
):
    """
    Desenha a espiral áurea contínua perfeita através dos arcos de cada quadrado decomposto.
    """
    for sq in squares:
        cx, cy = int(sq["arc_center"][0]), int(sq["arc_center"][1])
        r = int(sq["size"])
        a_start, a_end = sq["angles"]

        if r <= 1:
            continue

        # Linha de fundo escura para máximo contraste em fundos claros
        cv2.ellipse(
            image,
            (cx, cy),
            (r, r),
            0,
            a_start,
            a_end,
            DARK_GOLD_OUTLINE,
            thickness + 2,
            cv2.LINE_AA
        )

        # Curva da espiral em ouro vibrante
        cv2.ellipse(
            image,
            (cx, cy),
            (r, r),
            0,
            a_start,
            a_end,
            color,
            thickness,
            cv2.LINE_AA
        )

    # Olho da Espiral (último centro)
    if squares:
        last_sq = squares[-1]
        eye_x = int(last_sq["x"] + last_sq["size"] / 2.0)
        eye_y = int(last_sq["y"] + last_sq["size"] / 2.0)

        cv2.circle(image, (eye_x, eye_y), 7, DARK_GOLD_OUTLINE, -1, cv2.LINE_AA)
        cv2.circle(image, (eye_x, eye_y), 5, color, -1, cv2.LINE_AA)
        cv2.circle(image, (eye_x, eye_y), 2, (255, 255, 255), -1, cv2.LINE_AA)


def create_harmony_visualization(
    image,
    golden_analysis
):
    """
    Cria a visualização final completa da análise áurea com suporte às 4 orientações,
    Segmento Áureo, Retângulo e Espiral Áurea.
    """
    result = image.copy()
    height, width = result.shape[:2]

    rectangles = golden_analysis.get("detected_rectangles", [])

    if rectangles:
        best_rect = rectangles[0]
        orientation = best_rect.get("orientation", 0)
    else:
        orientation = golden_analysis.get("orientation", 0)
        # Fallback para o retângulo com melhor proporção na imagem
        crop_w = width
        crop_h = width / PHI
        if crop_h > height:
            crop_h = height
            crop_w = height * PHI
        best_rect = {
            "x": int((width - crop_w) / 2),
            "y": int((height - crop_h) / 2),
            "width": int(crop_w),
            "height": int(crop_h)
        }

    # 1. Desenha o Retângulo Áureo Principal
    draw_dashed_rectangle(
        result,
        best_rect["x"],
        best_rect["y"],
        best_rect["width"],
        best_rect["height"],
        color=GOLD_COLOR,
        thickness=2
    )

    # 2. Desenha a Grade do Segmento Áureo (Linhas 0.382 e 0.618)
    draw_golden_grid(
        result,
        best_rect,
        color=GOLD_COLOR,
        thickness=1
    )

    # 3. Decomposição em Quadrados Áureos conforme a orientação detectada
    squares = decompose_golden_rectangle(best_rect, orientation=orientation, steps=8)

    for sq in squares:
        draw_dashed_rectangle(
            result,
            int(sq["x"]),
            int(sq["y"]),
            int(sq["size"]),
            int(sq["size"]),
            color=GOLD_COLOR,
            thickness=1
        )

    # 4. Desenha a Espiral Áurea Logarítmica
    draw_golden_spiral(
        result,
        squares,
        color=GOLD_COLOR,
        thickness=4
    )

    return result


def image_to_base64(image):
    """
    Converte a imagem OpenCV para Base64 em formato JPG.
    """
    success, buffer = cv2.imencode(
        ".jpg",
        image,
        [cv2.IMWRITE_JPEG_QUALITY, 92]
    )

    if not success:
        raise ValueError("Não foi possível gerar a visualização.")

    return base64.b64encode(buffer).decode("utf-8")