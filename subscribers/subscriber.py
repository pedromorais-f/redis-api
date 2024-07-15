import redis
from utils.pubsub_utils import get_module_logger
import os
import asyncio

async def main():    
    redis_client = redis.Redis(host=os.getenv("REDIS_HOST"),port=6379, password=os.getenv("REDIS_PASSWORD"))
    channel = 'Prediction'

    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)

    logger = get_module_logger()

    logger.info(f"Subscribed in {channel} Channel")

    async def listen():
        for message in pubsub.listen():
            if message['type'] == 'message':
                prediction = message['data']
                logger.info(f"{prediction}\n")
    await asyncio.create_task(listen())


if __name__ == "__main__":
    asyncio.run(main())
