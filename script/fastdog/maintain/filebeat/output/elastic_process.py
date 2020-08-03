from . elastic import ELKHander,helpers

def elasticesearch_process(host,user,pswd,index,self,lines):
    if not hasattr(self,'es'):
        self.es = ELKProcess(host,user,pswd,index)
    print('发送elastic search')
    self.es.send(lines)
    
class ELKProcess(ELKHander):
    def make_index(self):
        if self.es.info().get('version').get('number').startswith('7'):
            _index_mappings = {
                "mappings": {
                    "properties": { 
                      "@timestamp":    { "type": "date"  }, 
                      "level":     { "type": "text"  }, 
                      "host": {"type": "text"},
                      "message":      { "type": "text" }, 
                      "path":{"type": "text"},
                      "process":{"type": "text"},
                    }
                }
              }
        else:
            _index_mappings = {
                "mappings": {
                    "_doc":{
                        "properties": { 
                            "@timestamp":    { "type": "date"  }, 
                            "level":     { "type": "text"  }, 
                            "host": {"type": "text"},
                            "message":      { "type": "text" }, 
                            "path":{"type": "text"},
                            "process":{"type": "text"},
                          }
                    }
                }
              }
            
        if self.es.indices.exists(index= self.index ) is not True:
            res = self.es.indices.create(index = self.index, body=_index_mappings) 
    
    def send(self,lines):
        actions=[ ]
        for line in lines:
            actions.append({
                    "_index": self.index,
                    "_type": "_doc",
                    "_source": {
                        "level":line.get('level','NULL'),
                        "host":line.get('host',self.hostName),
                        "message":line.get('message'),
                        '@timestamp':line.get('@timestamp'),
                        "path":line.get('path'),
                        "process":line.get('process'),
                    }
            })
        helpers.bulk(self.es, actions)