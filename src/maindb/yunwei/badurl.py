from helpers.director.shortcut import PlainTable,TablePage,page_dc,director
from maindb.mongoInstance import mydb
import json
from helpers.director.data_format.json_format import DirectorEncoder
import math
from django.utils import timezone
import pytz
import datetime

class BadurlPage(TablePage):
    def get_label(self):
        return '异常域名'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(PlainTable):
        def __init__(self,*args,**kws):
            super().__init__(*args,**kws)
            dc = {}
            if self.search_args.get('url'):
                dc['Url'] = {'$regex' : ".*%s.*"%self.search_args.get('url')}
            if self.search_args.get('UrlType'):
                dc['UrlType']=self.search_args.get('UrlType')
            beijin_tz = datetime.timezone(datetime.timedelta(hours=8))
            if self.search_args.get('_start_CreateTime'):
                start = timezone.datetime.strptime(self.search_args.get('_start_CreateTime') ,'%Y-%m-%d %H:%M:%S', )
                start = start.replace(tzinfo = beijin_tz)
                dc['CreateTime'] ={'$gte': start}
            if self.search_args.get('_end_CreateTime'):
                end = timezone.datetime.strptime(self.search_args.get('_end_CreateTime'), '%Y-%m-%d %H:%M:%S',  )
                end = end.replace(tzinfo = beijin_tz)
                if not 'CreateTime' in dc:
                    dc['CreateTime'] = {}
                dc['CreateTime'].update( {'$lte': end} )
                
            self.filter_args = dc
            
        def get_heads(self):
            return [
               
                {'name':'CreateTime','label':'创建时间','width':140},
                {'name':'UrlType','label':'Url类型','editor':'com-table-mapper','width':120,'options':[
                    {'value':1,'label':'AppService'},
                    {'value':2,'label':'Mq'},
                    {'value':3,'label':'Cdn'},
                    {'value':4,'label':'UrlService'},
                    ]},
                {'name':'ErrorCode','label':'错误代码'},
                {'name':'ErrorDesc','label':'错误描述','width':200},
                
                {'name':'Url','label':'地址','width':260},
                {'name':'Ip','label':'IP','width':130},
                {'name':'Area','label':'地区','width':150},
                {'name':'CostMilSeconds','label':'消耗毫秒数'},
                {'name':'Device','label':'设备'},
                {'name':'ReportTime','label':'报告时间'},
            ]
        
        def get_rows(self):
            out_row=[]
            start_index = ( self.page -1 ) * self.perpage
            beijin_tz = datetime.timezone(datetime.timedelta(hours=8))
            for item in mydb['BadUrl'].find(self.filter_args).sort('CreateTime',-1).skip(start_index).limit(self.perpage):
                item.pop('_id')
                item['CreateTime'] = item['CreateTime'].replace(tzinfo=pytz.UTC) .astimezone(beijin_tz)
                item['ReportTime'] = item['ReportTime'].replace(tzinfo=pytz.UTC) .astimezone(beijin_tz)
                #item['ReportTime'] = item.get('ReportTime').strftime('%Y-%m-%d %H:%M:%S')
                #item['Urls'] = json.dumps(item.get('Urls'),cls=DirectorEncoder)
                item['Device'] = json.dumps(item.get('Device'))
                out_row.append(item)
            return out_row
        
        def getRowPages(self):
            count = mydb['BadUrl'].find(self.filter_args).count()
            if self.page * self.perpage > count:
                self.page =  math.ceil( count/self.perpage )
            return {
                'total':count,
                'perpage':self.perpage,
                'crt_page':self.page
            }
        
        def getRowFilters(self):
            return [
                {'name':'url','label':'url','editor':'com-filter-text'},
                {'name':'UrlType','label':'url类型','editor':'com-filter-select','options':[
                    {'value':1,'label':'AppService'},
                    {'value':2,'label':'Mq'},
                    {'value':3,'label':'Cdn'},
                    {'value':4,'label':'UrlService'},
                ]},
                {'name':'CreateTime','label':'创建时间','editor':'com-filter-datetime-range'},
            ]

director.update({
    'badurl':BadurlPage.tableCls
})

page_dc.update({
    'badurl':BadurlPage
})