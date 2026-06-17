import cloudinary
import cloudinary.uploader
from PIL import Image
from moviepy import ImageClip
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import random

app = FastAPI()

IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

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

    response = requests.get(
        "https://meme-api.com/gimme"
    ).json()

    return {
        "title": response["title"],
        "image_url": response["url"]
    }

@app.get("/cloudinary-test")
def cloudinary_test():

    image_url = "https://picsum.photos/500"

    image_data = requests.get(image_url).content

    with open("test.jpg", "wb") as f:
        f.write(image_data)

    result = cloudinary.uploader.upload(
        "test.jpg"
    )

    return {
        "url": result["secure_url"]
    }
@app.get("/test-video")
def test_video():

    with open("test.txt", "w") as f:
        f.write("hello")

    return {
        "status": "success"
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
    
@app.get("/make-video")
def make_video():

    meme = requests.get(
        "https://meme-api.com/gimme"
    ).json()

    image_url = meme["url"]

    image_data = requests.get(image_url).content

    with open("meme.jpg", "wb") as f:
        f.write(image_data)

    clip = ImageClip("meme.jpg")
    clip = clip.with_duration(5)

    clip.write_videofile(
        "meme.mp4",
        fps=24
    )

    return {
        "title": meme["title"],
        "image_url": image_url,
        "video_created": True,
        "video_file": "meme.mp4"
    }
