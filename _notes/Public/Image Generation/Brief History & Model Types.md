---
title: Brief History & Model Types
---
Image generation has evolved rapidly over the past decade. **GANs** (Generative Adversarial Networks, 2014) were the first major breakthrough, with StyleGAN showing impressive face synthesis. **VAEs** (Variational Autoencoders) offered another early approach but struggled with image quality. The field shifted dramatically around 2020-2021 with **diffusion models**, which became dominant after DALL-E 2, Stable Diffusion, and Midjourney demonstrated superior quality and controllability. Transformers also entered the space with models like DALL-E and later improvements.

### Main Types of Image/Video Generation Models:
* **Diffusion Models**
	- Denoising Diffusion Probabilistic Models (DDPM)
	- Latent Diffusion Models (LDMs) - like Stable Diffusion
	- Variants: DALL-E 2, Imagen, Midjourney
* **GANs** (Generative Adversarial Networks)
	- StyleGAN series
	- BigGAN
	- Progressive GAN
* **Autoregressive Models**
	- DALL-E (original)
	- Parti
	- Generate images token-by-token
* **VAE-based**
	- Vector Quantized VAEs (VQ-VAE)
	- Often used as components in other models
* **Flow-based Models**
	- Normalizing flows
	- Less common now but theoretically elegant
* **Video Generation**
	- Diffusion-based: Stable Video Diffusion, Pika, Runway Gen-2
	- Autoregressive: Phenaki
	- Hybrid approaches: Sora (diffusion transformer)
 
### huggingface Diffusers 
- [huggingface Diffusers Docs](https://huggingface.co/docs/diffusers/index)
- https://huggingface.co/Tongyi-MAI/Z-Image
- https://huggingface.co/Tongyi-MAI/Z-Image-Turbo
- https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
- https://huggingface.co/stabilityai/sd-turbo
- https://huggingface.co/stabilityai/sdxl-turbo