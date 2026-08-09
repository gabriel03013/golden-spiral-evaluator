import cv2
import numpy as np
import math


PHI = (1 + math.sqrt(5)) / 2


def ratio_error(value: float) -> float:
    """
    Mede o quão próximo um valor está da proporção áurea.
    Retorna 0 quando é perfeito e cresce conforme se afasta.
    """

    if value <= 0:
        return 1.0

    direct = abs(value - PHI) / PHI
    inverse = abs(value - (1 / PHI)) / (1 / PHI)

    return min(direct, inverse)


def ratio_score(value: float) -> float:
    error = ratio_error(value)

    return max(
        0.0,
        min(
            100.0,
            100.0 * (1.0 - error)
        )
    )


def detect_rectangles(image: np.ndarray):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blurred,
        50,
        150
    )

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    rectangles = []

    for contour in contours:

        perimeter = cv2.arcLength(
            contour,
            True
        )

        approximation = cv2.approxPolyDP(
            contour,
            0.02 * perimeter,
            True
        )

        if len(approximation) != 4:
            continue

        x, y, w, h = cv2.boundingRect(
            approximation
        )

        if w < 30 or h < 30:
            continue

        area = w * h

        if area < 1000:
            continue

        ratio = max(w, h) / min(w, h)

        error = ratio_error(ratio)

        score = ratio_score(ratio)

        rectangles.append(
            {
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h),
                "ratio": round(float(ratio), 4),
                "golden_error": round(float(error), 4),
                "score": round(float(score), 2)
            }
        )

    rectangles.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return rectangles[:20]


def calculate_focal_point_score(
    image: np.ndarray
) -> float:

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    _, threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    moments = cv2.moments(threshold)

    if moments["m00"] == 0:
        return 50.0

    cx = moments["m10"] / moments["m00"]
    cy = moments["m01"] / moments["m00"]

    height, width = gray.shape

    normalized_x = cx / width
    normalized_y = cy / height

    golden_points = [
        (0.382, 0.382),
        (0.618, 0.382),
        (0.382, 0.618),
        (0.618, 0.618)
    ]

    distances = []

    for px, py in golden_points:

        distance = math.sqrt(
            (normalized_x - px) ** 2 +
            (normalized_y - py) ** 2
        )

        distances.append(distance)

    minimum_distance = min(distances)

    score = max(
        0.0,
        100.0 * (
            1.0 -
            minimum_distance / 0.8
        )
    )

    return min(score, 100.0)


def calculate_spiral_score(
    image: np.ndarray
) -> float:
    """
    Aproxima a presença de uma distribuição
    compatível com a espiral áurea usando NumPy vetorizado.
    """

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    edges = cv2.Canny(
        gray,
        50,
        150
    )

    height, width = gray.shape

    cx = width / 2.0
    cy = height / 2.0

    y_indices, x_indices = np.ogrid[:height, :width]
    dx = x_indices - cx
    dy = y_indices - cy

    distance = np.hypot(dx, dy)
    angle = np.arctan2(dy, dx)

    theta = angle + math.pi * 2.0
    radius = (
        min(width, height)
        * 0.08
        * np.exp(0.306349 * theta)
    )

    golden_region = (np.abs(distance - radius) < 10).astype(np.uint8) * 255

    intersection = cv2.bitwise_and(
        edges,
        golden_region
    )

    total_edges = np.count_nonzero(edges)

    if total_edges == 0:
        return 0.0

    score = (
        np.count_nonzero(intersection)
        / total_edges
    ) * 100

    return min(
        float(score * 4),
        100.0
    )



def analyze_golden_ratio(
    image: np.ndarray
):

    height, width = image.shape[:2]

    aspect_ratio = (
        max(width, height)
        /
        min(width, height)
    )

    aspect_score = ratio_score(
        aspect_ratio
    )

    rectangles = detect_rectangles(
        image
    )

    if rectangles:

        rectangle_score = sum(
            r["score"]
            for r in rectangles
        ) / len(rectangles)

    else:

        rectangle_score = 0.0

    focal_score = calculate_focal_point_score(
        image
    )

    spiral_score = calculate_spiral_score(
        image
    )

    final_score = (
        aspect_score * 0.20
        +
        rectangle_score * 0.35
        +
        focal_score * 0.20
        +
        spiral_score * 0.25
    )

    return {
        "score": round(final_score, 2),
        "aspect_ratio": round(
            aspect_ratio,
            4
        ),
        "golden_ratio_error": round(
            ratio_error(aspect_ratio),
            4
        ),
        "rectangle_score": round(
            rectangle_score,
            2
        ),
        "focal_point_score": round(
            focal_score,
            2
        ),
        "spiral_score": round(
            spiral_score,
            2
        ),
        "detected_rectangles": rectangles
    }