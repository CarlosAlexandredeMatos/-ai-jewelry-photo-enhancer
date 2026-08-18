import cv2

IMAGE_PATH = "data/raw/joia_teste.jpg"
OUTPUT_PATH = "data/processed/joia_teste_gray.jpg"

image = cv2.imread(IMAGE_PATH)

if image is None:
    print("Erro: não foi possível carregar a imagem.")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imwrite(OUTPUT_PATH, gray)

print("Imagem convertida para escala de cinza!")
print(f"Resultado salvo em: {OUTPUT_PATH}")