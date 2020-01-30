from elasticsearch import Elasticsearch
import logging
import socket
import datetime
from django.conf import settings

import logging
log = logging.getLogger('general_log')


hostName = socket.gethostname()

es = Elasticsearch(settings.ELK.get('elastic'),http_auth=(settings.ELK.get('user'),settings.ELK.get('pwsd') ),)

_index_mappings = {
  "mappings": {
    "user": { 
      "properties": { 
        "@timestamp":    { "type": "date"  }, 
        "level":     { "type": "text"  }, 
        "host": {"type": "text"},
        "message":      { "type": "text" }, 
      }
    }

  }
}

if es.indices.exists(index='adminbackend') is not True:
    res = es.indices.create(index='adminbackend', body=_index_mappings) 
    print(res)


#######################################################
# 异步代码
import asyncio
from elasticsearch_async import AsyncElasticsearch

client = AsyncElasticsearch(hosts=[settings.ELK.get('elastic')],http_auth=(settings.ELK.get('user'),settings.ELK.get('pwsd') ))

async def es_save(dc):
    try:
        info = await client.index('adminbackend', 'user', body = dc)
        print(info)
    except Exception as e:
        log.error('[异步]请求adminbackend出现了问题,%s' % e)
    

#loop = asyncio.get_event_loop()
#loop.run_until_complete(print_info())

###############################################################

class EsHandler(logging.Handler):
    #def __init__(self, level=NOTSET): 
        #self.
    
    def emit(self, record): 
        msg =   record.getMessage()
        if record.levelname == 'ERROR':
            if record.exc_text:
                msg += '\n' + record.exc_text
        dc = {
            '@timestamp': datetime.datetime.utcnow(),
            'level': record.levelname,
            'host': hostName,
            'message': msg
        }
        try:
            #res = es.index('adminbackend', 'user', body = dc)
            #print(res)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(es_save(dc))
            loop.run_until_complete(client.transport.close())
            loop.close()
        except Exception as e:
            log.error('请求adminbackend出现了问题,%s' % e)
    




