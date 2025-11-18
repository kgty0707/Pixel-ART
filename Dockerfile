FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

# 기본 작업 디렉토리
WORKDIR /code

# 시스템 패키지
RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 파이썬 패키지 설치
COPY ./requirements-clean.txt /code/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /code/requirements.txt

# 앱 코드 복사
COPY ./app /code/app
COPY ./static /code/static
COPY ./models /code/models

# 로그 버퍼링 방지
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# 기본 CMD: API 서버 실행 (worker는 compose에서 override)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
