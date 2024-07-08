import redis
import cv2
import numpy as np
from utils.pubsub_utils import get_module_logger

redis_client = redis.Redis(host="redis",port=6379, db=0)

channels = ["MNIST IMAGES", "Prediction"]

pubsub = redis_client.pubsub()
pubsub.subscribe(channels[0])

logger = get_module_logger()

logger.info(f"inscrito no canal {channels[0]}. aguardando filosofias...")

for message in pubsub.listen():
    logger.info(message)

    if message['type'] == 'message':
        image = message['data']
        imagem_decode = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

        redis_client.publish(channels[1], "Testing")
        logger.info("Prediction published")