# ✈️ Travel English (여행 영어 100일 완성 & 긴급 상황 검색)

아이폰 모바일 웹 환경에 최적화된 **여행 영어 학습 및 긴급 회화 검색 웹 애플리케이션**입니다.  
10개 테마, 100일간의 실용 회화 다이얼로그와 핵심 표현을 학습하고 복습 횟수를 관리할 수 있으며, 여행 중 긴급한 상황 발생 시 한글 키워드로 즉시 영어 표현을 찾아 원어민 발음(Web Speech TTS)으로 들을 수 있습니다.

Node.js 빌드 단계 없이 **순수 Python(FastAPI) 단일 스택**으로 구동되며, SQLite DB 볼륨 마운트를 지원하여 **시놀로지 NAS(Container Manager)** 및 Docker 환경에서 간편하게 배포할 수 있습니다.

---

## 📱 주요 기능

1. **100일 완성 여행 회화 코스**
   - 10개 핵심 테마(기내/공항, 교통, 호텔, 식당, 길찾기, 쇼핑, 관광, 긴급상황, 친교, 귀국) 분리
   - 각 Day별 A-B 롤플레잉 다이얼로그 및 핵심 단어/표현 제공
   - 한국어 번역 가리기/보이기 토글 (영어 집중 모드)

2. **학습 진도 & 반복 복습 관리**
   - 일일 학습 완료 처리 및 학습 완료 시 축하 Confetti 마이크로 애니메이션
   - Day별/전체 누적 반복 복습 횟수 관리
   - SQLite 데이터베이스 기반으로 디바이스/환경에 구애받지 않고 영구 보존

3. **긴급 상황 한글 검색**
   - 여행 중 당황스러운 상황(예: "여권 잃어버렸어", "식중독", "택시 요금", "체크아웃")을 한글로 실시간 검색
   - 긴급 표현, 대화문, 핵심 어휘를 통합 검색하여 즉시 표시

4. **네이티브 발음 청취 (Web Speech TTS)**
   - 브라우저 내장 Web Speech API를 활용하여 별도 외부 유료 API나 네트워크 지연 없이 즉각적인 원어민 발음 재생

5. **iOS 스타일 UI/UX**
   - 모바일 웹 뷰에 최적화된 Safe Area 대응 및 하단 탭 바 (홈, 학습, 긴급검색, 내통계)
   - 다크 인디고 & Glassmorphism(유리 모피즘) 비주얼 디자인
   - 데스크톱 접속 시에도 아이폰 프레임 뷰로 렌더링

---

## 🛠️ 기술 스택

- **Backend & Serving**: Python 3.10+, FastAPI, Uvicorn, SQLAlchemy
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (FastAPI 정적 파일 및 SPA Fallback 서빙)
- **Database**: SQLite (`travel_english.db`)
- **Container**: Docker (Multi-architecture: `linux/amd64`, `linux/arm64`), Docker Compose
- **CI/CD**: GitHub Actions

---

## 📁 프로젝트 구조

```
travel-english/
├── .github/
│   └── workflows/
│       └── docker-publish.yml     # GitHub Actions Docker Build & Push 워크플로우
├── backend/
│   ├── app/
│   │   ├── static/               # 프론트엔드 정적 파일 (Vanilla UI)
│   │   │   ├── index.html        # 메인 웹 페이지 마크업
│   │   │   ├── index.css         # iOS 테마 스타일시트
│   │   │   └── app.js            # SPA 라우팅, TTS, 검색, 이벤트 로직
│   │   ├── __init__.py
│   │   ├── crud.py               # 데이터베이스 CRUD 함수
│   │   ├── database.py           # SQLite DB 연결 및 경로 설정
│   │   ├── main.py               # FastAPI 서버 진입점 & SPA 서빙
│   │   ├── models.py             # SQLAlchemy ORM 모델
│   │   ├── schemas.py            # Pydantic 스키마
│   │   └── seed.py               # 초기 100일 데이터 시딩
│   ├── data/
│   │   ├── generate_data.py      # 데이터셋 생성 스크립트
│   │   └── travel_data.json      # 100일 회화 및 긴급 표현 데이터 원본
│   └── requirements.txt          # Python 패키지 의존성 목록
├── Dockerfile                    # 경량화된 단일 파이썬 Dockerfile
├── docker-build.sh               # 로컬 buildx 멀티플랫폼 빌드/푸시 스크립트
├── docker-compose.yml            # Docker Compose / 시놀로지 NAS 배포 설정
└── README.md
```

---

## 🚀 로컬 개발 및 실행 방법

### 1. 가상환경 설정 및 패키지 설치

```bash
# 저장소 루트 디렉토리로 이동
cd travel-english

# 파이썬 가상환경 생성 (Python 3.10 이상 권장)
python3 -m venv venv

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate
# Windows PowerShell인 경우: .\venv\Scripts\Activate.ps1

# 의존성 패키지 설치
pip install -r backend/requirements.txt
```

### 2. 로컬 서버 실행

```bash
# FastAPI 서버 실행 (기본 포트: 8000)
PYTHONPATH=backend python -m app.main
```

