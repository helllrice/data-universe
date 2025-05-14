import sys

import os

sys.path.append(os.path.abspath("."))

import asyncio


import json

from tqdm import tqdm

from common.data import DataEntity  # если он в common/data.py

from dynamic_desirability.config import get_config

from dynamic_desirability.desirability_retrieval import run_retrieval



SRC_DIR = "normalized"

DST_DIR = "weighted"

THRESHOLD = 0.1



os.makedirs(DST_DIR, exist_ok=True)



# 1. Загрузим DataEntity

entities = []

for fname in os.listdir(SRC_DIR):

    if not fname.endswith(".json"):

        continue



    path = os.path.join(SRC_DIR, fname)

    try:

        with open(path, "r", encoding="utf-8") as f:

            data = json.load(f)

            entity = DataEntity(**data)

            entities.append(entity)

    except Exception as e:

        print(f"⚠️ Ошибка в {fname}: {e}")



print(f"📦 Загружено сущностей: {len(entities)}")



# 2. Получим desirability веса

print("🔁 Получаем desirability weights...")

config = get_config()

lookup = asyncio.run(run_retrieval(config))



# 3. Применим веса

print("⚖️ Применяем веса...")

weighted = []

for entity in entities:

    desirability = lookup.get_weight(entity)

    if desirability is None:

        continue

    if desirability >= THRESHOLD:

        entity.desirability_weight = desirability

        weighted.append(entity)





# 4. Сохраним результат

print(f"💾 Сохраняем {len(weighted)} сущностей в {DST_DIR}/")

for entity in tqdm(weighted):

    uid = entity.id

    with open(os.path.join(DST_DIR, f"{uid}.json"), "w", encoding="utf-8") as f:

        json.dump(entity.dict(), f, ensure_ascii=False, indent=2)



print("✅ Завершено.")


