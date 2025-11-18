from fastapi import APIRouter, HTTPException
from app.schemas.generation import ImageRequest, ImageResponse
from app.services.generation_service import get_mock_pixel_art_url, generate_pixelart_image

router = APIRouter(
    prefix="/api/v1",
    tags=["generate"],
)

@router.post("/generate", response_model=ImageResponse)
async def generate_image_endpoint(request: ImageRequest):
    """
    프롬프트를 받아 실제 픽셀 아트 이미지를 생성해
    base64 data URL 형태로 반환하는 엔드포인트.
    """
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        # 1) 실제 모델로부터 base64 PNG 문자열을 얻고
        img_b64 = generate_pixelart_image(
            prompt=request.prompt,
            seed=None,  # 나중에 ImageRequest에 seed를 넣으면 여기 연결
        )

        # 2) 프론트에서 그대로 <img src="...">로 쓸 수 있게 data URL로 포장
        data_url = f"data:image/png;base64,{img_b64}"

        # 3) ImageResponse 스키마에 맞춰서 반환
        return ImageResponse(
            imageUrl=data_url,
            prompt=request.prompt,
        )

    except Exception as e:
        print(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image")

# @router.post("/generate", response_model=ImageResponse)
# async def generate_image_endpoint(request: ImageRequest):
#     """
#     프롬프트를 받아 픽셀 아트 이미지 URL을 반환하는 API 엔드포인트
#     """
#     if not request.prompt:
#         raise HTTPException(status_code=400, detail="Prompt cannot be empty")

#     try:
#         image_url = get_mock_pixel_art_url(request.prompt)
#         return ImageResponse(imageUrl=image_url, prompt=request.prompt)
#     except Exception as e:
#         print(f"Error generating image: {e}")
#         raise HTTPException(status_code=500, detail="Failed to generate image")