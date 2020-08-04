from fastdog.maintain.filebeat.dfilebeat import DFileBeat,multi_tail_file,django_log_parsers
from fastdog.maintain.filebeat.shotcut import ELKHander

from fastdog.maintain.fast_log import set_log
from functools import partial

import os
import sys

base_dir = os.path.dirname(  os.path.dirname( os.path.abspath(__file__) )  )
sys.path.append(os.path.join(base_dir,'src'))

log_path = os.path.join( base_dir,'log/filebeat.log')
set_log(log_path)

# setting  from  src
from settings import ELK

pp = DFileBeat(harvest= partial(multi_tail_file,
                                   [
                                       os.path.join(base_dir,'log/general_log.log'),
                                       os.path.join(base_dir,'log/errors.log'),
                                   ]),
                  parsers =django_log_parsers,
                  outputs = [
                      ELKHander(ELK.get('elastic'),ELK.get('user'),ELK.get('pwsd'),'adminbackend' ),
                      #partial(elastice_output,ELK.get('host'),ELK.get('username'),ELK.get('password'),ELK.get('index'),ELKHander)
                  ] )
pp.run()