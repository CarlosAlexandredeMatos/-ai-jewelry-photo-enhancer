from ultralytics import YOLO
import cv2
import numpy as np

MODEL_PATH = "models/yolov8n-seg.pt"
IMAGE_PATH = "data/raw/joia_teste.jpg"
MASK_PATH = "data/masks/joia_teste_mask.png"

model = YOLO(MODEL_PATH)

results = model.predict(
    source=IMAGE_PATH,
    conf=0.25,
    verbose=False
)

result = results[0]

if result.masks is None:
    print("Nenhuma máscara encontrada.")
    exit()

masks = result.masks.data

print(f"Máscaras encontradas: {len(masks)}")

# Criar máscara final vazia
combined_mask = np.zeros(
    (result.orig_shape[0], result.orig_shape[1]),
    dtype=np.uint8
)

for mask in masks:

    mask = mask.cpu().numpy()

    mask = cv2.resize(
        mask,
        (result.orig_shape[1], result.orig_shape[0])
    )

    mask = (mask > 0.5).astype(np.uint8) * 255

    combined_mask = cv2.max(
        combined_mask,
        mask
    )

cv2.imwrite(MASK_PATH, combined_mask)

print(f"Máscara salva em: {MASK_PATH}")