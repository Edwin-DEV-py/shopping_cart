import os
import django
#obtener las configuraciones del settings para poder ejecutar este archivo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cart.settings')
django.setup()


import pika, json
from CartApp.models import CartItem

#conectar con cloudAMQP
params = pika.URLParameters('amqps://rlvgzuul:IR8L9U8f_vzjLAF0P4gtt9ALoMC4Q8W7@jaragua.lmq.cloudamqp.com/rlvgzuul')
connection = pika.BlockingConnection(params)
channel = connection.channel()
print('conectado')
#definir el canal
channel.queue_declare(queue='carrito',durable=True)#anadir durable=True para que los mensaje lleguen a pesar de que este apagado
#implementa el protocolo de mensajeria AMQP para declarar una cola.
#una cola es un destino donde los productores envian mensajes y los consumidores reciben. este protocolo crea una cola.

#funcion para saber que obtuvo los datos
def callback(ch, method,properties, body):
    print('resibido en vista')
    
    data = json.loads(body)
    
    if properties.content_type == 'vaciar_carrito':
        user = data
        nombre = CartItem.objects.filter(user=user).delete()
        
        
channel.basic_consume(queue='carrito', on_message_callback=callback, auto_ack=True)

print('consumiendo')


channel.start_consuming()

channel.close()
        
            