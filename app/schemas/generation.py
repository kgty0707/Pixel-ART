from pydantic import BaseModel


class ImageRequest(BaseModel):
    """프롬프트를 받아 오는 요청 스키마"""
    prompt: str


class ImageResponse(BaseModel):
    """이미지 URL과 프롬프트를 반환하는 응답 스키마"""
    imageUrl: str
    prompt: str
