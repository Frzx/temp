from redis.asyncio import Redis
from redis.exceptions import ResponseError

def create_connection(redis_url: str):
    return Redis.from_url(redis_url, decode_responses=True)

async def close_redis_client(redis_client: Redis):
    await redis_client.aclose()

async def create_stream_consumer_group(
    redis_client: Redis,
    *,
    stream_name: str,
    group_name: str
) -> None:
    try:
        await redis_client.xgroup_create(
            name=stream_name,
            groupname = group_name,
            id="0",
            mkstream=True
        )
    except ResponseError as error:
        if "BUSYGROUP" not in str(error):
            raise


async def publish_event(redis_client: Redis,*, stream_name, event_json: str) -> str:
    return await redis_client.xadd(stream_name, {"event": event_json})

async def acknowledge_message(redis_client: Redis,*, stream_name: str, group_name: str, message_id: str) -> None:
    await redis_client.xack(stream_name, group_name, message_id)