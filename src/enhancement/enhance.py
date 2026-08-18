import cv2
import numpy as np


IMAGE_PATH = "data/output/joia_teste_catalogo_shadow.png"
OUTPUT_PATH = "data/output/joia_teste_enhanced.png"


def enhance_image(image):

    # -------------------------
    # 1. Exposição
    # -------------------------

    exposure = 1.05

    image = image.astype(np.float32) * exposure
    image = np.clip(image, 0, 255).astype(np.uint8)

    # -------------------------
    # 2. Contraste
    # -------------------------

    contrast = 1.08
    brightness = 0

    image = cv2.convertScaleAbs(
        image,
        alpha=contrast,
        beta=brightness
    )

    # -------------------------
    # 3. Saturação
    # -------------------------

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    saturation = 1.05

    hsv[:, :, 1] = np.clip(
        hsv[:, :, 1].astype(np.float32) * saturation,
        0,
        255
    ).astype(np.uint8)

    image = cv2.cvtColor(
        hsv,
        cv2.COLOR_HSV2BGR
    )

    # -------------------------
    # 4. Nitidez
    # -------------------------

    blurred = cv2.GaussianBlur(
        image,
        (0, 0),
        2
    )

    image = cv2.addWeighted(
        image,
        1.3,
        blurred,
        -0.3,
        0
    )

    return image


image = cv2.imread(IMAGE_PATH)

if image is None:
    raise FileNotFoundError(
        "Imagem não encontrada."
    )


result = enhance_image(image)

cv2.imwrite(
    OUTPUT_PATH,
    result
)

print("Enhancement concluído!")
print(f"Resultado: {OUTPUT_PATH}")