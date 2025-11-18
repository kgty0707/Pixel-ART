from io import BytesIO
import base64
from app.models.pipeline import PixelArtPipeline
import time
import random
import urllib.parse
from datetime import datetime


# 앱 전체에서 한 번만 쓰는 전역 인스턴스 (FastAPI startup에서 초기화하는 방식도 있음)
pipeline = PixelArtPipeline()


def generate_pixelart_image(prompt: str, seed: int | None = None) -> str:
    negative = "blurry, low quality, photo, 3d render, realistic"
    img = pipeline.generate(
        prompt=prompt,
        negative_prompt=negative,
        seed=seed,
        num_inference_steps=8,
        guidance_scale=1.0,
        out_size=64,
    )

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded

def get_mock_pixel_art_url(prompt: str) -> str:
    """
    실제 AI 모델 대신 placeholder 이미지 URL을 반환하는 모의 함수.

    나중에 여기 부분을:
    1. Stable Diffusion + LoRA 파이프라인 호출
    2. 생성 이미지를 S3/로컬에 저장
    3. 저장된 이미지의 URL을 반환
    이런 식으로 교체하면 됨.
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received prompt: {prompt}")

    # 모의 생성 시간 (2초 ~ 5초)
    mock_delay = random.uniform(2, 5)
    time.sleep(mock_delay)

    encoded_prompt = urllib.parse.quote(prompt)

    image_url = f"https://placehold.co/256x256/0d1117/00dbde?text={encoded_prompt}&font=pressstart2p"

    print(f"Generated mock image URL: {image_url}")
    return image_url