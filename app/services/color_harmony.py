import cv2
import numpy as np

from sklearn.cluster import KMeans
from colorsys import rgb_to_hsv


def rgb_to_hex(rgb):

    return "#{:02X}{:02X}{:02X}".format(
        int(rgb[0]),
        int(rgb[1]),
        int(rgb[2])
    )


def calculate_color_harmony(image):

    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    pixels = rgb.reshape(
        -1,
        3
    )

    # Reduz quantidade de pixels
    # para acelerar o KMeans
    if len(pixels) > 10000:

        indices = np.random.choice(
            len(pixels),
            10000,
            replace=False
        )

        pixels = pixels[indices]

    kmeans = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    kmeans.fit(pixels)

    centers = kmeans.cluster_centers_

    labels = kmeans.labels_

    counts = np.bincount(labels)

    order = np.argsort(
        counts
    )[::-1]

    centers = centers[order]

    dominant_colors = [
        rgb_to_hex(color)
        for color in centers
    ]

    hsv_colors = [
        rgb_to_hsv(
            color[0] / 255,
            color[1] / 255,
            color[2] / 255
        )
        for color in centers
    ]

    saturations = [
        hsv[1]
        for hsv in hsv_colors
    ]

    saturation = np.mean(
        saturations
    )

    saturation_score = min(
        saturation * 100,
        100
    )

    # Mede diversidade cromática
    hues = [
        hsv[0]
        for hsv in hsv_colors
    ]

    hue_differences = []

    for i in range(len(hues)):

        for j in range(i + 1, len(hues)):

            difference = abs(
                hues[i] - hues[j]
            )

            difference = min(
                difference,
                1 - difference
            )

            hue_differences.append(
                difference
            )

    if hue_differences:

        average_difference = np.mean(
            hue_differences
        )

    else:

        average_difference = 0

    # Heurística de harmonia cromática
    color_contrast = (
        average_difference * 100
    )

    if color_contrast < 20:

        harmony_type = "Monocromática"

        harmony_score = 80

    elif color_contrast < 40:

        harmony_type = "Análoga"

        harmony_score = 90

    elif color_contrast < 65:

        harmony_type = "Complementar ou complementar dividida"

        harmony_score = 95

    else:

        harmony_type = "Alto contraste cromático"

        harmony_score = 70

    final_score = (
        harmony_score * 0.6
        +
        saturation_score * 0.2
        +
        color_contrast * 0.2
    )

    return {
        "score": round(
            min(final_score, 100),
            2
        ),
        "dominant_colors": dominant_colors,
        "color_contrast": round(
            float(color_contrast),
            2
        ),
        "saturation_score": round(
            float(saturation_score),
            2
        ),
        "harmony_type": harmony_type
    }