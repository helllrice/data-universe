import asyncio

from twikit import Client

import json

from datetime import datetime

import uuid

import os



# Настройки

SCREEN_NAME = "elonmusk"

COOKIES_PATH = "twitter_cookies.json"

OUTPUT_DIR = "scraped_data"



async def main():

    client = Client()

    client.load_cookies(COOKIES_PATH)



    user = await client.get_user_by_screen_name(SCREEN_NAME)

    tweets = await user.get_tweets(tweet_type="Tweets", count=10)



    os.makedirs(OUTPUT_DIR, exist_ok=True)

    index_entries = []



    for tweet in tweets:

        uid = str(uuid.uuid4())

        data = {

            "id": uid,

            "text": tweet.full_text,

            "timestamp": tweet.created_at,

            "author": SCREEN_NAME,

            "source": "twitter"

        }



        file_path = os.path.join(OUTPUT_DIR, f"{uid}.jsonl")

        with open(file_path, "w", encoding="utf-8") as f:

            f.write(json.dumps(data, ensure_ascii=False) + "\n")



        index_entries.append({

            "id": uid,

            "file_name": os.path.basename(file_path),

            "timestamp": data["timestamp"]

        })



    index_path = os.path.join(OUTPUT_DIR, "index.json")

    with open(index_path, "w", encoding="utf-8") as f:

        json.dump(index_entries, f, indent=2, ensure_ascii=False)



    print(f"✅ Скрапинг завершён. Сохранено {len(tweets)} твитов в папку {OUTPUT_DIR}")



# Запуск

asyncio.run(main())



