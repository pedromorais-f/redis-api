import redis

cliente_redis = redis.Redis(host="redis",port=6379,db=0)
canal = 'Prediction'
pubsub = cliente_redis.pubsub()
pubsub.subscribe(canal)
print(f"inscrito no canal {canal}. aguardando filosofias...")
for mensagem in pubsub.listen():
    print(mensagem)
    if mensagem['type'] == 'message':
        str = mensagem['data']
        print(str)
