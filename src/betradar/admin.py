from django.contrib import admin

# Register your models here.
from helpers.director.shortcut import TablePage,ModelTable,page_dc,RowSort,model_dc,FieldsPage,ModelFields
from .models import Alltournamentsidcn,Players

class AlltournamentsidcnPage(TablePage):
    class tableCls(ModelTable):
        model=Alltournamentsidcn
        exclude=[]

class AlltournamentsidcnFormPage(FieldsPage):
    class fieldsCls(ModelFields):
        class Meta:
            model = Alltournamentsidcn
            exclude=[]

class PlayersPage(TablePage):
    class tableCls(ModelTable):
        model=Players
        exclude=[]
        class sort(RowSort):
            names=['playersid','international']

class PlayersFormPage(FieldsPage):
    class fieldsCls(ModelFields):
        class Meta:
            model = Players
            exclude=[]

model_dc[Alltournamentsidcn]={'fields':AlltournamentsidcnFormPage.fieldsCls}
model_dc[Players]={'fields':PlayersFormPage.fieldsCls}

page_dc.update({
    'betradar.Alltournamentsidcn':AlltournamentsidcnPage,
    'betradar.Alltournamentsidcn.edit':AlltournamentsidcnFormPage,
    'betradar.Players':PlayersPage,
    'betradar.Players.edit':PlayersFormPage
})
