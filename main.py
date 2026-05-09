import time
import random
from vinted import search_items
from discord_webhook import send_to_discord

seen = set()

print("Bot a correr...")

while True:
    try:
        items = search_items()

        for item in items:
            if item["id"] not in seen:
                seen.add(item["id"])

                send_to_discord(
                    item["title"],
                    item["price"],
                    item["url"],
                    item["image"]
                )

        time.sleep(random.randint(50, 80))

    except Exception as e:
        print("Erro:", e)
        time.sleep(30)