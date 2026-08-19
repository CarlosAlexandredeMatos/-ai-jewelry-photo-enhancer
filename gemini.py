import os
from pathlib import Path

from google import genai
from google.genai import types


MODEL = "gemini-3.1-flash-image"


PROMPT = """
Transform this jewelry photograph into a premium professional jewelry
photograph suitable for a high-end jewelry store.

The jewelry in the input image is the REAL PRODUCT.

PRESERVE EXACTLY:
- geometry
- proportions
- shape
- number of stones
- position of every stone
- stone shapes and sizes
- metal structure
- settings
- prongs
- engravings
- ornaments
- links
- every physical detail

DO NOT redesign the jewelry.
DO NOT add stones.
DO NOT remove stones.
DO NOT change the geometry.
DO NOT invent details.

Improve ONLY the photographic presentation.

Make it look like professional luxury jewelry photography:
- professional macro photography
- extremely detailed gemstones
- realistic gemstone reflections and refraction
- elegant natural sparkle
- realistic polished metal
- beautiful controlled reflections
- sophisticated studio lighting
- soft shadows
- high dynamic range
- excellent exposure
- accurate white balance
- premium color grading
- sharp jewelry
- natural shallow depth of field
- smooth professional bokeh
- minimal noise
- professional commercial retouching

You may subtly enhance existing colors to make the jewelry more
luxurious and commercially attractive.

Existing gold may look richer and warmer.
Existing silver/platinum may look cleaner and more polished.
Existing gemstones may have enhanced brilliance and sparkle.

Do NOT change the actual gemstone colors.
Do NOT change the metal type.
Do NOT invent stones.

The final result must look like a REAL professional photograph
of the EXACT SAME jewelry.

Do not reproduce text, logos, watermarks or social-media UI.
"""


def melhorar_foto(caminho_imagem: str, caminho_saida: str):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY não foi encontrada."
        )

    client = genai.Client(api_key=api_key)

    imagem = Path(caminho_imagem)

    print(f"Enviando: {imagem.name}")

    uploaded = client.files.upload(
        file=imagem
    )

    print("Processando com Gemini...")

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            uploaded,
            PROMPT,
        ],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    if not response.candidates:
        raise RuntimeError("Gemini não retornou candidatos.")

    for part in response.candidates[0].content.parts:

        if part.inline_data is not None:

            resultado = part.as_image()

            resultado.save(caminho_saida)

            print(f"Resultado salvo em: {caminho_saida}")

            return

    raise RuntimeError(
        "O Gemini respondeu, mas não retornou uma imagem."
    )


if __name__ == "__main__":

    melhorar_foto(
        "data/raw/joia_teste.jpg",
        "output/teste_resultado.png"
    )