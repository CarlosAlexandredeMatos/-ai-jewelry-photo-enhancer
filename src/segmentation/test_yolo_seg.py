from ultralytics import YOLO

MODEL_PATH = "yolo11n-seg.pt"
IMAGE_PATH = "data/raw/joia_teste.jpg"

model = YOLO(MODEL_PATH)

results = model.predict(
    source=IMAGE_PATH,
    save=True,
    conf=0.25
)

print("Processamento concluído!")