# app/services/worker.py
import asyncio
import json

from app.core.redis_client import redis, QUEUE_NAME
from app.services.generation_service import generate_pixelart_image


async def run_worker() -> None:
    """
    Redis 큐에서 작업을 소비하는 무한 루프 워커.
    - QUEUE_NAME 리스트에서 BRPOP
    - 상태: pending -> running -> done/error
    - 결과: result_base64에 base64 PNG 저장
    """
    print("[worker] Started. Waiting for jobs...")
    
    try:
        while True:
            job = await redis.brpop(QUEUE_NAME, timeout=1)
            
            if job is None:
                continue

            _, payload = job
            data = json.loads(payload)

            job_id = data.get("id")
            prompt = data.get("prompt")

            if not job_id or not prompt:
                print(f"[worker] Invalid job payload: {data}")
                continue

            print(f"[worker] Processing job_id={job_id}, prompt={prompt!r}")
            await redis.hset(f"job:{job_id}", "status", "running")

            try:
                # 실제 모델 호출 (이 함수가 동기 함수라면, 너무 오래 걸릴 때 강제 종료가 조금 늦을 순 있습니다)
                img_b64 = generate_pixelart_image(prompt=prompt, seed=None)

                await redis.hset(
                    f"job:{job_id}",
                    mapping={
                        "status": "done",
                        "result_base64": img_b64,
                        "prompt": prompt,
                    },
                )
                print(f"[worker] Job {job_id} done.")
            except Exception as exc:
                print(f"[worker] Job {job_id} failed: {exc}")
                await redis.hset(
                    f"job:{job_id}",
                    mapping={"status": "error", "error_message": str(exc)},
                )

    except asyncio.CancelledError:
        print("[worker] 🛑 Worker shutting down gracefully...")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        pass