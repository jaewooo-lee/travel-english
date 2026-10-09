from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from .database import get_db, SessionLocal
from .seed import seed_data
from . import crud, schemas

app = FastAPI(title="Travel English API", version="1.0.0")

# CORS 설정 (개발 환경 대응)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup 이벤트: DB 초기화 및 데이터 시딩
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

# --- API Endpoints ---

# 1. 100일 과정 목록 및 진척도 조회
@app.get("/api/days", response_model=list[schemas.DayProgressBrief])
def read_days(db: Session = Depends(get_db)):
    return crud.get_days_progress(db)

# 2. 특정 일차 상세 정보 (다이얼로그 및 핵심 표현)
@app.get("/api/days/{day_id}", response_model=schemas.DayProgressDetail)
def read_day_detail(day_id: int, db: Session = Depends(get_db)):
    day = crud.get_day_detail(db, day_id)
    if not day:
        raise HTTPException(status_code=404, detail="Day not found")
    return day

# 3. 특정 일차 학습 완료 처리 (반복 횟수 +1)
@app.post("/api/days/{day_id}/complete", response_model=schemas.DayProgressBrief)
def complete_day(day_id: int, db: Session = Depends(get_db)):
    day = crud.get_day_detail(db, day_id)
    if not day:
        raise HTTPException(status_code=404, detail="Day not found")
    return crud.complete_day(db, day_id)

# 4. 한글 상황 검색 API
@app.get("/api/search", response_model=list[schemas.SearchResultItem])
def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return crud.search_phrases(db, q)

# 5. 통계 정보 조회
@app.get("/api/stats", response_model=schemas.StatsResponse)
def read_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)

# 6. 학습 데이터 초기화
@app.post("/api/reset")
def reset_progress(db: Session = Depends(get_db)):
    crud.reset_progress(db)
    return {"message": "Success"}


# --- SPA Static Files Serving ---

# Static 디렉토리 경로 지정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

# static 폴더가 없으면 미리 임시로 만듬 (빌드 전 에러 방지)
os.makedirs(STATIC_DIR, exist_ok=True)

# index.html이 없을 경우를 대비해 헬스체크 라우트 먼저 등록
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Travel English API server is running."}

# SPA Fallback & Static File Serving: API가 아닌 모든 경로는 파일이 존재하면 서빙하고, 없으면 index.html을 리턴
@app.get("/{catchall:path}")
async def serve_spa(catchall: str):
    # API 요청이었으나 매칭되지 않은 경우 404 리턴
    if catchall.startswith("api") or catchall.startswith("docs") or catchall.startswith("redoc") or catchall.startswith("openapi.json"):
        raise HTTPException(status_code=404, detail="Not Found")
        
    # 요청한 파일이 static 디렉토리에 실제로 존재하면 전송
    file_path = os.path.join(STATIC_DIR, catchall)
    if catchall and os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
        
    # 그 외 경로는 SPA 라우팅을 위해 index.html 반환
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return {
        "message": "Travel English API is running successfully.",
        "note": "Frontend static/index.html not found. Access APIs at /api/days."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
