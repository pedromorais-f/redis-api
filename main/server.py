import redis
import cv2
import numpy as np
import os
import json
import base64
import asyncio
from utils.pubsub_utils import get_module_logger, preprocess_image, model_prediction, load_model
from mnist import MnistModel


async def main():
    redis_client = redis.Redis(host=os.getenv("REDIS_HOST"),port=6379, password=os.getenv("REDIS_PASSWORD"))
    logger = get_module_logger()

    channels = ["MNIST IMAGES", "Prediction"]


    pubsub = redis_client.pubsub()
    pubsub.subscribe(channels[0])


    logger.info(f"Subscribed in channel: {channels[0]}.")

    model = MnistModel()
    model_loaded = load_model(model)

    async def listen():
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])

                data["image"] = base64.b64decode(data["image"])

                data["image"] = cv2.imdecode(np.frombuffer(data["image"], np.uint8), cv2.IMREAD_COLOR)
                logger.info("Image Decoded!")

                data["image"] = preprocess_image(data["image"])
                logger.info("Image Processed!")
                logger.info("Generating the result...")

                data["Prediction"] = model_prediction(data["image"], model_loaded)

                redis_client.publish(channels[1], f"The Prediction of the image {data['image_name']} that was sent by {data['user']} is {data['Prediction']}")
                logger.info("Prediction published\n")
    await asyncio.create_task(listen())


if __name__ == "__main__":
    asyncio.run(main())