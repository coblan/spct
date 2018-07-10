import pika
from django.conf import settings
rabbitHost = settings.RABBITMQ

credentials = pika.PlainCredentials('publisher', 'publisher')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))


def closeHandicap(msg): 
    channel = connection.channel()
    channel.basic_publish(exchange='sportative.topic',
                          routing_key= 'match.closehandicap',
                          body=msg)