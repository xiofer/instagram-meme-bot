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

@app.post("/publish-reel")
def publish_reel(data: ReelRequest):

    create_url = f"https://graph.facebook.com/v25.0/{IG_BUSINESS_ID}/media"

    create_response = requests.post(
        create_url,
        data={
            "media_type": "REELS",
            "video_url": data.video_url,
            "caption": data.caption,
            "access_token": PAGE_ACCESS_TOKEN
        }
    ).json()

    return create_response
