import cv2
import numpy as np

IMAGE_PATH = "data/output/joia_teste_catalogo.png"
OUTPUT_PATH = "data/output/joia_teste_catalogo_shadow.png"

SHADOW_OFFSET_X = 0
SHADOW_OFFSET_Y = 25

SHADOW_BLUR = 35
SHADOW_OPACITY = 0.25

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise FileNotFoundError("Imagem de catálogo não encontrada.")

# Criar máscara da joia a partir da imagem.
# Como o fundo é branco, detectamos os pixels que não são brancos.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, mask = cv2.threshold(
    gray,
    245,
    255,
    cv2.THRESH_BINARY_INV
)

# Deslocar a máscara
translation_matrix = np.float32([
    [1, 0, SHADOW_OFFSET_X],
    [0, 1, SHADOW_OFFSET_Y]
])

shadow_mask = cv2.warpAffine(
    mask,
    translation_matrix,
    (image.shape[1], image.shape[0])
)

# Aplicar blur
shadow_mask = cv2.GaussianBlur(
    shadow_mask,
    (0, 0),
    SHADOW_BLUR
)

# Normalizar opacidade
shadow_alpha = (
    shadow_mask.astype(np.float32) / 255.0
) * SHADOW_OPACITY

# Criar camada preta
shadow = np.zeros_like(image)

# Composição
result = image.astype(np.float32)

for channel in range(3):

    result[:, :, channel] = (
        shadow[:, :, channel] * shadow_alpha
        + result[:, :, channel] * (1 - shadow_alpha)
    )

result = np.clip(result, 0, 255).astype(np.uint8)

cv2.imwrite(OUTPUT_PATH, result)

print("Sombra criada!")
print(f"Offset X: {SHADOW_OFFSET_X}")
print(f"Offset Y: {SHADOW_OFFSET_Y}")
print(f"Blur: {SHADOW_BLUR}")
print(f"Opacity: {SHADOW_OPACITY}")
print(f"Salvo em: {OUTPUT_PATH}")