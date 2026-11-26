import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()


def send_new_video_notification(video):
    ntfy_server = os.environ["NTFY_SERVER"]
    ntfy_topic = os.environ["NTFY_TOPIC"]

    url = f"{ntfy_server}/{ntfy_topic}"

    published_dt = datetime.fromisoformat(video.published)
    published_text = published_dt.strftime("%d %b %Y, %H:%M")

    response = requests.post(
        url,
        data=f"\n\n{video.title} \n\n {published_text}",
        headers={
            "Title": f"New video from {video.name}".encode(),
            "Attach": video.thumbnail,
            "Action": f"view, Watch, {video.link}",
            "Markdown": "yes",
        },
        timeout=10,
    )

    response.raise_for_status()
    return response.status_code == 200
