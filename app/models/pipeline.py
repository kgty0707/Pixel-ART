import torch
from diffusers import DiffusionPipeline, LCMScheduler
from PIL import Image
from app.core.config import settings

class PixelArtPipeline:
    def __init__(self):
        device = settings.device
        dtype = torch.float16 if device == "cuda" else torch.float32

        self.pipe = DiffusionPipeline.from_pretrained(
            settings.base_model_id,
            torch_dtype=dtype,
            variant="fp16",  
            use_safetensors=True,
            low_cpu_mem_usage=True,
            safety_checker=None,
        )
        
        self.pipe.scheduler = LCMScheduler.from_config(self.pipe.scheduler.config)

        self.pipe.load_lora_weights(
            settings.lcm_lora_id, adapter_name="lcm"
        )
        self.pipe.load_lora_weights(
            settings.style_lora_dir, weight_name=settings.style_lora_name, adapter_name="style"
        )
        self.pipe.load_lora_weights(
            settings.concept_lora_dir, weight_name=settings.concept_lora_name, adapter_name="concept"
        )

        self.pipe.set_adapters(
            ["lcm", "style", "concept"],
            [1.0, 0.9, 0.7],
        )

        if device == "cuda":
            self.pipe.enable_model_cpu_offload()
            self.pipe.enable_vae_slicing() 
            self.pipe.enable_attention_slicing() 

    @torch.inference_mode()
    def generate(
        self,
        prompt: str,
        negative_prompt: str | None = None,
        num_inference_steps: int = 8,
        guidance_scale: float = 1.0,
        seed: int | None = None,
    ) -> Image.Image:
        device = settings.device
        generator = None
        if seed is not None:
            generator = torch.Generator(device).manual_seed(seed)

        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
            num_images_per_prompt=1,
        ).images[0]

        return result