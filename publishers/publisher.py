import redis
import cv2

cliente_redis = redis.Redis(host="redis",port=6379)
canal = "imagens-mnist"
while True:
    mensagem = cv2.imread("inputs/1.png")
    mensagem = cv2.imencode('.png', mensagem)[1].tobytes()
    cliente_redis.publish(canal,mensagem)
    image_input = input("message:")