import pika
from django.conf import settings
rabbitHost = settings.RABBITMQ
rabbitPort = settings.RABBITMA_PORT
credentials = pika.PlainCredentials(settings.RAB_USER, settings.RAB_PSWD)


def closeHandicap(msg): 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, port= rabbitPort, credentials = credentials))    
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