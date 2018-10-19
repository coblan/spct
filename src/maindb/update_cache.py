from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .redisInstance import redisInst
#from .models import TbCurrency, TbNotice, TbBanner, TbMatches, TbOddstypegroup
from . import models as sports_model
from helpers.func.sim_signal import sim_signal
#dc = {
    #TbCurrency: 'App:Static:Currency',
    #TbNotice: 'App:Cache:index:notices',
    #TbBanner: 'App:Cache:index:banners',
    #TbMatches: 'App:Cache:index:matches',
    #TbOddstypegroup: 'App:Static:TypeGroup',
#}

# 利用django的model的signal进行缓存清空
def update_redis_cache(sender, **kws): 
    
    if sender == sports_model.TbBanner:
        redisInst.delete('App:Cache:index:banners')
    elif sender == sports_model.TbMatches:
        redisInst.delete('App:Cache:index:matches')
    #elif sender == sports_model.TbNotice:
        #redisInst.delete('App:Cache:index:notices')
    elif sender == sports_model.TbMaxpayout:
        for key in  ['App:Static:MaxPayout', 'App:Static:MaxSinglePayout']:
            redisInst.delete(key)
    elif sender == sports_model.TbOddstypes:
        redisInst.delete('App:Static:OddsType')
    elif sender == sports_model.TbOddstypegroup:
        redisInst.delete('App:Static:TypeGroup')
    elif sender == sports_model.Blackiprangelist:
        redisInst.delete('App:BlackList:*')
    #if sender.__module__ == 'maindb.models' :  #in sports_model:
        #ls1 = redisInst.keys(pattern='App:Cache:index:*')
        #if ls1:
            #redisInst.delete(*ls1)
        #ls2 = redisInst.keys(pattern='App:Static:*')
        #if ls2:
            #redisInst.delete(*ls2)
        
        #redisInst.delete('App:Cache:index:*')
        #redisInst.delete('App:Static:*')
    #if sender in dc:
        #redisInst.delete(dc.get(sender))  
        
post_delete.connect(update_redis_cache)
post_save.connect(update_redis_cache)

@sim_signal.recieve('notice.static.changed')
def clear_notice_cache(): 
    redisInst.delete('App:Cache:index:notices')

@sim_signal.recieve('help.static.changed')
def clear_help_cache(): 
    pass