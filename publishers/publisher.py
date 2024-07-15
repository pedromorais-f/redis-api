import redis
import cv2
import time
import json
import base64
import os

redis_client = redis.Redis(host="localhost",port=6379)
channel = "MNIST IMAGES"

user = ""

image_path = "publishers/inputs"
images_names_list = os.listdir(image_path)
print(images_names_list)


for image_input in images_names_list:
    image = cv2.imread(f"{image_path}/{image_input}")
    image = cv2.imencode('.jpg', image)[1].tobytes()
    image = base64.b64encode(image).decode('utf-8')

    message = json.dumps({"image_name": image_input, "image": image, "user": user, "Prediction": None})
    time.sleep(1)
    redis_client.publish(channel, message)
    