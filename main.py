from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ReelRequest(BaseModel):
image_url: str
caption: str

@app.get("/")
def root():
return {"status": "working"}

@app.post("/create-reel")
def create_reel(data: ReelRequest):
return {
"status": "success",
"image_url": data.image_url,
"caption": data.caption
}
