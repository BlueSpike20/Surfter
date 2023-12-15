import pika
from pika.exchange_type import ExchangeType
import uuid


def on_reply_message_received(ch, method, properties, body):
    print(f"reply received: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel  = connection.channel()

reply_queue = channel.queue_declare(queue='', exclusive=True)
#channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True,
    on_message_callback=on_reply_message_received)

channel.queue_declare(queue='request_queue')

message = "RabbitServer, please reply to this message!"

cor_id = str(uuid.uuid4())

print(f"RabbitsClient: Sending message: {cor_id}")

print(f"RabbitsClient starting")
channel.basic_publish(
    exchange='', 
    routing_key='request_queue',
    properties=pika.BasicProperties(
        reply_to=reply_queue.method.queue,
        correlation_id=cor_id), 
    body=message)

channel.start_consuming()
