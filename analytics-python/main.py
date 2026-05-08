
import os

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from analytics import get_creator_cpm

app = FastAPI()

frontend_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "creatoriq-analytics"}

@app.get("/analytics/cpm/{creator_id}")
def get_cpm(creator_id: str):
    cpm = get_creator_cpm(creator_id)

    if cpm is None:
        raise HTTPException(status_code=404, detail="Creator metrics not found")

    return cpm
