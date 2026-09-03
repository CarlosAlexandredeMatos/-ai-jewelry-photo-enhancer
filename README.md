python src/segmentation/extract_mask.py
python src/background/remove_background.py
python src/background/standardize.py
python src/background/shadow.py
python src/enhancement/enhance.py

python src/generation/hf_flux_img2img.py




# AI Jewelry Photo Enhancer

AI-powered pipeline for transforming ordinary jewelry photographs into professional e-commerce catalog images while preserving the original product's identity and details.

The project combines **Computer Vision, Deep Learning and Generative AI** to automatically segment the jewelry, remove the original background, standardize composition, improve lighting and colors, generate realistic shadows, and produce a high-quality catalog image.

## 🎯 Objective

Transform:

`ordinary jewelry photo → professional catalog photo`

The system is designed to preserve the real characteristics of the jewelry, including:

* Geometry
* Proportions
* Stones
* Number of stones
* Shape
* Colors
* Metallic details
* Unique product characteristics

Generative AI should be used primarily to improve **lighting, reflections, shadows, background and overall photographic finish**, rather than freely recreating the product.

## 🚀 Pipeline

```text
Original Image
      ↓
Pre-processing
      ↓
Jewelry Segmentation
      ↓
Background Removal
      ↓
Object Standardization
      ↓
Color & Lighting Correction
      ↓
White Background
      ↓
Professional Shadow
      ↓
Generative AI (Optional)
      ↓
Quality Validation
      ↓
Final Catalog Image
```

## 🧠 Technologies

* Python
* OpenCV
* NumPy
* Pillow
* PyTorch
* SAM 2
* YOLO Segmentation
* Stable Diffusion / equivalent models
* ControlNet
* LoRA
* Inpainting
* Image-to-Image
* FastAPI
* Streamlit / Gradio
* Docker
* Git / GitHub

## 🏗️ Development Strategy

The project follows a progressive development strategy.

### V1 — Computer Vision MVP

Start with pre-trained models and deterministic image processing:

* Image preprocessing
* Jewelry segmentation
* Background removal
* Automatic cropping
* Scaling and centering
* White background
* Lighting correction
* Artificial shadow
* Batch processing

### V2 — Generative AI

Introduce generative models to improve:

* Studio lighting
* Metallic reflections
* Shadows
* Product finish
* Photographic quality

### V3 — Fine-tuning

Investigate:

* LoRA
* Diffusion fine-tuning
* ControlNet
* Pix2Pix
* GAN-based approaches

### V4 — Production

Build:

* Web interface
* REST API
* Batch processing
* GPU workers
* Quality control
* Docker deployment
* Cloud GPU infrastructure

## 📁 Project Structure

```text
ai-jewelry-photo-enhancer/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── masks/
│   ├── output/
│   └── dataset/
│
├── models/
│
├── src/
│   ├── preprocessing/
│   ├── segmentation/
│   ├── background/
│   ├── enhancement/
│   ├── generation/
│   ├── validation/
│   └── pipeline/
│
├── tests/
├── notebooks/
├── configs/
├── scripts/
├── app/
│
├── requirements.txt
├── README.md
├── .gitignore
└── Dockerfile
```

## 💎 Supported Jewelry

The initial dataset is planned around:

```text
Ring
Necklace
Earring
Bracelet
Pendant
```

## 🎨 Image Presets

### Catalog

```text
White background
Neutral lighting
Soft shadow
Centered composition
```

### Premium

```text
White background
Studio lighting
Higher contrast
Controlled reflections
Soft shadow
```

### Luxury

```text
Dark background
Dramatic lighting
Controlled reflections
Premium presentation
```

### Instagram

```text
4:5 format
Artistic composition
Premium lighting
Social-media optimized
```

## 📊 Quality Evaluation

The system will evaluate:

### Segmentation

* IoU
* Dice Score
* Precision
* Recall

### Image Similarity

* PSNR
* SSIM
* LPIPS

### Visual Quality

Human evaluation from 1 to 5:

```text
1 = Poor
2 = Below expectations
3 = Acceptable
4 = Professional
5 = Excellent
```

## 🔬 Research

The project will also investigate different approaches for image-to-image transformation:

```text
Traditional Computer Vision
        ↓
Pix2Pix / GAN
        ↓
Diffusion
        ↓
ControlNet
        ↓
LoRA / Fine-tuning
```

The goal is to compare these approaches in terms of:

* Image quality
* Product fidelity
* Processing time
* Computational cost
* Dataset requirements
* Preservation of jewelry identity

## 📈 Dataset

The project will progressively build a proprietary jewelry dataset containing paired images:

```text
Input                         Target

original_jewelry.jpg    →    professional_jewelry.jpg
```

Initial target:

```text
500 image pairs
```

Future targets:

```text
1,000+
2,000+
5,000+
```

## 🔮 Long-Term Vision

The final system should allow a user to simply upload:

```text
ring_photo.jpg
```

select:

```text
CATALOG
```

and automatically receive:

```text
ring_professional.jpg
```

without manually writing prompts.

## 📌 Project Philosophy

**First make it work. Then make it intelligent.**

The project intentionally starts with pre-trained models and deterministic Computer Vision techniques before introducing Generative AI, GANs, LoRA and custom fine-tuning.

This approach allows the core pipeline to be validated before investing in expensive training and large datasets.

## 🛠️ Status

🚧 **Work in progress**

The project is being developed incrementally, from a Computer Vision MVP toward a complete AI-powered jewelry photography processing system.
