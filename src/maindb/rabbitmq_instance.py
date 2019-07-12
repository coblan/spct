import pika
import json
from django.conf import settings
rabbitHost = settings.RABBITMQ
rabbitPort = settings.RABBITMA_PORT
credentials = pika.PlainCredentials(settings.RAB_USER, settings.RAB_PSWD)


def closeHandicap(msg): 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, port= rabbitPort, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'backend.close.markethcp',
                          body=msg)

def updateSpread(msg): 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'sportative.spread',
                          body=msg)

def notifyWithdraw(accountid, orderid): 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'user.withdraw',
                          body= json.dumps({'accountid': accountid, 'orderid': orderid,}))   

def notifyManulOutcome(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'backend.betclear',
                          body=msg)

def notifyMatchRecommond(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'backend.recommend.match',
                          body=msg)
    
def notifyAdjustOddsBase(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'backend.adjust.odds',
                          body=msg)

def notifyAccountFrozen(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'backend.account.frozen',
                          body=msg)