import redis
import logging


def get_module_logger(mod_name):

    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

redis_client = redis.Redis(host="redis",port=6379)
channel = 'Prediction'

pubsub = redis_client.pubsub()
pubsub.subscribe(channel)

get_module_logger(__name__).info(f"Subscribed in {channel} Channel")

for message in pubsub.listen():
    get_module_logger(__name__).info(message)
    if message['type'] == 'message':
        str = message['data']
        get_module_logger(__name__).info(str)
