import redis
import cv2
import numpy as np

cliente_redis = redis.StrictRedis(host="localhost",port=6379,db=0)
canal = 'nicolas gameplays'
pubsub = cliente_redis.pubsub()
pubsub.subscribe(canal)
print(f"inscrito no canal {canal}. aguardando filosofias...")
for mensagem in pubsub.listen():
    if mensagem['type'] == 'message':
        image = mensagem['data']
        imagem_decode = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("Imagem", imagem_decode)
        cv2.waitKey(0)