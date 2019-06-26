from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from maindb.models import TbAdvertisement

class AdvertisementPage(TablePage):
    def get_label(self):
        return '广告'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        pop_edit_fields=['id']
        model = TbAdvertisement
        exclude =[]
        def get_operation(self):
            ops = super().get_operation()
            ls =[]
            for op in ops:
                if op != 'delete_selected':
                    ls.append(op)
            return ls

class AdvertiseForm(ModelFields):
    class Meta:
        model = TbAdvertisement
        exclude =[]

director.update({
    'advertise':AdvertisementPage.tableCls,
    'advertise.edit':AdvertiseForm
})

page_dc.update({
    'advertise':AdvertisementPage
})