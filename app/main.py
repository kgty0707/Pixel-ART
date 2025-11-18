# app/main.py
import uvicorn
import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1.routes_generate import router as generate_router
from app.services.worker import run_worker

# 환경 변수로 embedded worker 제어
RUN_EMBEDDED_WORKER = os.getenv("RUN_EMBEDDED_WORKER", "true").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 최신 권장 방식: lifespan 이벤트 핸들러
    startup + shutdown 모두 처리
    """
    worker_task = None

    if RUN_EMBEDDED_WORKER:
        print("[lifespan] Running embedded worker in FastAPI process (DEV mode).")
        worker_task = asyncio.create_task(run_worker())

    # 앱 실행 구간
    yield

    # 종료 시 워커도 정리
    if worker_task:
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            print("[lifespan] Worker task cancelled.")


app = FastAPI(title="PixelArt Generation API", lifespan=lifespan)

app.include_router(generate_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    print("Starting FastAPI server at http://127.0.0.1:8000")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
