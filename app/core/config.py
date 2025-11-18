from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    base_model_id: str = "runwayml/stable-diffusion-v1-5"
    lcm_lora_id: str = "latent-consistency/lcm-lora-sdv1-5"

    style_lora_dir: str = str(BASE_DIR / "models" / "lora" / "style")
    style_lora_name: str = "pytorch_lora_weights.safetensors"

    concept_lora_dir: str = str(BASE_DIR / "models" / "lora" / "concept")
    concept_lora_name: str = "pytorch_lora_weights.safetensors"

    device: str = "cuda"

    # pydantic v2 설정
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
