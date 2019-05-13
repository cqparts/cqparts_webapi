#!/usr/bin/env python
import pika
import sys
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost',heartbeat=0)
)
channel = connection.channel()



def callback(ch, method, properties, body):
    time.sleep(0.01)
    #print(ch,method,properties,body)
    channel.basic_ack(method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=sys.argv[1], on_message_callback=callback)

channel.start_consuming()

