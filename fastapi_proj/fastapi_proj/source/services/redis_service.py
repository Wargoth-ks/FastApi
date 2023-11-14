from redis import asyncio as aioredis
from configs import settings
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_redis():
    pool = aioredis.ConnectionPool.from_url(
        f"redis://redis",
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
        encoding="utf-8",
    )
    redis = aioredis.Redis.from_pool(pool)
    try:
        yield redis
    finally:
        await redis.close()

