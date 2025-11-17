import torch
from diffusers import DiffusionPipeline, LCMScheduler
from PIL import Image
from . import __init__  # 패키지 인식용
from app.core.config import settings


class PixelArtPipeline:
    def __init__(self):
        device = settings.device
        dtype = torch.float16 if device == "cuda" else torch.float32

        self.pipe = DiffusionPipeline.from_pretrained(
            settings.base_model_id,
            torch_dtype=dtype,
        )
        self.pipe.scheduler = LCMScheduler.from_config(self.pipe.scheduler.config)

        # LCM LoRA
        self.pipe.load_lora_weights(
            settings.lcm_lora_id,
            adapter_name="lcm",
        )

        # 스타일 LoRA
        self.pipe.load_lora_weights(
            settings.style_lora_dir,
            weight_name=settings.style_lora_name,
            adapter_name="style",
        )

        # 두 어댑터 조합
        self.pipe.set_adapters(
            ["lcm", "style"],
            [1.0, 0.9],  # 추후 config로 빼도 됨
        )

        if device == "cuda":
            self.pipe.enable_model_cpu_offload()

    @torch.inference_mode()
    def generate(
        self,
        prompt: str,
        negative_prompt: str | None = None,
        num_inference_steps: int = 8,
        guidance_scale: float = 1.0,
        seed: int | None = None,
        out_size: int = 64,
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

        if out_size is not None:
            result = result.resize((out_size, out_size), Image.Resampling.LANCZOS)
        return result
