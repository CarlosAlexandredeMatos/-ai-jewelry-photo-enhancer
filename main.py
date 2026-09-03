import os
import base64
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# CONFIGURAÇÃO
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY não encontrada. "
        "Crie um arquivo .env com sua chave."
    )

client = OpenAI(api_key=api_key)


# ============================================================
# PASTAS
# ============================================================

MASTER_IMAGE = Path("data/mestre/mestre.jpeg")

INPUT_DIR = Path("data/joias")
OUTPUT_DIR = Path("data/joias_geradas")


# ============================================================
# MODELO
# ============================================================

MODEL = "gpt-image-2"

QUALITY = "low"
SIZE = "1024x1024"

MAX_RETRIES = 1


# ============================================================
# PROMPT
# ============================================================

PROMPT = """
TWO IMAGES ARE PROVIDED.

IMAGE 1 = MASTER POSE REFERENCE
IMAGE 2 = ACTUAL PRODUCT


============================================================
ABSOLUTE RULE
============================================================

IMAGE 2 IS THE PRODUCT.

IMAGE 1 IS ONLY A POSE AND CAMERA-ANGLE REFERENCE.

The final image MUST contain the exact jewelry from IMAGE 2.

IMAGE 1 must NEVER be used as a reference for the appearance,
material, color, geometry or design of the product.


============================================================
IMAGE 1 — USE ONLY FOR POSITION AND ANGLE
============================================================

Analyze IMAGE 1 ONLY to determine:

- product position within the frame
- product orientation
- product rotation
- viewing angle
- camera angle relative to the product
- perspective
- product scale within the frame
- framing
- placement of the product within the image

Reproduce ONLY these spatial characteristics.

DO NOT copy anything else from IMAGE 1.


============================================================
DO NOT COPY FROM IMAGE 1
============================================================

IGNORE the jewelry itself in IMAGE 1.

DO NOT use IMAGE 1 as a reference for:

- metal color
- metal type
- material
- surface
- finish
- reflections
- gemstones
- gemstone color
- gemstone arrangement
- geometry
- shape
- proportions
- thickness
- details
- texture
- design
- appearance
- lighting
- color grading
- background

IMAGE 1 ONLY DEFINES WHERE AND HOW THE PRODUCT IS VIEWED.


============================================================
IMAGE 2 — ABSOLUTE PRODUCT SOURCE
============================================================

IMAGE 2 is the ONLY source of truth for the product.

Preserve the product from IMAGE 2 exactly.

Every property of the jewelry must remain unchanged.

Preserve:

- exact geometry
- exact shape
- exact silhouette
- exact proportions
- exact dimensions
- exact thickness
- exact structure
- exact metal type
- exact metal color
- exact metal finish
- exact surface appearance
- exact gemstones
- exact gemstone count
- exact gemstone shape
- exact gemstone size
- exact gemstone color
- exact gemstone position
- exact gemstone setting
- exact prongs
- exact engravings
- exact details
- exact texture
- exact design


============================================================
METAL COLOR — IMMUTABLE
============================================================

The metal color MUST come exclusively from IMAGE 2.

NEVER infer the metal color from IMAGE 1.

If IMAGE 2 shows SILVER, the final product MUST be SILVER.

If IMAGE 2 shows GOLD, the final product MUST be GOLD.

If IMAGE 2 shows WHITE GOLD, the final product MUST be WHITE GOLD.

If IMAGE 2 shows PLATINUM, the final product MUST be PLATINUM.

If IMAGE 2 shows ROSE GOLD, the final product MUST be ROSE GOLD.

NEVER swap metal colors.

SILVER → SILVER.

GOLD → GOLD.

WHITE GOLD → WHITE GOLD.

PLATINUM → PLATINUM.

ROSE GOLD → ROSE GOLD.


============================================================
NO PRODUCT MODIFICATION
============================================================

DO NOT:

- redesign the jewelry
- reconstruct the jewelry
- reinterpret the jewelry
- improve the jewelry
- simplify the jewelry
- add details
- remove details
- change proportions
- change geometry
- change materials
- change colors
- change gemstones
- change gemstone positions
- change metal finish
- change surface characteristics


============================================================
POSE TRANSFER
============================================================

Take the EXACT PRODUCT from IMAGE 2.

Place and orient it according to IMAGE 1.

Match the spatial configuration of IMAGE 1:

- same viewing angle
- same orientation
- same rotation
- same perspective
- same position in the frame
- same relative scale
- same framing

The product itself must remain unchanged.

Only its spatial presentation may be changed.


============================================================
IMPORTANT MENTAL MODEL
============================================================

Imagine that IMAGE 2 is a real physical piece of jewelry.

Do NOT create a new version of it.

Instead:

Take the exact physical product from IMAGE 2
and position it in front of the camera
at the exact viewing angle and position shown in IMAGE 1.

IMAGE 1 tells you:

"WHERE IS THE PRODUCT?"

"HOW IS THE PRODUCT ORIENTED?"

"FROM WHAT ANGLE IS THE PRODUCT BEING VIEWED?"

IMAGE 2 tells you:

"WHAT IS THE PRODUCT?"

Nothing from IMAGE 1 should alter the answer to
"What is the product?"


============================================================
FINAL OUTPUT
============================================================

Generate the exact jewelry from IMAGE 2.

Match ONLY the angle, orientation, perspective,
position and framing of IMAGE 1.

The product must remain identical to IMAGE 2
in every other respect.

FINAL RULE:

IMAGE 1 = ANGLE + POSITION + ORIENTATION + FRAMING ONLY.

IMAGE 2 = EVERYTHING ABOUT THE PRODUCT.

DO NOT TRANSFER ANY PRODUCT PROPERTY FROM IMAGE 1.

DO NOT MODIFY ANY PRODUCT PROPERTY FROM IMAGE 2.

ONLY CHANGE THE PRODUCT'S SPATIAL PRESENTATION.
"""


    
# ============================================================
# VALIDAR IMAGEM
# ============================================================

