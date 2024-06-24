import redis

cliente_redis = redis.StrictRedis(host="localhost",port=6379,db=0)
canal = "nicolas gameplays"
while True:
    mensagem = input("Enter a message: ")
    cliente_redis.publish(canal,mensagem)