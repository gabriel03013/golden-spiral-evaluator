import cv2
import numpy as np
import math


PHI = (1 + math.sqrt(5)) / 2  # 1.618033988749895

ORIENTATION_NAMES = {
    0: "Inferior Direita",
    1: "Inferior Esquerda",
    2: "Superior Esquerda",
    3: "Superior Direita"
}


def ratio_error(value: float) -> float:
    """
    Mede o quão próximo um valor está da proporção áurea.
    Retorna 0.0 para proporção perfeita e cresce conforme se afasta.
    """
    if value <= 0:
        return 1.0

    direct = abs(value - PHI) / PHI
    inverse = abs(value - (1 / PHI)) / (1 / PHI)

    return min(direct, inverse)


def ratio_score(value: float) -> float:
    """
    Converte o erro da proporção áurea em um score de 0 a 100.
    """
    error = ratio_error(value)
    return max(0.0, min(100.0, 100.0 * (1.0 - error)))


def decompose_base_0(rect: dict, steps: int = 10) -> list:
    """
    Decomposição padrão perfeita para Orientação 0 (Inferior Direita).
    w >= h: left -> top -> right -> bottom
    h > w: top -> right -> bottom -> left
    """
    x = float(rect["x"])
    y = float(rect["y"])
    w = float(rect["width"])
    h = float(rect["height"])

    squares = []

    if w >= h:
        dirs = ["left", "top", "right", "bottom"]
    else:
        dirs = ["top", "right", "bottom", "left"]

    for step in range(steps):
        if w <= 2 or h <= 2:
            break

        d = dirs[step % 4]

        if d == "left":
            size = h
            sq_x, sq_y = x, y
            x += size
            w -= size
            arc_center = (sq_x + size, sq_y + size)
            angles = (180, 270)
        elif d == "top":
            size = w
            sq_x, sq_y = x, y
            y += size
            h -= size
            arc_center = (sq_x, sq_y + size)
            angles = (270, 360)
        elif d == "right":
            size = h
            sq_x, sq_y = x + (w - size), y
            w -= size
            arc_center = (sq_x, sq_y)
            angles = (0, 90)
        elif d == "bottom":
            size = w
            sq_x, sq_y = x, y + (h - size)
            h -= size
            arc_center = (sq_x + size, sq_y)
            angles = (90, 180)

        squares.append({
            "x": sq_x,
            "y": sq_y,
            "size": size,
            "arc_center": arc_center,
            "angles": angles
        })

    return squares


def decompose_golden_rectangle(rect: dict, orientation: int = 0, steps: int = 10) -> list:
    """
    Decompõe o retângulo áureo em quadrados e arcos sucessivos para qualquer uma das 4 orientações,
    utilizando transformações trigonométricas isométricas perfeitas.

    Orientações (posição do olho / convergência):
      0: Inferior Direita
      1: Inferior Esquerda (Flip X)
      2: Superior Esquerda (Flip X + Flip Y)
      3: Superior Direita  (Flip Y)
    """
    squares_base = decompose_base_0(rect, steps=steps)

    if orientation == 0:
        return squares_base

    rx = float(rect["x"])
    ry = float(rect["y"])
    rw = float(rect["width"])
    rh = float(rect["height"])

    flip_x = orientation in (1, 2)
    flip_y = orientation in (2, 3)

    transformed = []

    for sq in squares_base:
        sq_x = sq["x"]
        sq_y = sq["y"]
        sz = sq["size"]
        cx, cy = sq["arc_center"]
        a_start, a_end = sq["angles"]

        # Reflexão isométrica rigorosa dentro do retângulo de referência [rx, rx+rw] x [ry, ry+rh]
        new_sq_x = (2 * rx + rw - (sq_x + sz)) if flip_x else sq_x
        new_sq_y = (2 * ry + rh - (sq_y + sz)) if flip_y else sq_y

        new_cx = (2 * rx + rw - cx) if flip_x else cx
        new_cy = (2 * ry + rh - cy) if flip_y else cy

        new_a_start = a_start
        new_a_end = a_end

        if flip_x:
            new_a_start = 180 - new_a_start
            new_a_end = 180 - new_a_end

        if flip_y:
            new_a_start = -new_a_start
            new_a_end = -new_a_end

        min_a = min(new_a_start, new_a_end)
        min_a_norm = min_a % 360
        max_a_norm = min_a_norm + 90

        transformed.append({
            "x": new_sq_x,
            "y": new_sq_y,
            "size": sz,
            "arc_center": (new_cx, new_cy),
            "angles": (min_a_norm, max_a_norm)
        })

    return transformed









