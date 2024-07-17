import cv2
import numpy as np
import os
import json
import base64
import redis.asyncio as redis
import asyncio
from utils.pubsub_utils_async import get_module_logger, preprocess_image, model_prediction, load_model
from mnist import MnistModel


async def listen(channel: redis.client.PubSub, model_loaded : MnistModel, logger, redis_client, channels):
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            data = json.loads(message['data'])

            data["image"] = base64.b64decode(data["image"])

            data["image"] = cv2.imdecode(np.frombuffer(data["image"], np.uint8), cv2.IMREAD_COLOR)
            logger.info("Image Decoded!")

            data["image"] = await preprocess_image(data["image"])
            logger.info("Image Processed!")
            logger.info("Generating the result...")

            data["Prediction"] = await model_prediction(data["image"], model_loaded)    
            
            await redis_client.publish(channels[1], f"The Prediction of the image {data['image_name']} that was sent by {data['user']} is {data['Prediction']}")
            logger.info("Prediction published\n")

async def main():
    redis_host = os.getenv("REDIS_HOST")
    password = os.getenv("REDIS_PASSWORD")    
    redis_client = await redis.from_url(f"redis://{redis_host}:6379", password=password)

    pubsub = redis_client.pubsub()
    channels = ["MNIST-IMAGES", "Prediction"]

    await pubsub.subscribe(channels[0])

    logger = get_module_logger()
    logger.info(f"Subscribed in channel: {channels[0]}.")

    model = MnistModel()
    model_loaded = load_model(model)

    await listen(pubsub, model_loaded, logger, redis_client, channels)
    



if __name__ == "__main__":
    asyncio.run(main())