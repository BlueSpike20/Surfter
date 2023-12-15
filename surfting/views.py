import pika
from pika.exchange_type import ExchangeType
import uuid
from django.shortcuts import render
from django.http import HttpResponse
from calc.tasks import SurftResults

# Create your views here.

# Global variable to check if the process is running
# is_running = False

# def surfting(request):
#     global is_running

#     if not is_running:
#         is_running = True
#         SurftResults.task_status == 'SUCCESS'

#         connection_parameters = pika.ConnectionParameters('localhost')
#         connection = pika.BlockingConnection(connection_parameters)
#         channel  = connection.channel()

#         reply_queue = channel.queue_declare(queue='', exclusive=True)

#         # Send a message to the server
#         channel.basic_publish(exchange='', routing_key='server_queue', properties=pika.BasicProperties(reply_to=reply_queue.method.queue), body='Surfting')

#         # Wait for the reply
#         while is_running:
#             connection.process_data_events()

#         connection.close()

#         return render(request, 'results.html')
#     else:
#         return HttpResponse('Surfting is already running.')

# def on_reply_message_received(ch, method, properties, body):
#     global is_running

#     print(f"reply received: {body}")

#     # Stop waiting for the reply
#     is_running = False

# connection_parameters = pika.ConnectionParameters('localhost')
# connection = pika.BlockingConnection(connection_parameters)
# channel  = connection.channel()

# reply_queue = channel.queue_declare(queue='', exclusive=True)

# channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True, on_message_callback=on_reply_message_received)

# channel.queue_declare(queue='request_queue')

# message = "RabbitServer, please reply to this message!"

# cor_id = str(uuid.uuid4())

# print(f"RabbitsClient: Sending message: {cor_id}")

# print(f"RabbitsClient starting")
# channel.basic_publish(
#     exchange='', 
#     routing_key='request_queue',
#     properties=pika.BasicProperties(
#         reply_to=reply_queue.method.queue,
#         correlation_id=cor_id), 
#     body=message)

# channel.start_consuming()
