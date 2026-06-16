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

    if "id" not in create_response:
        return create_response

    creation_id = create_response["id"]

    publish_url = f"https://graph.facebook.com/v25.0/{IG_BUSINESS_ID}/media_publish"

    publish_response = requests.post(
        publish_url,
        data={
            "creation_id": creation_id,
            "access_token": PAGE_ACCESS_TOKEN
        }
    ).json()

    return {
        "creation_response": create_response,
        "publish_response": publish_response
    }
