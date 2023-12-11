import pika
from django.shortcuts import render
import time


def on_request_message_received(ch, method, properties, body):
    print(f"RabbitServer received message: {properties.correlation_id}")
    time.sleep(3) # simulate some work
    
    ch.basic_publish('', routing_key=properties.reply_to,
        body=f"RabbitServer sending message to RabbitClient {properties.correlation_id}")
    
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel  = connection.channel()

channel.queue_declare(queue='request_queue')

channel.basic_consume(queue='request_queue', auto_ack=True,
    on_message_callback=on_request_message_received)

print("Starting RabbitSerfter")

channel.start_consuming()