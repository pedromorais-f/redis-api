import redis
import cv2

redis_client = redis.Redis(host="localhost",port=6379)
channel = "MNIST IMAGES"

while True:
    image_file = input("Image:")
    message = cv2.imread(f"inputs/{image_file}")
    message = cv2.imencode('.png', message)[1].tobytes()
    redis_client.publish(channel, message)