def validate_file(path: Path):

    if not path.exists():
        raise RuntimeError(
            f"Arquivo não encontrado: {path}"
        )

    if path.stat().st_size == 0:
        raise RuntimeError(
            f"Arquivo vazio: {path}"
        )


# ============================================================
# GERAR UMA IMAGEM
# ============================================================

def generate_image(
    master_path: Path,
    product_path: Path,
    output_path: Path,
):

    validate_file(master_path)
    validate_file(product_path)

    print(f"\nProduto: {product_path.name}")
    print(f"Mestre:  {master_path.name}")

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            print(
                f"Tentativa {attempt}/{MAX_RETRIES}..."
            )

            # ------------------------------------------------
            # IMPORTANTE:
            #
            # As duas imagens são enviadas para o modelo.
            #
            # A ordem corresponde ao prompt:
            #
            # imagem 1 = MESTRE
            # imagem 2 = PRODUTO
            # ------------------------------------------------

            with open(master_path, "rb") as master_file, \
                 open(product_path, "rb") as product_file:

                result = client.images.edit(
                    model=MODEL,

                    image=[
                        master_file,
                        product_file,
                    ],

                    prompt=PROMPT,

                    quality=QUALITY,
                    size=SIZE,
                )

            # ------------------------------------------------
            # OBTER BASE64
            # ------------------------------------------------

            image_base64 = result.data[0].b64_json

            if not image_base64:
                raise RuntimeError(
                    "A API não retornou a imagem em base64."
                )

            # ------------------------------------------------
            # DECODIFICAR
            # ------------------------------------------------

            image_bytes = base64.b64decode(
                image_base64
            )

            # ------------------------------------------------
            # SALVAR
            # ------------------------------------------------

            with open(
                output_path,
                "wb"
            ) as output_file:

                output_file.write(image_bytes)

            print(
                f"Imagem salva: {output_path}"
            )

            return True

        except Exception as error:

            print(
                f"Erro na tentativa {attempt}: {error}"
            )

            if attempt < MAX_RETRIES:

                wait_time = attempt * 3

                print(
                    f"Aguardando {wait_time}s "
                    f"antes de tentar novamente..."
                )

                time.sleep(wait_time)

            else:

                print(
                    "Número máximo de tentativas atingido."
                )

                return False


# ============================================================
# ENCONTRAR IMAGENS
# ============================================================

def get_images():

    extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    if not INPUT_DIR.exists():

        raise RuntimeError(
            f"A pasta '{INPUT_DIR}' não existe."
        )

    images = [
        path
        for path in INPUT_DIR.iterdir()
        if (
            path.is_file()
            and path.suffix.lower() in extensions
        )
    ]

    images.sort()

    return images


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # VALIDAR MESTRE
    # --------------------------------------------------------

    validate_file(MASTER_IMAGE)

    # --------------------------------------------------------
    # CRIAR OUTPUT
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # ENCONTRAR JOIAS
    # --------------------------------------------------------

    images = get_images()

    if not images:

        print(
            "Nenhuma imagem encontrada "
            "na pasta 'joias'."
        )

        return

    # --------------------------------------------------------
    # INFORMAÇÕES
    # --------------------------------------------------------

    total = len(images)

    print("=" * 60)

    print(
        "PROCESSAMENTO DE JOIAS"
    )

    print(
        f"Imagem mestre: {MASTER_IMAGE}"
    )

    print(
        f"Joias encontradas: {total}"
    )

    print(
        f"Modelo: {MODEL}"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # PROCESSAR
    # --------------------------------------------------------

    success = 0
    skipped = 0
    failed = 0

    for index, input_path in enumerate(
        images,
        start=1
    ):

        output_name = (
            f"{input_path.stem}_comercial.png"
        )

        output_path = (
            OUTPUT_DIR / output_name
        )

        print("\n" + "=" * 60)

        print(
            f"[{index}/{total}] "
            f"{input_path.name}"
        )

        # ----------------------------------------------------
        # NÃO GERAR NOVAMENTE
        # ----------------------------------------------------

        if (
            output_path.exists()
            and output_path.stat().st_size > 0
        ):

            print(
                f"Já existe: {output_path.name}"
            )

            print(
                "Pulando para não gastar créditos."
            )

            skipped += 1

            continue

        # ----------------------------------------------------
        # GERAR
        # ----------------------------------------------------

        result = generate_image(
            master_path=MASTER_IMAGE,
            product_path=input_path,
            output_path=output_path,
        )

        if result:

            success += 1

            print(
                f"OK [{index}/{total}]"
            )

        else:

            failed += 1

            print(
                f"FALHOU [{index}/{total}]"
            )

    # --------------------------------------------------------
    # RESUMO
    # --------------------------------------------------------

    print("\n")

    print("=" * 60)

    print("PROCESSAMENTO FINALIZADO")

    print("=" * 60)

    print(
        f"Total:       {total}"
    )

    print(
        f"Concluídas:  {success}"
    )

    print(
        f"Puladas:     {skipped}"
    )

    print(
        f"Falharam:    {failed}"
    )

    print(
        f"Resultados:  {OUTPUT_DIR}"
    )

    print("=" * 60)


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    main()
