# 버스 도착 알리미

서울·경기 버스 실시간 도착 정보를 확인하고, 즐겨찾기 정류장을 관리하는 웹 애플리케이션입니다.  
Google OAuth 로그인 후 관리자 승인을 받은 사용자만 접근할 수 있습니다.

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| 백엔드 | Python 3.11+, FastAPI, SQLAlchemy, SQLite |
| 인증 | Google OAuth 2.0, JWT |
| 프론트엔드 | React 18, Vite, React Router, Axios, @dnd-kit |
| 외부 API | 서울시 버스 API, 경기도 버스 API |

---

## 주요 기능

- **Google 소셜 로그인** — OAuth 2.0 코드 플로우, JWT 세션 관리
- **버스 정류장 검색** — 서울·경기 통합 검색
- **실시간 도착 정보** — 선택한 정류장의 버스 도착 예정 시간 조회
- **즐겨찾기** — 정류장 등록·삭제, 드래그로 순서 변경(dnd-kit)
- **관리자 패널** — 가입 승인 대기 사용자 승인/거부

---

## 시작하기

### 사전 요구사항

- Python 3.11 이상
- Node.js 20 이상
- Google Cloud Console 프로젝트 (OAuth 클라이언트 ID/Secret)
- 서울시 버스 API 키 및 경기도 버스 API 키

### 1. 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성합니다.

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
JWT_SECRET=your_jwt_secret_key
JWT_EXPIRE_HOURS=24
FIRST_ADMIN_EMAIL=admin@example.com
SEOUL_BUS_API_KEY=your_seoul_bus_api_key
GYEONGGI_BUS_API_KEY=your_gyeonggi_bus_api_key
DATABASE_URL=sqlite:///./bus_arrival.db
```

`FIRST_ADMIN_EMAIL`에 지정된 이메일로 처음 로그인하면 자동으로 관리자 권한이 부여됩니다.

### 2. 백엔드 실행

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

서버가 `http://localhost:8000` 에서 실행됩니다.  
API 문서: `http://localhost:8000/docs`

### 3. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

앱이 `http://localhost:5173` 에서 실행됩니다.

---

## 프로젝트 구조

```
product-forge/
├── backend/
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py            # 환경변수 설정 (pydantic-settings)
│   ├── database.py          # DB 초기화 및 세션
│   ├── models.py            # SQLAlchemy 모델
│   ├── auth/                # Google OAuth, JWT 발급
│   ├── arrivals/            # 버스 도착 정보 조회
│   ├── favorites/           # 즐겨찾기 CRUD
│   ├── search/              # 정류장 검색
│   ├── admin/               # 사용자 승인 관리
│   └── tests/               # pytest 테스트
└── frontend/
    └── src/
        ├── App.jsx           # 라우팅 및 보호 라우트
        ├── contexts/         # AuthContext (사용자 상태)
        ├── pages/            # Login, Dashboard, Search, Admin, Pending
        └── api/              # Axios 클라이언트
```

---

## 테스트

```bash
cd backend
pytest
```

---

## 사용자 플로우

1. `/login` — Google 계정으로 로그인
2. 최초 로그인 시 승인 대기 상태(`/pending`)로 이동
3. 관리자가 `/admin` 패널에서 승인
4. 승인 후 대시보드(`/`) 접근 가능 — 즐겨찾기 정류장 확인 및 실시간 도착 정보 조회
5. `/search` 에서 새 정류장 검색 후 즐겨찾기 추가
