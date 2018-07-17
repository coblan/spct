from elasticsearch import Elasticsearch
import logging
import socket
import datetime
import json
import logging
log = logging.getLogger('extra.error')


hostName = socket.gethostname()

es = Elasticsearch('http://192.168.40.137:9200')

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

#res = es.index('adminBackend', 'user', body = {'title': 'jjj', 'name': 'ppp', 'age': 18,})
#print(res)

class EsHandler(logging.Handler):
    #def __init__(self, level=NOTSET): 
        #self.
    
    def emit(self, record): 
        msg =   record.getMessage()
        if record.levelname == 'ERROR':
            msg += '\n' + record.exc_text
        dc = {
            '@timestamp': datetime.datetime.utcnow(),
            'level': record.levelname,
            'host': hostName,
            'message': msg
        }
        try:
            res = es.index('adminbackend', 'user', body = dc)
            #print(res)
        except Exception as e:
            log.error('请求adminbackend出现了问题,%s' % e)
        
        #print(record)
    


