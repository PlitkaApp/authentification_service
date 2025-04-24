from redis.asyncio import Redis, ConnectionPool
from app.config import get_redis_url

pool = ConnectionPool.from_url(
    get_redis_url(),
    max_connections=10
)

async def connection_try():
    async with Redis.from_pool(pool) as blacklist:
        await blacklist.set('async_key', 'Async works!')
        value = await blacklist.get('async_key')
        print(value)


async def add_access_token_to_blacklist(user_id: str, token: str) -> bool:
    async with Redis.from_pool(pool) as blacklist:
        try:
            added = await blacklist.sadd(f"user:{user_id}:tokens_set", token)
            await blacklist.expire(f"user:{user_id}:tokens_set", 15*60)
            return added > 0
        except Exception as e:
            return False

async def add_refresh_token_to_blacklist(user_id: str, token: str) -> bool:
    async with Redis.from_pool(pool) as blacklist:
        try:
            added = await blacklist.sadd(f"user:{user_id}:tokens_set", token)
            await blacklist.expire(f"user:{user_id}:tokens_set", 15*60*4*24*30)
            return added > 0
        except Exception as e:
            return False


async def token_in_blacklist(user_id: str, token: str) -> bool:
        async with Redis.from_pool(pool) as blacklist:
            result = await blacklist.sismember(f"user:{user_id}:tokens_set", token)
            return result > 0

