from fastapi import APIRouter, HTTPException
from app.schemas.generation import ImageRequest, ImageResponse
from app.services.generation_service import generate_pixelart_image
from app.services.generation_service import get_mock_pixel_art_url

router = APIRouter(
    prefix="/api/v1",
    tags=["generate"],
)

# @router.post("/", response_model=GenerateResponse)
# async def generate(req: GenerateRequest):
#     img_b64 = generate_pixelart_image(req.prompt, seed=req.seed)
#     return GenerateResponse(
#         image_base64=img_b64,
#         seed=req.seed,
#     )

@router.post("/generate", response_model=ImageResponse)
async def generate_image_endpoint(request: ImageRequest):
    """
    프롬프트를 받아 픽셀 아트 이미지 URL을 반환하는 API 엔드포인트
    """
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        image_url = get_mock_pixel_art_url(request.prompt)
        return ImageResponse(imageUrl=image_url, prompt=request.prompt)
    except Exception as e:
        print(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate image")