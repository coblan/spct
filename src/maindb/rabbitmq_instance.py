import pika
from django.conf import settings
rabbitHost = settings.RABBITMQ

credentials = pika.PlainCredentials('publisher', 'publisher')


def closeHandicap(msg): 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'match.closehandicap',
                          body=msg)

def updateSpread(msg): 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'sportative.spread',
                          body=msg)