def sample_spiral_points(squares: list, samples_per_arc: int = 20) -> list:
    """
    Gera pontos discretos da espiral a partir da decomposição em arcos.
    """
    points = []
    for sq in squares:
        cx, cy = sq["arc_center"]
        r = sq["size"]
        a_start, a_end = sq["angles"]

        # Converte para radianos
        rad_start = math.radians(a_start)
        rad_end = math.radians(a_end)

        for i in range(samples_per_arc):
            t = rad_start + (rad_end - rad_start) * (i / max(1, samples_per_arc - 1))
            px = int(cx + r * math.cos(t))
            py = int(cy + r * math.sin(t))
            points.append((px, py))

    return points


def fit_golden_crop(box: tuple, image_shape: tuple) -> dict:
    """
    Ajusta uma bounding box (x, y, w, h) para que possua proporção áurea (PHI).
    """
    img_h, img_w = image_shape[:2]
    x, y, w, h = box

    if w <= 0 or h <= 0:
        return {"x": 0, "y": 0, "width": img_w, "height": int(img_w / PHI)}

    # Ajusta dimensão mantendo centro
    cx = x + w / 2.0
    cy = y + h / 2.0

    if w >= h:
        target_w = w
        target_h = w / PHI
        if target_h > img_h:
            target_h = img_h
            target_w = img_h * PHI
    else:
        target_h = h
        target_w = h / PHI
        if target_w > img_w:
            target_w = img_w
            target_h = img_w * PHI

    target_w = min(target_w, img_w)
    target_h = min(target_h, img_h)

    new_x = max(0, min(img_w - target_w, cx - target_w / 2.0))
    new_y = max(0, min(img_h - target_h, cy - target_h / 2.0))

    return {
        "x": int(new_x),
        "y": int(new_y),
        "width": int(target_w),
        "height": int(target_h)
    }


