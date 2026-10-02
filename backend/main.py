from fastapi import FastAPI
from database import init_db

app = FastAPI(title="버스 도착 알리미")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}
