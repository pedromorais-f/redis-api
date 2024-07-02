import redis
import cv2
import numpy as np
import logging

def get_module_logger(mod_name):

    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

cliente_redis = redis.Redis(host="redis",port=6379)

channels = ["MNIST IMAGES", "Prediction"]

pubsub = cliente_redis.pubsub()
pubsub.subscribe(channels[0])

get_module_logger(__name__).info(f"inscrito no canal {channels[0]}. aguardando filosofias...")

for message in pubsub.listen():
    get_module_logger(__name__).info(message)

    if message['type'] == 'message':
        image = message['data']
        imagem_decode = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

        cliente_redis.publish(channels[1], "Testing")
        get_module_logger(__name__).info("Prediction published")