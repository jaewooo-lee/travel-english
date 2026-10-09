FROM python:3.10-slim
WORKDIR /app

# 시스템 의존성 설치 및 타임존 설정 (필요시)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 라이브러리 설치
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 소스코드 전체 복사 (app/ 및 data/ 포함)
COPY backend/ ./backend/

# 시놀로지 NAS 마운트 등을 위한 영구 볼륨 디렉토리 생성
RUN mkdir -p /app/data

# 데이터 볼륨 경로 지정 (sqlite db가 생성될 위치)
VOLUME ["/app/data"]

# 환경변수 기본값 설정 (DB_DIR 지정)
ENV DB_DIR=/app/data

# 작업 경로 변경
WORKDIR /app/backend

# 서비스 포트
EXPOSE 8000

# uvicorn 구동
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
