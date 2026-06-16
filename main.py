from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

class ReelRequest(BaseModel):
    video_url: str
    caption: str

@app.get("/")
def root():
    return {"status": "working"}

@app.get("/")
def root():
    return {
        "ig_id": IG_BUSINESS_ID,
        "token_exists": PAGE_ACCESS_TOKEN is not None
    }