def detect_rectangles(image: np.ndarray) -> list:
    """
    Detecção avançada multiescala de retângulos e regiões candidatas a Proporção Áurea.
    Prioriza a enquadração composicional macro da imagem (arte/sujeito principal)
    e alinha automaticamente a espiral com a posição focal do sujeito.
    """
    height, width = image.shape[:2]
    img_area = width * height
    is_vertical_image = height > width

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Gradiente de Sobel para densidade de energia visual
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.hypot(sobelx, sobely)
    grad_mag = np.uint8(np.clip(grad_mag / (grad_mag.max() + 1e-5) * 255, 0, 255))

    candidate_boxes = []

    # 1. Enquadramento Global Centrado principal (100%)
    if is_vertical_image:
        crop_h = height
        crop_w = height / PHI
        if crop_w > width:
            crop_w = width
            crop_h = width * PHI
    else:
        crop_w = width
        crop_h = width / PHI
        if crop_h > height:
            crop_h = height
            crop_w = height * PHI

    crop_x = (width - crop_w) / 2.0
    crop_y = (height - crop_h) / 2.0
    candidate_boxes.append((int(crop_x), int(crop_y), int(crop_w), int(crop_h)))

    # 2. Crops Multiescala de Composição Macro (0.95, 0.90, 0.85)
    for scale in [0.95, 0.90, 0.85]:
        sw = int(width * scale)
        sh = int(height * scale)
        candidate_boxes.append((int((width - sw) / 2.0), int((height - sh) / 2.0), sw, sh))

    # 3. Contornos e objetos salientes relevantes (pelo menos 5% da área total)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
        bx, by, bw, bh = cv2.boundingRect(cnt if len(approx) != 4 else approx)
        if bw * bh >= img_area * 0.05:
            candidate_boxes.append((bx, by, bw, bh))

    # 4. MSER / Regiões de alto contraste salientes
    mser = cv2.MSER_create()
    regions, _ = mser.detectRegions(gray)
    for p in regions[:10]:
        bx, by, bw, bh = cv2.boundingRect(p)
        if bw * bh >= img_area * 0.08:
            candidate_boxes.append((bx, by, bw, bh))

    # Remove duplicatas próximas
    unique_candidates = []
    for box in candidate_boxes:
        golden_rect = fit_golden_crop(box, image.shape)
        if not any(
            abs(g["x"] - golden_rect["x"]) < 30 and
            abs(g["y"] - golden_rect["y"]) < 30 and
            abs(g["width"] - golden_rect["width"]) < 30 and
            abs(g["height"] - golden_rect["height"]) < 30
            for g in unique_candidates
        ):
            unique_candidates.append(golden_rect)

    # Avaliação e pontuação de cada candidato
    scored_rectangles = []

    for rect in unique_candidates:
        rx, ry, rw, rh = rect["x"], rect["y"], rect["width"], rect["height"]
        if rw < 40 or rh < 40:
            continue

        rect_area = rw * rh
        area_coverage = rect_area / float(img_area)
        is_rect_vertical = rh > rw

        ratio = max(rw, rh) / min(rw, rh)
        aspect_sc = ratio_score(ratio)

        sub_edges = edges[ry:ry+rh, rx:rx+rw]
        sub_grad = grad_mag[ry:ry+rh, rx:rx+rw]
        if sub_edges.size == 0:
            continue

        # Linhas guia do Segmento Áureo (0.382 e 0.618)
        gx1, gx2 = int(rw * 0.381966), int(rw * 0.618034)
        gy1, gy2 = int(rh * 0.381966), int(rh * 0.618034)

        grid_density = (
            np.mean(sub_grad[:, min(gx1, rw-1)]) +
            np.mean(sub_grad[:, min(gx2, rw-1)]) +
            np.mean(sub_grad[min(gy1, rh-1), :]) +
            np.mean(sub_grad[min(gy2, rh-1), :])
        ) / 4.0
        grid_sc = min(100.0, (grid_density / 255.0) * 200.0)

        # Centroide de energia dentro do retângulo
        M = cv2.moments(sub_grad)
        if M["m00"] > 0:
            cx_local = M["m10"] / M["m00"]
            cy_local = M["m01"] / M["m00"]
        else:
            cx_local, cy_local = rw / 2.0, rh / 2.0

        best_orient = 0
        best_orient_score = -1.0
        best_spiral_sc = 0.0
        best_focal_sc = 0.0
        best_grid_sc = grid_sc

        for orient in range(4):
            sqs = decompose_golden_rectangle(rect, orient)
            spiral_pts = sample_spiral_points(sqs)

            matches = 0
            total_pts = len(spiral_pts)
            for px, py in spiral_pts:
                if 0 <= px < width and 0 <= py < height:
                    if edges[py, px] > 0 or grad_mag[py, px] > 40:
                        matches += 1

            spiral_sc = min(100.0, (matches / max(1, total_pts)) * 250.0)

            last_sq = sqs[-1]
            eye_x = last_sq["x"] + last_sq["size"] / 2.0 - rx
            eye_y = last_sq["y"] + last_sq["size"] / 2.0 - ry

            dist = math.hypot(cx_local - eye_x, cy_local - eye_y)
            max_dist = math.hypot(rw, rh)
            focal_sc = max(0.0, 100.0 * (1.0 - (dist / (max_dist * 0.4))))

            orient_score = 0.40 * spiral_sc + 0.45 * focal_sc + 0.15 * grid_sc

            if orient_score > best_orient_score:
                best_orient_score = orient_score
                best_orient = orient
                best_spiral_sc = spiral_sc
                best_focal_sc = focal_sc

        # Bônus para concordância de orientação de formato (imagem vertical -> retângulo vertical)
        orientation_harmony_bonus = 1.15 if (is_vertical_image == is_rect_vertical) else 0.85

        # Fator de Cobertura de Área (Privilegia enquadramento composicional de toda a arte)
        if area_coverage < 0.10:
            area_weight = 0.45
        elif area_coverage < 0.25:
            area_weight = 0.75
        else:
            area_weight = 1.0 + (area_coverage * 0.25)

        total_score = (
            aspect_sc * 0.25 +
            best_spiral_sc * 0.35 +
            best_grid_sc * 0.20 +
            best_focal_sc * 0.20
        ) * area_weight * orientation_harmony_bonus

        rect_data = {
            "x": int(rx),
            "y": int(ry),
            "width": int(rw),
            "height": int(rh),
            "ratio": round(float(ratio), 4),
            "golden_error": round(float(ratio_error(ratio)), 4),
            "score": round(float(total_score), 2),
            "orientation": best_orient,
            "orientation_name": ORIENTATION_NAMES[best_orient],
            "spiral_score": round(float(best_spiral_sc), 2),
            "grid_score": round(float(best_grid_sc), 2),
            "focal_score": round(float(best_focal_sc), 2)
        }
        scored_rectangles.append(rect_data)

    scored_rectangles.sort(key=lambda item: item["score"], reverse=True)
    return scored_rectangles[:10]




