from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import random

app = FastAPI()

IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")


class ReelRequest(BaseModel):
    video_url: str
    caption: str


class PublishRequest(BaseModel):
    creation_id: str


@app.get("/")
def root():
    return {"status": "working"}


@app.get("/get-meme")
def get_meme():

    url = "https://www.reddit.com/r/memes/top.json?t=day&limit=25"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    return {
        "status_code": response.status_code,
        "text": response.text[:500]
    }

@app.post("/create-reel")
def create_reel(data: ReelRequest):

    create_url = f"https://graph.facebook.com/v25.0/{IG_BUSINESS_ID}/media"

    response = requests.post(
        create_url,
        data={
            "media_type": "REELS",
            "video_url": data.video_url,
            "caption": data.caption,
            "access_token": PAGE_ACCESS_TOKEN
        }
    ).json()

    return response


@app.post("/publish-reel")
def publish_reel(data: PublishRequest):

    publish_url = f"https://graph.facebook.com/v25.0/{IG_BUSINESS_ID}/media_publish"

    response = requests.post(
        publish_url,
        data={
            "creation_id": data.creation_id,
            "access_token": PAGE_ACCESS_TOKEN
        }
    ).json()

    return response
