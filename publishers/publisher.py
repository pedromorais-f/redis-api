import redis
import cv2
import time

redis_client = redis.Redis(host="localhost",port=6379)
channel = "MNIST IMAGES"

image_path = "publishers/inputs"

while True:
    image_input = input("Image:")

    message = cv2.imread(f"{image_path}/{image_input}")
    message = cv2.imencode('.jpg', message)[1].tobytes()
    time.sleep(2)
    redis_client.publish(channel, message)
    