import redis.asyncio as redis
import cv2
import json
import base64
import os
import asyncio


async def main():
    redis_host = os.getenv("REDIS_HOST")
    password = os.getenv("REDIS_PASSWORD")    
    redis_client = await redis.from_url(f"redis://{redis_host}:6379", password=password)
    channel = "MNIST-IMAGES"

    user = os.getenv("USER")

    image_path = "publishers/inputs"
    images_names_list = os.listdir(image_path)

    print(images_names_list)
    
    while True:
        image_input = input("IMAGE NAME:")

        image = cv2.imread(f"{image_path}/{image_input}")
        image = cv2.imencode('.jpg', image)[1].tobytes()
        image = base64.b64encode(image).decode('utf-8')

        message = json.dumps({"image_name": image_input, "image": image, "user": user, "Prediction": None})
        await redis_client.publish(channel, message)

if __name__ == "__main__":
    asyncio.run(main())
    