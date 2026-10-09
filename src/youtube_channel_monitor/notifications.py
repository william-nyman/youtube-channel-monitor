import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()


def send_new_video_notification(title, thumbnail, name, published, link):
    ntfy_server = os.environ["NTFY_SERVER"]
    ntfy_topic = os.environ["NTFY_TOPIC"]

    url = f"{ntfy_server}/{ntfy_topic}"

    published_dt = datetime.fromisoformat(published)
    published_text = published_dt.strftime("%d %b %Y, %H:%M")

    requests.post(
        url,
        data = f"\n\n{title} \n\n {published_text}",
        headers = {
            "Title": f"New video from {name}",
            "Attach": thumbnail,
            "Action": f"view, Watch, {link}",
            "Markdown": "yes",
            },
            timeout=10,
    )
