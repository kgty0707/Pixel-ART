# app/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1.routes_generate import router as generate_router


app = FastAPI(title="PixelArt Generation API")

# API 라우터 등록
app.include_router(generate_router)

# 정적 파일(Frontend) 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    """
    루트 경로('/') 접속 시 'static/index.html' 파일을 반환
    """
    return FileResponse("static/index.html")


if __name__ == "__main__":
    print("Starting FastAPI server at http://127.0.0.1:8000")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
