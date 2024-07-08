import redis
from utils.pubsub_utils import get_module_logger

redis_client = redis.Redis(host="redis",port=6379)
channel = 'Prediction'

pubsub = redis_client.pubsub()
pubsub.subscribe(channel)

logger = get_module_logger()

logger.info(f"Subscribed in {channel} Channel")

for message in pubsub.listen():
    logger.info(message)
    if message['type'] == 'message':
        str = message['data']
        logger.info(str)
