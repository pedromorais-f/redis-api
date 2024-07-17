import redis.asyncio as redis
import os
import asyncio
from utils.pubsub_utils_async import get_module_logger


async def main():
    redis_host = os.getenv("REDIS_HOST")
    password = os.getenv("REDIS_PASSWORD")    
    redis_client = await redis.from_url(f"redis://{redis_host}:6379", password=password)
    channel = 'Prediction'

    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)

    logger = get_module_logger()

    logger.info(f"Subscribed in {channel} Channel")

    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message is not None:
            prediction = message["data"]
            logger.info(f"{prediction}\n")    


if __name__ == "__main__":
    asyncio.run(main())
