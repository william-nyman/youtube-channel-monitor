import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

ntfy_server = os.environ["NTFY_SERVER"]
ntfy_topic = os.environ["NTFY_TOPIC"]

url = f"{ntfy_server}/{ntfy_topic}"

def send_new_video_notification(title, thumbnail, name, published, link):
    published_dt = datetime.fromisoformat(published)
    published_text = published_dt.strftime("%d %b %Y, %H:%M")

    requests.post(
        url,
        data = f"\n{title}\n\nUploaded at {published_text}\n\n{link}",
        headers = {
            "Title": f"New video from {name}",
            "Attach": thumbnail,
            },
            timeout=10,
    )
