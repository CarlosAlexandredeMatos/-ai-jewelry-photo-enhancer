from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path


class JewelryPipeline:

    def __init__(self, model_path="models/yolov8n-seg.pt"):
        print("Carregando modelo YOLO...")
        self.model = YOLO(model_path)

    def segment(self, image):

        results = self.model.predict(
            source=image,
            conf=0.25,
            verbose=False
        )

        result = results[0]

        if result.masks is None:
            raise ValueError("Nenhuma joia foi segmentada.")

        masks = result.masks.data

        combined_mask = np.zeros(
            image.shape[:2],
            dtype=np.uint8
        )

        for mask in masks:

            mask = mask.cpu().numpy()

            mask = cv2.resize(
                mask,
                (image.shape[1], image.shape[0])
            )

            mask = (mask > 0.5).astype(np.uint8) * 255

            combined_mask = cv2.max(
                combined_mask,
                mask
            )

        return combined_mask

    def remove_background(self, image, mask):

        rgba = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2BGRA
        )

        rgba[:, :, 3] = mask

        return rgba

    def standardize(
        self,
        rgba,
        mask,
        canvas_size=2000,
        target_size=1400
    ):

        ys, xs = np.where(mask > 0)

        if len(xs) == 0:
            raise ValueError("Máscara vazia.")

        x_min = xs.min()
        x_max = xs.max()
        y_min = ys.min()
        y_max = ys.max()

        cropped = rgba[
            y_min:y_max + 1,
            x_min:x_max + 1
        ]

        cropped_mask = mask[
            y_min:y_max + 1,
            x_min:x_max + 1
        ]

        height, width = cropped.shape[:2]

        scale = target_size / max(
            width,
            height
        )

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

        resized[:, :, 3] = resized_mask

        canvas = np.ones(
            (canvas_size, canvas_size, 4),
            dtype=np.uint8
        ) * 255

        x_offset = (
            canvas_size - new_width
        ) // 2

        y_offset = (
            canvas_size - new_height
        ) // 2

        region = canvas[
            y_offset:y_offset + new_height,
            x_offset:x_offset + new_width
        ]

        alpha = (
            resized[:, :, 3]
            .astype(np.float32) / 255.0
        )

        for channel in range(3):

            region[:, :, channel] = (
                resized[:, :, channel] * alpha
                + region[:, :, channel] * (1 - alpha)
            ).astype(np.uint8)

        canvas[
            y_offset:y_offset + new_height,
            x_offset:x_offset + new_width
        ] = region

        return canvas

    def add_shadow(
        self,
        image,
        offset_x=0,
        offset_y=25,
        blur=35,
        opacity=0.25
    ):

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        _, mask = cv2.threshold(
            gray,
            245,
            255,
            cv2.THRESH_BINARY_INV
        )

        matrix = np.float32([
            [1, 0, offset_x],
            [0, 1, offset_y]
        ])

        shadow_mask = cv2.warpAffine(
            mask,
            matrix,
            (image.shape[1], image.shape[0])
        )

        shadow_mask = cv2.GaussianBlur(
            shadow_mask,
            (0, 0),
            blur
        )

        alpha = (
            shadow_mask.astype(np.float32)
            / 255.0
        ) * opacity

        result = image.astype(np.float32)

        for channel in range(3):

            result[:, :, channel] = (
                result[:, :, channel]
                * (1 - alpha)
            )

        return np.clip(
            result,
            0,
            255
        ).astype(np.uint8)

    def process(self, image_path):

        print("\n=== AI JEWELRY PHOTO ENHANCER ===")

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(
                f"Imagem não encontrada: {image_path}"
            )

        print("1. Segmentando...")
        mask = self.segment(image)

        print("2. Removendo fundo...")
        rgba = self.remove_background(
            image,
            mask
        )

        print("3. Padronizando...")
        standardized = self.standardize(
            rgba,
            mask
        )

        print("4. Criando sombra...")
        final = self.add_shadow(
            standardized
        )

        return final


if __name__ == "__main__":

    pipeline = JewelryPipeline()

    result = pipeline.process(
        "data/raw/joia_teste.jpg"
    )

    output_path = (
        "data/output/"
        "joia_teste_final.png"
    )

    cv2.imwrite(
        output_path,
        result
    )

    print("\nProcessamento concluído!")
    print(f"Resultado: {output_path}")