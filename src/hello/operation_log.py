
import logging
import socket
import datetime
from django.conf import settings
from helpers.director.middleware.request_cache import get_request_cache

import json

dc = {
}

class DBOperationHandler(logging.Handler):

    def emit(self, record): 
        global dc
        if not dc.get('TbOperationlog'):
            from maindb.models import TbOperationlog
            dc['TbOperationlog'] = TbOperationlog
        TbOperationlog = dc['TbOperationlog']
        
        msg =   record.getMessage()
        if record.levelname == 'ERROR':
            msg += '\n' + record.exc_text
        
        user = get_request_cache().get('request').user
        user_label = user.username if user.is_authenticated else '【匿名用户】'
        
        try:
            db_op_dict = json.loads(msg)
            content = db_op_dict.pop('content', None)
            if not content:
                content = pop_content(db_op_dict, user)
            type_key = db_op_dict.pop('model', '')
            memo = db_op_dict.get('memo', '')
        except json.decoder.JSONDecodeError:
            type_key = '_direct_message'
            memo = ''
            content = msg
        TbOperationlog.objects.create(createuser = user_label,
                                      type = type_key, 
                                      content = content, 
                                      memo = memo)
                                      #createtime = datetime.datetime.now())

def pop_content(dc, user): 
    after = dc.pop('_after', {})
    after.update( dc.pop('after', {}) )
    model = dc.get('model', 'NULL')
    pk = dc.pop('pk', 'NULL')
    if after:
        before = dc.pop('_before', {})
        before.update( dc.pop('before', {}) )
        
        before_str =  ';'.join( ['%s=%s' % (k, v) for (k, v) in before.items()])
        after_str = ';'.join( ['%s=%s' % (k, v) for (k, v) in after.items()])
        str_kws =  {
            'user': user,
            'pk': pk,
            'model': model,
            'before_str': before_str,
            'after_str': after_str,
        }
        if dc.get('kind') == 'add':
            content = '%(user)s创建了主键为%(pk)s的%(model)s,值为%(after_str)s' % str_kws
        elif before_str:
            content = '%(user)s将主键为%(pk)s的%(model)s,从%(before_str)s,修改为%(after_str)s' % str_kws
        else:
            content = '%(user)s将主键为%(pk)s的%(model)s,修改为%(after_str)s' % str_kws
            
    else:
        content = json.dumps(dc)
    return content

        
        

    




