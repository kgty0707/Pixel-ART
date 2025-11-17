from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_model_id: str = "runwayml/stable-diffusion-v1-5"
    lcm_lora_id: str = "latent-consistency/lcm-lora-sdv1-5"
    style_lora_dir: str = "models/lora/style"
    style_lora_name: str = "pytorch_lora_weights.safetensors"
    device: str = "cuda"

    # v2에서 Config 대신 model_config 사용
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
