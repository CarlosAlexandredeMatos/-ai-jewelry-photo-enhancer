import cv2
import numpy as np

IMAGE_PATH = "data/raw/joia_teste.jpg"
MASK_PATH = "data/masks/joia_teste_mask.png"
OUTPUT_PATH = "data/processed/joia_teste_rgba.png"

image = cv2.imread(IMAGE_PATH, cv2.IMREAD_COLOR)
mask = cv2.imread(MASK_PATH, cv2.IMREAD_GRAYSCALE)

if image is None:
    raise FileNotFoundError("Imagem original não encontrada.")

if mask is None:
    raise FileNotFoundError("Máscara não encontrada.")

if image.shape[:2] != mask.shape[:2]:
    raise ValueError("Imagem e máscara possuem dimensões diferentes.")

# Criar canal alpha
alpha = mask

# Converter BGR → BGRA
rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

# Substituir canal alpha
rgba[:, :, 3] = alpha

cv2.imwrite(OUTPUT_PATH, rgba)

print(f"Imagem RGBA salva em: {OUTPUT_PATH}")