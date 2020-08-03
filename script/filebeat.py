from fastdog.maintain.filebeat.dfilebeat import DFileBeat,multi_tail_file,django_log_parsers,elastice_search
from fastdog.maintain.fast_log import set_log
from functools import partial
from settings import ELK
import os

base_dir = os.path.dirname(  os.path.dirname( os.path.abspath(__file__) )  )
log_path = os.path.join( base_dir,'log/filebeat.log')
set_log(log_path)

pp = DFileBeat(harvest= partial(multi_tail_file,
                                   [
                                       os.path.join(base_dir,'log/general_log.log'),
                                       os.path.join(base_dir,'log/errors.log'),
                                   ]),
                  parsers =django_log_parsers,
                  outputs = [
                      partial(elastice_search,ELK.get('host'),ELK.get('username'),ELK.get('password'),ELK.get('index'))
                  ] )
pp.run()