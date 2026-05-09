import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_to_discord(title, price, url, image):
    data = {
        "embeds": [
            {
                "title": title,
                "url": url,
                "description": f"💰 {price}€",
                "image": {"url": image}
            }
        ]
    }

    requests.post(WEBHOOK, json=data)