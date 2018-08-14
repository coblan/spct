from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .redisInstance import redisInst
from .models import TbCurrency, TbNotice, TbBanner, TbMatches

dc = {
    TbCurrency: 'App:Static:Currency',
    TbNotice: 'App:Cache:index:notices',
    TbBanner: 'App:Cache:index:banners',
    TbMatches: 'App:Cache:index:matches',
    
}


def update_redis_cache(sender, **kws): 
    if sender in dc:
        redisInst.delete(dc.get(sender))  
        

post_delete.connect(update_redis_cache)
post_save.connect(update_redis_cache)