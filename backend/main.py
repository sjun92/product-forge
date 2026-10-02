from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from auth.router import router as auth_router
from favorites.router import router as favorites_router

app = FastAPI(title="버스 도착 알리미")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(auth_router)
app.include_router(favorites_router)

@app.get("/health")
def health():
    return {"status": "ok"}
