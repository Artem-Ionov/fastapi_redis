import json
from datetime import datetime, time

import redis.asyncio as redis

from config import REDIS_HOST, REDIS_PORT


class RedisCache:
    def __init__(self):
        # Подключаемся к серверу Redis
        self.redis = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=True
        )

    async def get(self, key: str):
        """Получить данные из кэша по ключу"""
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value, ttl: int):
        """Сохранить в кэш по ключу с временем жизни time-to-leave"""
        await self.redis.set(key, json.dumps(value), ex=ttl)

    async def get_ttl(self) -> int:
        """Расчёт времени жизни ключа time-to-leave"""
        now = datetime.now()
        target_time = datetime.combine(now.date(), time(14, 11))
        if now.time() > time(14, 11):
            target_time = target_time.replace(day=target_time.day + 1)
        return int((target_time - now).total_seconds())
