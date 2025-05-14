import os

import json

from datetime import datetime

from uuid import uuid4

from dateutil import parser


SRC_DIR = "scraped_data"

DST_DIR = "normalized"



os.makedirs(DST_DIR, exist_ok=True)



def normalize(tweet):

    return {

        "id": str(uuid4()),

        "source": "twitter",

	"timestamp": parser.parse(tweet["timestamp"]).isoformat(),

        "content": tweet.get("full_text") or tweet.get("text"),

        "user": tweet["user"]["screen_name"] if "user" in tweet else "unknown",

        "media_urls": [],

        "metadata": {

            "lang": tweet.get("lang", "und"),

            "retweet_count": tweet.get("retweet_count", 0),

            "favorite_count": tweet.get("favorite_count", 0),

        }

    }



def main():

    for fname in os.listdir(SRC_DIR):

        if not fname.endswith(".jsonl"):

            continue

        src_path = os.path.join(SRC_DIR, fname)

        with open(src_path, "r", encoding="utf-8") as f:

            lines = f.readlines()



        for line in lines:

            try:

                tweet = json.loads(line)

                entity = normalize(tweet)

                out_path = os.path.join(DST_DIR, f"{entity['id']}.json")

                with open(out_path, "w", encoding="utf-8") as out:

                    json.dump(entity, out, ensure_ascii=False, indent=2)

            except Exception as e:

                print(f"[!] Ошибка в файле {fname}: {e}")



if __name__ == "__main__":

    main()

