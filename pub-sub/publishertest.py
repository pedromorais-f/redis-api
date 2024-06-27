import redis
import cv2
import numpy as np

cliente_redis = redis.StrictRedis(host="localhost",port=6379,db=0)
canal = "imagens-mnist"
while True:
    mensagem = cv2.imread("")
    mensagem = cv2.imencode('.png', mensagem)[1].tostring()
    cliente_redis.publish(canal,mensagem)