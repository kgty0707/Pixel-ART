from fastapi import APIRouter, HTTPException
from uuid import uuid4
import json

from app.schemas.generation import ImageRequest  # prompt만 있는 요청 모델
from app.schemas.job import JobResponse, StatusResponse, ImageResult
from app.core.redis_client import redis, QUEUE_NAME

router = APIRouter(prefix="/api/v1", tags=["generate"])


@router.post("/generate", response_model=JobResponse)
async def generate_image_endpoint(request: ImageRequest) -> JobResponse:
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    trigger = "in sks_pixelart_style"
    final_prompt = f"{request.prompt} {trigger}"
    
    job_id = str(uuid4())

    # 초기 상태 저장
    await redis.hset(
        f"job:{job_id}",
        mapping={
            "status": "pending",
            "prompt": final_prompt,
        },
    )

    # 큐에 작업 push
    payload = {"id": job_id, "prompt": final_prompt}
    await redis.lpush(QUEUE_NAME, json.dumps(payload))

    return JobResponse(jobId=job_id, status="pending")


@router.get("/status/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str) -> StatusResponse:
    status = await redis.hget(f"job:{job_id}", "status")
    if status is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return StatusResponse(jobId=job_id, status=status)


@router.get("/result/{job_id}", response_model=ImageResult)
async def get_result(job_id: str) -> ImageResult:
    record = await redis.hgetall(f"job:{job_id}")
    if not record:
        raise HTTPException(status_code=404, detail="Job not found")

    status = record.get("status")
    if status != "done":
        # 아직 처리 중이면 202
        raise HTTPException(status_code=202, detail=f"Job status: {status}")

    # base64 또는 URL 형태 모두 지원
    image_url = record.get("result_url")
    image_data = record.get("result_base64")
    prompt = record.get("prompt", "")

    if not (image_url or image_data):
        raise HTTPException(status_code=500, detail="Result not found")

    return ImageResult(
        jobId=job_id,
        prompt=prompt,
        imageUrl=image_url,
        imageData=image_data,
    )
