import torch
from diffusers import StableCascadeDecoderPipeline, StableCascadePriorPipeline

def generate_single_background(lyrics):
    prior = StableCascadePriorPipeline.from_pretrained(
        "stabilityai/stable-cascade-prior", variant="bf16", torch_dtype=torch.bfloat16
    )
    decoder = StableCascadeDecoderPipeline.from_pretrained(
        "stabilityai/stable-cascade", variant="bf16", torch_dtype=torch.float16
    )

    prompt = f"(generate a cartoon depicting the following lyrics) {lyrics}"

    generated_image = None

    prior.enable_model_cpu_offload()
    prior_output = prior(
        prompt=prompt,
        height=1024,
        width=1024,
        negative_prompt="font visualization",
        guidance_scale=4.0,
        num_images_per_prompt=1,
        num_inference_steps=20,
    )
    decoder.enable_model_cpu_offload()
    decoder_output = decoder(
        image_embeddings=prior_output.image_embeddings.to(torch.float16),
        prompt=prompt,
        negative_prompt="font visualization",
        guidance_scale=0.0,
        output_type="pil",
        num_inference_steps=10,
    ).images[0]
    generated_image = decoder_output

    del prior
    del decoder

    torch.cuda.empty_cache()

    return generated_image

def generate_backgrounds(lyrics):
    prior = StableCascadePriorPipeline.from_pretrained(
        "stabilityai/stable-cascade-prior", variant="bf16", torch_dtype=torch.bfloat16
    )
    decoder = StableCascadeDecoderPipeline.from_pretrained(
        "stabilityai/stable-cascade", variant="bf16", torch_dtype=torch.float16
    )

    prompts = [
        f"Create a charming watercolor illustration inspired by the following lyrics: {lyrics}. Use a storybook style with soft, rounded forms and pastel tones suitable for children.",
        f"(generate a cartoon depicting the following lyrics) {lyrics}",
        f"{lyrics}",
    ]

    generated_images = []

    for prompt in prompts:
        prior.enable_model_cpu_offload()
        prior_output = prior(
            prompt=prompt,
            height=1024,
            width=1024,
            negative_prompt="font visualization",
            guidance_scale=4.0,
            num_images_per_prompt=1,
            num_inference_steps=20,
        )
        decoder.enable_model_cpu_offload()
        decoder_output = decoder(
            image_embeddings=prior_output.image_embeddings.to(torch.float16),
            prompt=prompt,
            negative_prompt="font visualization",
            guidance_scale=0.0,
            output_type="pil",
            num_inference_steps=10,
        ).images[0]
        generated_images.append(decoder_output)

    del prior
    del decoder

    torch.cuda.empty_cache()

    return generated_images