실행 후 브라우저에서 `http://localhost:8000` 으로 접속합니다.  
(서버가 기동되면서 `backend/data/travel_data.json`의 100일 데이터가 SQLite로 자동 시딩됩니다.)

---

## 🐳 Docker를 통한 실행 방법

### 1. 로컬에서 Docker 컨테이너 직접 실행

```bash
# DockerHub에서 이미지 pull & 실행
docker run -d \
  --name travel-english \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e TZ=Asia/Seoul \
  --restart unless-stopped \
  jaewooo/travel-english:latest
```

### 2. Docker Compose로 실행

```bash
# 컨테이너 백그라운드 시작
docker compose up -d

# 로그 확인
docker compose logs -f

# 컨테이너 종료
docker compose down
```

### 3. 로컬에서 직접 Docker 이미지 빌드 및 푸시 (`docker-build.sh`)

`docker buildx`를 이용해 `linux/amd64`와 `linux/arm64` 멀티 아키텍처 이미지를 로컬에서 직접 빌드하고 푸시할 수 있습니다.

```bash
# Docker Hub 로그인 필요
docker login

# 빌드 및 푸시 스크립트 실행
./docker-build.sh
```

---

## 📦 시놀로지 NAS (Container Manager) 배포 가이드

시놀로지 NAS에 배포하여 컨테이너가 업데이트되거나 재시작되어도 SQLite 데이터가 유실되지 않도록 외부 볼륨으로 마운트합니다.

### 방법: Container Manager '프로젝트(Compose)'로 배포 (추천)

1. **NAS 공유 폴더 생성**
   - 시놀로지 DSM **File Station** 실행
   - `docker` 공유 폴더 아래에 `travel-english/data` 디렉토리 생성  
     (예: `/volume1/docker/travel-english/data`)

2. **프로젝트 생성**
   - DSM **Container Manager** 실행
   - 좌측 메뉴 **프로젝트** > **생성** 클릭
   - 프로젝트 이름: `travel-english`
   - 경로: `docker/travel-english` 선택
   - 소스: **docker-compose.yml 생성** 선택 후 아래 내용 입력:

```yaml
version: '3.8'

services:
  travel-english:
    image: jaewooo/travel-english:latest
    container_name: travel-english
    ports:
      - "8000:8000"
    volumes:
      # NAS의 실제 절대 경로로 매핑 (볼륨 번호 확인 필요)
      - /volume1/docker/travel-english/data:/app/data
    environment:
      - TZ=Asia/Seoul
      - DB_DIR=/app/data
    restart: unless-stopped
```

3. **완료 및 서비스 시작**
   - 웹 포털 설정은 필요에 따라 역방향 프록시(Reverse Proxy) 또는 DDNS를 연동합니다.
   - 프로젝트가 시작되면 `http://<NAS-IP>:8000` 으로 접속 가능합니다.
   - 학습 진도 및 복습 횟수는 `/volume1/docker/travel-english/data/travel_english.db` 파일에 영구 보존됩니다.

---

## 🔄 GitHub Actions를 통한 Docker Build & Push 자동화

이 프로젝트에는 GitHub Actions를 통해 코드가 푸시되면 자동으로 Docker Hub에 멀티 아키텍처 이미지를 빌드 및 푸시하는 워크플로우가 포함되어 있습니다.  
(`.github/workflows/docker-publish.yml`)

### 1. Docker Hub Access Token 발급

1. [Docker Hub](https://hub.docker.com/) 로그인
2. 우측 상단 프로필 > **Account Settings** 이동
3. 좌측 메뉴 **Security** > **New Access Token** 클릭
4. Token 설명(예: `github-actions-travel-english`) 입력 후 권한을 `Read & Write`로 설정하여 토큰 생성
5. 생성된 토큰 문자열을 복사합니다.

### 2. GitHub Secrets 등록

1. GitHub 저장소 페이지 이동
2. **Settings** > 좌측 메뉴 **Secrets and variables** > **Actions** 클릭
3. **New repository secret** 버튼 클릭 후 아래 2개의 Secret을 등록합니다:

| Secret 이름 | 설명 | 값 예시 |
|---|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub 사용자 계정명 | `jaewooo` |
| `DOCKERHUB_TOKEN` | 위 1단계에서 발급받은 Docker Hub Access Token | `dckr_pat_xxxxxx...` |

### 3. 워크플로우 동작 방식

- **자동 트리거**:
  - `main` 또는 `master` 브랜치에 코드가 `push`될 때: `jaewooo/travel-english:latest` 태그로 자동 빌드 및 푸시
  - 버전 태그(`v1.0.0` 등)가 푸시될 때: 해당 버전 태그명으로 자동 빌드 및 푸시
- **수동 트리거**:
  - GitHub 저장소 **Actions** 탭 > **Build and Push Docker Image** > **Run workflow** 버튼 클릭으로 즉시 수동 실행 가능
- **멀티 아키텍처 지원**:
  - QEMU와 Docker Buildx를 사용하여 `linux/amd64` (일반 PC/서버/NAS) 및 `linux/arm64` (Apple Silicon/Raspberry Pi/ARM 서버) 환경을 모두 지원하는 멀티 플랫폼 이미지를 한 번에 빌드합니다.
