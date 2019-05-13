#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

for i in range(10000):
    channel.basic_publish(exchange='incoming', routing_key=sys.argv[1],body='message of stuff')
print(" [x] Sent 'Hello World!'")
connection.close()
