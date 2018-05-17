# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import TablePage,ModelTable,page_dc,RowSort,director,RowFilter,field_map,BaseFieldProc,model_to_name
from ..models import TbChannel,TbChargeflow
from django.db.models.aggregates import Count,Sum
from django.utils import timezone


class ReportChnnel(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return '渠道报表'
    
    class tableCls(ModelTable):
        model=TbChargeflow
        exclude=[]
        
        @classmethod
        def clean_search_args(cls,search_args):
            today = timezone.now()
            sp = timezone.timedelta(days=30)
            last = today-sp
            def_start = last.strftime('%Y-%m-%d')
            def_end=today.strftime('%Y-%m-%d')
            search_args['_start_createtime'] =search_args.get('_start_createtime',def_start)
            search_args['_end_createtime'] =search_args.get('_end_createtime',def_end)
            return search_args
        
        def get_heads(self):
            heads = [{'name':'createdate','label':'日期','width':120}]
            for channel in TbChannel.objects.all():
                heads.append({
                    'name':channel.channel,
                    'label':channel.channelname,
                    'width':60,
                })
            return heads
        
        def get_rows(self):
            "{'money': 3, u'createdate': u'2018-05-15', u'channel': 13}"
            rows = ModelTable.get_rows(self)
            dc={}
            out_rows=[]
            for row in rows:
                date = row.get('createdate')
                if date not in dc:
                    new_row = {'createdate':row['createdate'],row['channel']:row['money']}
                    dc[date] = new_row
                    out_rows.append(new_row)
                else:
                    dc[date][row['channel']] = row['money']
            return out_rows
        
        def permited_fields(self):
            namse = ModelTable.permited_fields(self)
            namse.append('createdate')
            return namse
        
        #def statistics(self, query):
        def inn_filter(self, query):
            ss=  query.extra(select={'createdate': "LEFT(createtime,10 )"})
                   #.order_by('createdate') 
            return ss
        
        def statistics(self, query):
            ss = query.values('channel','createdate').annotate(money=Sum('amount'))
            return ss
        
        class filters(RowFilter):
            range_fields=['createtime']
        
        class sort(RowSort):
            names = ['createdate']
          

class ReportCreatedateProc(BaseFieldProc):
    def get_range_filter_head(self):
        return {'name':'createdate',
                'label':'日期',
                'editor':'com-date-range-filter'
                }

field_map['%s.%s'%( model_to_name(TbChargeflow) ,'createdate')] = ReportCreatedateProc

director.update({
    'maindb.report.channel':ReportChnnel.tableCls
})

page_dc.update({
    'maindb.report.channel':ReportChnnel
})
        
        