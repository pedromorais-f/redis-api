import redis

cliente_redis = redis.StrictRedis(host="localhost",port=6379,db=0)
canal = 'nicolas gameplays'
pubsub = cliente_redis.pubsub()
pubsub.subscribe(canal)
print(f"inscrito no canal {canal}. aguardando filosofias...")
for mensagem in pubsub.listen():
    if mensagem['type'] == 'message':
        print(f"nicolas postou: {mensagem['data'].decode('utf-8')}")