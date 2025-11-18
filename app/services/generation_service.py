from io import BytesIO
import base64
from app.models.pipeline import PixelArtPipeline
import time
import random
import urllib.parse
from datetime import datetime

_pipeline = None

# TODO: 모델 로딩 미리 백그라운드로 효율적 배치 필요
def get_pipeline():
    global _pipeline
    if _pipeline is None:
        print("🎨 모델 로딩을 시작합니다...") 
        _pipeline = PixelArtPipeline()
    return _pipeline

def generate_pixelart_image(prompt: str, seed: int | None = None) -> str:
    pipeline = get_pipeline()
    negative = "blurry, photo, 3d render, realistic"

    img = pipeline.generate(
        prompt=prompt,
        negative_prompt=negative,
        seed=seed,
        num_inference_steps=8,
        guidance_scale=1.0,
    )

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded