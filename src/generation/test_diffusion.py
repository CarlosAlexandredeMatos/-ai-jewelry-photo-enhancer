import torch
from diffusers import StableDiffusionPipeline


MODEL_ID = "runwayml/stable-diffusion-v1-5"

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Dispositivo: {device}")

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16
)

pipe = pipe.to(device)

# Reduz uso de memória
pipe.enable_attention_slicing()

prompt = (
    "professional studio product photography "
    "of a luxury jewelry ring, white background, "
    "soft studio lighting, realistic metal reflections, "
    "high quality product photography"
)

print("Gerando imagem...")

image = pipe(
    prompt=prompt,
    height=512,
    width=512,
    num_inference_steps=20,
    guidance_scale=7.5
).images[0]

output_path = "data/output/diffusion_test.png"

image.save(output_path)

print(f"Imagem salva em: {output_path}")