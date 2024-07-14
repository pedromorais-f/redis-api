import redis
import cv2
import numpy as np
import os
from utils.pubsub_utils import get_module_logger, preprocess_image, model_prediction, load_model
from mnist import MnistModel


def main():
    redis_client = redis.Redis(host=os.getenv("REDIS_HOST"),port=os.getenv("REDIS_PORT"))
    logger = get_module_logger()

    channels = ["MNIST IMAGES", "Prediction"]

    pubsub = redis_client.pubsub()
    pubsub.subscribe(channels[0])


    logger.info(f"Subscribed in channel: {channels[0]}.")

    model = MnistModel()
    model_loaded = load_model(model)

    for idx, message in enumerate(pubsub.listen()):
        if message['type'] == 'message':
            logger.info(f"Image {idx} Received")
            image = message['data']
            image_decode = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
            logger.info("Image Decoded!")

            image_processed = preprocess_image(image_decode)
            logger.info("Image Processed!")
            logger.info("Generating the result...")

            result = model_prediction(image_processed, model_loaded)

            redis_client.publish(channels[1], f"The Prediction of your image:{result}")
            logger.info("Prediction published\n")


if __name__ == "__main__":
    main()