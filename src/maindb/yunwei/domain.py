from helpers.director.shortcut import TablePage,ModelFields,ModelTable,page_dc,director
from ..models import TbDomain
import json
from django.conf import settings
import os

class DomainPage(TablePage):
    def get_label(self):
        return '域名管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbDomain
        exclude =[]
        
        def dict_head(self, head):
            width_dc ={
                'url':300
            }
            if head['name'] in width_dc:
                head['width'] = width_dc.get(head['name'])
            return head

class DomainForm(ModelFields):
    class Meta:
        model = TbDomain
        exclude = []
    
    def after_save(self):
        if self.changed_data:
            gen_js_file()

def gen_js_file():
    domain_list =[]
    for domain in TbDomain.objects.filter(status=1):
        domain_list.append(domain.url)
    outstr = 'url_list = %s'%json.dumps(domain_list)
    path = os.path.join(settings.MEDIA_ROOT,'public','check','domain.js')
    with open('w',path) as f:
        f.write(outstr)


director.update({
    'domain':DomainPage.tableCls,
    'domain.edit':DomainForm
})

page_dc.update({
    'domain':DomainPage
})