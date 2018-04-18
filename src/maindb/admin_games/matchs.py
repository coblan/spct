# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelTable,TablePage,page_dc
from ..models import TbMatches

class MatchsPage(TablePage):
    template='maindb/table.html'
    class tableCls(ModelTable):
        model = TbMatches
        exclude=[]

page_dc.update({
    'maindb.Matches':MatchsPage
})