import pika
import json
from django.conf import settings
import logging
general_log = logging.getLogger('general_log')

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

#def notifyHandicapcount(msg):
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    #channel = connection.channel()
    #channel.basic_publish(exchange='center.topic',
                          #routing_key= 'backend.handicapcount.tournament',
                          #body=msg)

def notifyLeagueGroup(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'backend.leaguegroup.tournament',
                          body=msg)

def notifyAccountFrozen(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'backend.account.frozen',
                          body=msg)
    
def notifyScrapyMatch(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'match.multisource',
                          body=msg)

def notifyCreateNewMatch(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='service.topic',
                          routing_key= 'newbetradar.matches',
                          body=msg)
    
    try:
        rabbit_forword_publish(exchange='service.topic',
                              routing_key= 'newbetradar.matches',
                              body=msg)
    except Exception as e:
        general_log.error('新建比赛发送forword消息报错:%s'%str(e))
    
    

def notifyMatchMaping(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='center.topic',
                          routing_key= 'spider.event.mapping',
                          body=msg)
    

def rabbit_forword_publish(exchange,routing_key,body):
    rabbitHost = settings.RABBIT_FORWORD.get('ip')
    rabbitPort = settings.RABBIT_FORWORD.get('port')
    virtual_host= settings.RABBIT_FORWORD.get('virtual_host')
    credentials = pika.PlainCredentials(settings.RABBIT_FORWORD.get('username'), 
                                        settings.RABBIT_FORWORD.get('password'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, 
                                                                   port= rabbitPort, 
                                                                   credentials = credentials,
                                                                   virtual_host=virtual_host))    
    channel = connection.channel()
    channel.basic_publish(exchange=exchange,
                          routing_key= routing_key,
                          body=body)


def notifyMapingSetting(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitHost, credentials = credentials))    
    channel = connection.channel()
    channel.basic_publish(exchange='spider.topic',
                          routing_key= 'spider.source.update',
                          body=msg)