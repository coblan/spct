# encoding:utf-8
from gevent import event,Greenlet
import os
import time

func_list=[]
def run():
    while True:
        for func_item in list(func_list):
            func_item()
        time.sleep(1)

Greenlet(run).start()

def long_link(span=None):
    def inn_func(func):
        if os.environ.get('long_link')=='unblock':
            return func
    
        def _func(*args,**kw):
            ev=event.Event()
            dc={'rt':None}
            before=time.time()
            def __func():
                try:
                    dc['rt']=func(*args,**kw)
                except Exception as e:
                    dc['rt']=e # 将异常扔到外面去运行
                    
                if dc['rt']:
                    ev.set()
                else:
                    after=time.time()
                    if span and after-before > span:
                        ev.set()
                    
            func_list.append(__func)
            ev.wait()
            func_list.remove(__func)
            if isinstance(dc['rt'],Exception):
                raise dc['rt']
            else:
                return dc['rt']
        return _func
    return inn_func