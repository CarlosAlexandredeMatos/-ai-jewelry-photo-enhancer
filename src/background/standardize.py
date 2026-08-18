import cv2
import numpy as np

IMAGE_PATH = "data/processed/joia_teste_rgba.png"
MASK_PATH = "data/masks/joia_teste_mask.png"
OUTPUT_PATH = "data/output/joia_teste_catalogo.png"

CANVAS_SIZE = 2000
TARGET_SIZE = 1400

image = cv2.imread(IMAGE_PATH, cv2.IMREAD_UNCHANGED)
mask = cv2.imread(MASK_PATH, cv2.IMREAD_GRAYSCALE)

if image is None:
    raise FileNotFoundError("Imagem RGBA não encontrada.")

if mask is None:
    raise FileNotFoundError("Máscara não encontrada.")

# Encontrar a região da joia
ys, xs = np.where(mask > 0)

if len(xs) == 0:
    raise ValueError("A máscara está vazia.")

# Bounding box
x_min = xs.min()
x_max = xs.max()
y_min = ys.min()
y_max = ys.max()

# Recortar imagem e máscara
cropped = image[y_min:y_max + 1, x_min:x_max + 1]
cropped_mask = mask[y_min:y_max + 1, x_min:x_max + 1]

height, width = cropped.shape[:2]

# Escala mantendo proporção
scale = TARGET_SIZE / max(width, height)

new_width = int(width * scale)
new_height = int(height * scale)

resized = cv2.resize(
    cropped,
    (new_width, new_height),
    interpolation=cv2.INTER_AREA
)

resized_mask = cv2.resize(
    cropped_mask,
    (new_width, new_height),
    interpolation=cv2.INTER_NEAREST
)

# Garantir que o canal Alpha venha da máscara
resized[:, :, 3] = resized_mask

# Canvas branco
canvas = np.ones(
    (CANVAS_SIZE, CANVAS_SIZE, 4),
    dtype=np.uint8
)

canvas[:, :, 0:3] = 255
canvas[:, :, 3] = 255

# Posição central
x_offset = (CANVAS_SIZE - new_width) // 2
y_offset = (CANVAS_SIZE - new_height) // 2

# Região onde a joia será colocada
region = canvas[
    y_offset:y_offset + new_height,
    x_offset:x_offset + new_width
]

# Alpha da joia normalizado entre 0 e 1
alpha = resized[:, :, 3].astype(np.float32) / 255.0

# Composição sobre fundo branco
for channel in range(3):

    region[:, :, channel] = (
        resized[:, :, channel] * alpha
        + region[:, :, channel] * (1 - alpha)
    ).astype(np.uint8)

# A imagem final será RGB/BGR normal, sem transparência
region[:, :, 3] = 255

canvas[
    y_offset:y_offset + new_height,
    x_offset:x_offset + new_width
] = region

cv2.imwrite(OUTPUT_PATH, canvas)

print("Imagem padronizada!")
print(f"Tamanho original da joia: {width} x {height}")
print(f"Tamanho final da joia: {new_width} x {new_height}")
print(f"Canvas: {CANVAS_SIZE} x {CANVAS_SIZE}")
print(f"Salvo em: {OUTPUT_PATH}")