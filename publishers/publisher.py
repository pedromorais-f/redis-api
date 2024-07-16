import redis
import cv2
import json
import base64
import os

redis_client = redis.Redis(host=os.getenv("REDIS_HOST"),port=6379, password=os.getenv("REDIS_PASSWORD"))
channel = "MNIST IMAGES"

user = os.getenv("USER")

image_path = "publishers/inputs"
images_names_list = os.listdir(image_path)

print(images_names_list)
while True:
    image_input = input("Write IMAGE_NAME:")

    image = cv2.imread(f"{image_path}/{image_input}")
    image = cv2.imencode('.jpg', image)[1].tobytes()
    image = base64.b64encode(image).decode('utf-8')

    message = json.dumps({"image_name": image_input, "image": image, "user": user, "Prediction": None})
    redis_client.publish(channel, message)
    