def calculate_focal_point_score(image: np.ndarray) -> float:
    """
    Calcula a precisão dos pontos focais da imagem em relação aos 4 centros da seção áurea.
    """
    height, width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    moments = cv2.moments(threshold)

    if moments["m00"] == 0:
        return 50.0

    cx = moments["m10"] / moments["m00"]
    cy = moments["m01"] / moments["m00"]

    norm_x = cx / width
    norm_y = cy / height

    golden_points = [
        (0.381966, 0.381966),
        (0.618034, 0.381966),
        (0.381966, 0.618034),
        (0.618034, 0.618034)
    ]

    distances = [
        math.hypot(norm_x - px, norm_y - py)
        for px, py in golden_points
    ]

    min_dist = min(distances)
    score = max(0.0, 100.0 * (1.0 - min_dist / 0.6))
    return min(score, 100.0)


def analyze_golden_ratio(image: np.ndarray) -> dict:
    """
    Realiza a análise completa de Proporção Áurea, Segmento Áureo e Espiral Áurea.
    """
    height, width = image.shape[:2]
    aspect_ratio = max(width, height) / min(width, height)
    aspect_sc = ratio_score(aspect_ratio)

    rectangles = detect_rectangles(image)

    if rectangles:
        best_rect = rectangles[0]
        rect_sc = best_rect["score"]
        spiral_sc = best_rect["spiral_score"]
        focal_sc = best_rect["focal_score"]
        orient_name = best_rect["orientation_name"]
        orient_id = best_rect["orientation"]
    else:
        rect_sc = aspect_sc
        spiral_sc = 50.0
        focal_sc = calculate_focal_point_score(image)
        orient_name = "Inferior Direita"
        orient_id = 0

    final_score = (
        aspect_sc * 0.25 +
        rect_sc * 0.35 +
        focal_sc * 0.20 +
        spiral_sc * 0.20
    )

    return {
        "score": round(float(final_score), 2),
        "aspect_ratio": round(float(aspect_ratio), 4),
        "golden_ratio_error": round(float(ratio_error(aspect_ratio)), 4),
        "rectangle_score": round(float(rect_sc), 2),
        "focal_point_score": round(float(focal_sc), 2),
        "spiral_score": round(float(spiral_sc), 2),
        "orientation": orient_id,
        "orientation_name": orient_name,
        "detected_rectangles": rectangles
    }