import cv2

IMAGE_PATH = "data/raw/joia_teste.jpg"

image = cv2.imread(IMAGE_PATH)

if image is None:
    print("Erro: não foi possível carregar a imagem.")
    exit()

height, width, channels = image.shape

print("Imagem carregada com sucesso!")
print(f"Largura: {width} px")
print(f"Altura: {height} px")
print(f"Canais: {channels}")

cv2.imshow("Joia", image)

cv2.waitKey(0)
cv2.destroyAllWindows()