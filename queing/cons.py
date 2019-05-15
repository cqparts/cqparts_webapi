#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()



def callback(ch, method, properties, body):
    print(" [x] Received ",method,body,properties)
    print(method.routing_key)
    print(method.exchange)
    key = method.routing_key
    ch.queue_declare(queue=key,auto_delete=False,arguments={'x-message-ttl':360000,'x-dead-letter-exchange':'dead-letter'})
    #ch.queue_declare(queue=key,auto_delete=True)
    ch.queue_bind(queue=key,exchange=method.exchange,routing_key=key)
    ch.basic_publish(exchange=method.exchange,routing_key=key,body=body)



channel.basic_consume(queue='sump', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

