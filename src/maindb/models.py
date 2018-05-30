# encoding:utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from .status_code import *
from .cus_models_fields import CusPictureField, CusFileField
from helpers.director.model_func.cus_fields.cus_decimal import CusDecimalField

class Blackiplist(models.Model):
    blackiplistid = models.AutoField(db_column='BlackIpListID', primary_key=True)  # Field name made lowercase.
    ip = models.CharField(db_column='Ip', max_length=16)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200)  # Field name made lowercase.
    iswork = models.BooleanField(db_column='IsWork')  # Field name made lowercase.
    itype = models.IntegerField(db_column='IType')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BlackIpList'


class Blackiprangelist(models.Model):
    blackiprangelistid = models.AutoField(db_column='BlackIpRangeListID', primary_key=True,verbose_name= _('ID'))  # Field name made lowercase.
    startip = models.CharField(db_column='StartIp', max_length=16,verbose_name= _('StartIp') ) # Field name made lowercase.
    startipnum = models.BigIntegerField(db_column='StartIpNum', verbose_name= _('StartIpNum'))  # Field name made lowercase.
    endip = models.CharField(db_column='EndIp', max_length=16,verbose_name= _('EndIp'))  # Field name made lowercase.
    endipnum = models.BigIntegerField(db_column='EndIpNum', verbose_name= _('EndIpNum'))  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200,verbose_name= _('Remark'))  # Field name made lowercase.
    iswork = models.BooleanField(db_column='IsWork',verbose_name= _('IsWork'))  # Field name made lowercase.
    #itype = models.IntegerField(db_column='IType')  # Field name made lowercase.
    area = models.CharField(db_column='Area', max_length=255,verbose_name= _('Area'))  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BlackIpRangeList'


class TbAccount(models.Model):
    accountid = models.AutoField(db_column='AccountID',verbose_name=_('accountID'), primary_key=True)  # Field name made lowercase.
 
    accounttype = models.SmallIntegerField(db_column='AccountType',verbose_name=_('Account Type'),choices=ACCOUNT_TYPE)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=255)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=32)  # Field name made lowercase.
    username = models.CharField(db_column='UserName',verbose_name=_('User Name'), max_length=100, blank=True, null=True)  # Field name made lowercase.
    userrealname = models.CharField(db_column='UserRealName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    verify = models.SmallIntegerField(db_column='Verify')  # Field name made lowercase.
    agent = models.CharField(db_column='Agent', max_length=20, blank=True, null=True)  # Field name made lowercase.
    viplv = models.SmallIntegerField(db_column='VIPLv',verbose_name=_('VIP Level'))  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name=_('Create Time'))  # Field name made lowercase.
    pwupdatetime = models.DateTimeField(db_column='PWUpdateTime')  # Field name made lowercase.
    amount = CusDecimalField(db_column='Amount', max_digits=18, decimal_places=4, verbose_name=_('Account Balance') )  # Field name made lowercase.
    #amount = CusDecimalField(db_column='Amount',verbose_name=_('Account Balance'), max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=64, blank=True, null=True)  # Field name made lowercase.
    #currency = models.IntegerField(db_column='Currency', blank=True, null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=255)  # Field name made lowercase.
    gender = models.IntegerField(db_column='Gender')  # Field name made lowercase.
    birthday = models.CharField(db_column='Birthday', max_length=10, blank=True, null=True)  # Field name 
    points = models.IntegerField(db_column='Points', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Account'
    
    def __str__(self):
        return self.username or ''


class TbAccountMatchFav(models.Model):
    accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Account_Match_Fav'
        unique_together = (('accountid', 'matchid'),)


class TbAppresource(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    url = CusFileField(db_column='Url', max_length=255)  # Field name made lowercase.
    isexpired = models.BooleanField(db_column='IsExpired')  # Field name made lowercase.
    md5 = models.CharField(db_column='Md5', max_length=64)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AppResource'
        

class TbActivity(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    cover = CusPictureField(db_column='Cover', max_length=512, blank=True, null=True)  # Field name made lowercase.
    zip = models.CharField(db_column='Zip', max_length=512, blank=True, null=True)  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', null=True,default=0,choices=ONLINE_STATUS)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Activity'

class TbAreacitycode(models.Model):
    areacitycodeid = models.AutoField(db_column='AreaCityCodeID', primary_key=True)  # Field name made lowercase.
    cityid = models.IntegerField(db_column='CityId')  # Field name made lowercase.
    areaid = models.IntegerField(db_column='AreaId')  # Field name made lowercase.
    cityname = models.CharField(db_column='CityName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AreaCityCode'


class TbAreacode(models.Model):
    areaid = models.IntegerField(db_column='AreaId', primary_key=True)  # Field name made lowercase.
    areaname = models.CharField(db_column='AreaName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AreaCode'


class TbAppversion(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    terminal = models.IntegerField(db_column='Terminal',choices=PLATFORM)  # Field name made lowercase.
    packageurl = models.CharField(db_column='PackageUrl', max_length=255, blank=True, null=True)  # Field name made lowercase.
    md5 = models.CharField(db_column='Md5', max_length=32, blank=True, null=True)  # Field name made lowercase.
    versionid = models.IntegerField(db_column='VersionId',default=0)  # Field name made lowercase.
    versionname = models.CharField(db_column='VersionName', max_length=64, blank=False)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=512, blank=True, null=True)  # Field name made lowercase.
    required = models.IntegerField(db_column='Required',verbose_name=_('Force Update'), default=0, choices=REQUIRED)  # Field name made lowercase.
    size = models.FloatField(db_column='Size',default=0)  # Field name made lowercase.
    valid = models.BooleanField(db_column='Valid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tb_AppVersion'



class TbBalance(models.Model):
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    amount = CusDecimalField(db_column='Amount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    accountid = models.BigIntegerField(db_column='AccountID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Balance'


class TbBalancelog(models.Model):
    """
    账目记录
    """
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    account = models.CharField(db_column='Account',verbose_name=_('Account'), max_length=20)  # Field name made lowercase.
    categoryid = models.IntegerField(verbose_name='类型',db_column='CategoryID',choices=BALANCE_CAT)  # Field name made lowercase.
    cashflow = models.SmallIntegerField(db_column='CashFlow')  # Field name made lowercase.
    beforeamount = CusDecimalField(db_column='BeforeAmount',verbose_name=_('BeforeAmount'), max_digits=18, decimal_places=4)  # Field name made lowercase.
    amount = CusDecimalField(db_column='Amount',verbose_name=_('ChangedAmount'), max_digits=18, decimal_places=4)  # Field name made lowercase.
    afteramount = CusDecimalField(db_column='AfterAmount',verbose_name=_('AfterAmount'), max_digits=18, decimal_places=4)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo',verbose_name='备注', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(verbose_name=_('Change Time'),db_column='CreateTime')  # Field name made lowercase.
    creater = models.CharField(db_column='Creater',verbose_name=_('Operator'), max_length=20, blank=True, null=True)  # Field name made lowercase.
    accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BalanceLog'


class TbBankcards(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    cardno = models.CharField(db_column='CardNo', max_length=200)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    banktypeid = models.IntegerField(db_column='BankTypeID')  # Field name made lowercase.
    areaid = models.IntegerField(db_column='AreaID')  # Field name made lowercase.
    cityid = models.IntegerField(db_column='CityID')  # Field name made lowercase.
    phoneno = models.CharField(db_column='PhoneNo', max_length=200)  # Field name made lowercase.
    branchaddr = models.CharField(db_column='BranchAddr', max_length=100)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    lastusetime = models.DateTimeField(db_column='LastUseTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BankCards'


class TbBanktype(models.Model):
    banktypeid = models.IntegerField(db_column='BankTypeID', primary_key=True)  # Field name made lowercase.
    banktypename = models.CharField(db_column='BankTypeName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    moneyintype = models.IntegerField(db_column='MoneyInType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BankType'


class TbBetstopreason(models.Model):
    reasonid = models.IntegerField(db_column='ReasonID', primary_key=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=100)  # Field name made lowercase.
    dangerousstatus = models.SmallIntegerField(db_column='DangerousStatus')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BetStopReason'


class TbBlackuserlist(models.Model):
    blackuserlistid = models.AutoField(db_column='BlackUserListID', primary_key=True)  # Field name made lowercase.
    accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    accounttype = models.SmallIntegerField(db_column='AccountType', blank=True, null=True)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=100)  # Field name made lowercase.
    addtime = models.DateTimeField(db_column='AddTime', blank=True, null=True)  # Field name made lowercase.
    ban_status = models.SmallIntegerField(db_column='Ban_Status', blank=True, null=True)  # Field name made lowercase.
    #adduser = models.CharField(db_column='AddUser', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BlackUserList'


class TbBlackuserlistLog(models.Model):
    blacklogid = models.IntegerField(db_column='BlackLogID')  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=100, blank=True, null=True)  # Field name made lowercase.
    addtime = models.DateTimeField(db_column='AddTime', blank=True, null=True)  # Field name made lowercase.
    before_ban_status = models.SmallIntegerField(db_column='Before_Ban_Status', blank=True, null=True)  # Field name made lowercase.
    alter_ban_status = models.SmallIntegerField(db_column='Alter_Ban_Status', blank=True, null=True)  # Field name made lowercase.
    modify_user = models.CharField(db_column='Modify_user', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BlackUserList_Log'


class TbCategory(models.Model):
    categoryid = models.IntegerField(db_column='CategoryID', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', max_length=200)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Category'


class TbChannel(models.Model):
    channelid = models.IntegerField(db_column='ChannelID',verbose_name='渠道ID', primary_key=True)  # Field name made lowercase.
    channel = models.IntegerField(db_column='Channel',verbose_name=_('Channel'), max_length=40,unique=True)  # Field name made lowercase.
    channelname = models.CharField(db_column='ChannelName',verbose_name=_('Channel Name'), max_length=30)  # Field name made lowercase.
    #channelgroup = models.CharField(db_column='ChannelGroup', verbose_name='渠道群组',max_length=20)  # Field name made lowercase.
    #cashflow = models.SmallIntegerField(db_column='CashFlow',verbose_name='存提状态',choices=CHANNEL_CASHFLOW,default=0)  # Field name made lowercase.
    #returntype = models.CharField(db_column='ReturnType',verbose_name='回传类型', max_length=10)  # Field name made lowercase.
    maxlimit = CusDecimalField(db_column='MaxLimit',verbose_name=_('Max Limit Amount'), max_digits=18, decimal_places=4)  # Field name made lowercase.
    minlimit = CusDecimalField(db_column='MinLimit',verbose_name=_('Min Limit Amount'), max_digits=18, decimal_places=4)  # Field name made lowercase.
    grouptitle = models.CharField(db_column='GroupTitle',verbose_name=_('Group Title'), max_length=20)  # Field name made lowercase.
    #btnname = models.CharField(db_column='BtnName',verbose_name='类型名', max_length=20)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status',verbose_name=_('Status'),choices=CHANNEL_STATUS,default=0)  # Field name made lowercase.
    terminal = models.IntegerField(db_column='Terminal')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_Channel'
    
    def __str__(self):
        return self.channelname or ''


class TbCitycode(models.Model):
    areaid = models.IntegerField(db_column='AreaId', primary_key=True)  # Field name made lowercase.
    areaname = models.CharField(db_column='AreaName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_CityCode'


class TbCompetitors(models.Model):
    tb_competitorsid = models.AutoField(db_column='TB_CompetitorsId', primary_key=True)  # Field name made lowercase.
    id = models.BigIntegerField(db_column='ID')  # Field name made lowercase.
    superid = models.BigIntegerField(db_column='SuperID')  # Field name made lowercase.
    competitorbet = models.CharField(db_column='CompetitorBet', max_length=100)  # Field name made lowercase.
    competitorzh = models.CharField(db_column='CompetitorZh', max_length=100)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Competitors'


class TbConcurrentusers(models.Model):
    concurrentusersid = models.AutoField(db_column='ConcurrentUsersId', primary_key=True)  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=10)  # Field name made lowercase.
    servername = models.CharField(db_column='ServerName', max_length=32)  # Field name made lowercase.
    total = models.IntegerField(db_column='Total')  # Field name made lowercase.
    h00 = models.IntegerField(db_column='H00')  # Field name made lowercase.
    h01 = models.IntegerField(db_column='H01')  # Field name made lowercase.
    h02 = models.IntegerField(db_column='H02')  # Field name made lowercase.
    h03 = models.IntegerField(db_column='H03')  # Field name made lowercase.
    h04 = models.IntegerField(db_column='H04')  # Field name made lowercase.
    h05 = models.IntegerField(db_column='H05')  # Field name made lowercase.
    h06 = models.IntegerField(db_column='H06')  # Field name made lowercase.
    h07 = models.IntegerField(db_column='H07')  # Field name made lowercase.
    h08 = models.IntegerField(db_column='H08')  # Field name made lowercase.
    h09 = models.IntegerField(db_column='H09')  # Field name made lowercase.
    h10 = models.IntegerField(db_column='H10')  # Field name made lowercase.
    h11 = models.IntegerField(db_column='H11')  # Field name made lowercase.
    h12 = models.IntegerField(db_column='H12')  # Field name made lowercase.
    h13 = models.IntegerField(db_column='H13')  # Field name made lowercase.
    h14 = models.IntegerField(db_column='H14')  # Field name made lowercase.
    h15 = models.IntegerField(db_column='H15')  # Field name made lowercase.
    h16 = models.IntegerField(db_column='H16')  # Field name made lowercase.
    h17 = models.IntegerField(db_column='H17')  # Field name made lowercase.
    h18 = models.IntegerField(db_column='H18')  # Field name made lowercase.
    h19 = models.IntegerField(db_column='H19')  # Field name made lowercase.
    h20 = models.IntegerField(db_column='H20')  # Field name made lowercase.
    h21 = models.IntegerField(db_column='H21')  # Field name made lowercase.
    h22 = models.IntegerField(db_column='H22')  # Field name made lowercase.
    h23 = models.IntegerField(db_column='H23')  # Field name made lowercase.
    hn00 = models.IntegerField(db_column='HN00')  # Field name made lowercase.
    hn01 = models.IntegerField(db_column='HN01')  # Field name made lowercase.
    hn02 = models.IntegerField(db_column='HN02')  # Field name made lowercase.
    hn03 = models.IntegerField(db_column='HN03')  # Field name made lowercase.
    hn04 = models.IntegerField(db_column='HN04')  # Field name made lowercase.
    hn05 = models.IntegerField(db_column='HN05')  # Field name made lowercase.
    hn06 = models.IntegerField(db_column='HN06')  # Field name made lowercase.
    hn07 = models.IntegerField(db_column='HN07')  # Field name made lowercase.
    hn08 = models.IntegerField(db_column='HN08')  # Field name made lowercase.
    hn09 = models.IntegerField(db_column='HN09')  # Field name made lowercase.
    hn10 = models.IntegerField(db_column='HN10')  # Field name made lowercase.
    hn11 = models.IntegerField(db_column='HN11')  # Field name made lowercase.
    hn12 = models.IntegerField(db_column='HN12')  # Field name made lowercase.
    hn13 = models.IntegerField(db_column='HN13')  # Field name made lowercase.
    hn14 = models.IntegerField(db_column='HN14')  # Field name made lowercase.
    hn15 = models.IntegerField(db_column='HN15')  # Field name made lowercase.
    hn16 = models.IntegerField(db_column='HN16')  # Field name made lowercase.
    hn17 = models.IntegerField(db_column='HN17')  # Field name made lowercase.
    hn18 = models.IntegerField(db_column='HN18')  # Field name made lowercase.
    hn19 = models.IntegerField(db_column='HN19')  # Field name made lowercase.
    hn20 = models.IntegerField(db_column='HN20')  # Field name made lowercase.
    hn21 = models.IntegerField(db_column='HN21')  # Field name made lowercase.
    hn22 = models.IntegerField(db_column='HN22')  # Field name made lowercase.
    hn23 = models.IntegerField(db_column='HN23')  # Field name made lowercase.
    hl00 = models.IntegerField(db_column='HL00')  # Field name made lowercase.
    hl01 = models.IntegerField(db_column='HL01')  # Field name made lowercase.
    hl02 = models.IntegerField(db_column='HL02')  # Field name made lowercase.
    hl03 = models.IntegerField(db_column='HL03')  # Field name made lowercase.
    hl04 = models.IntegerField(db_column='HL04')  # Field name made lowercase.
    hl05 = models.IntegerField(db_column='HL05')  # Field name made lowercase.
    hl06 = models.IntegerField(db_column='HL06')  # Field name made lowercase.
    hl07 = models.IntegerField(db_column='HL07')  # Field name made lowercase.
    hl08 = models.IntegerField(db_column='HL08')  # Field name made lowercase.
    hl09 = models.IntegerField(db_column='HL09')  # Field name made lowercase.
    hl10 = models.IntegerField(db_column='HL10')  # Field name made lowercase.
    hl11 = models.IntegerField(db_column='HL11')  # Field name made lowercase.
    hl12 = models.IntegerField(db_column='HL12')  # Field name made lowercase.
    hl13 = models.IntegerField(db_column='HL13')  # Field name made lowercase.
    hl14 = models.IntegerField(db_column='HL14')  # Field name made lowercase.
    hl15 = models.IntegerField(db_column='HL15')  # Field name made lowercase.
    hl16 = models.IntegerField(db_column='HL16')  # Field name made lowercase.
    hl17 = models.IntegerField(db_column='HL17')  # Field name made lowercase.
    hl18 = models.IntegerField(db_column='HL18')  # Field name made lowercase.
    hl19 = models.IntegerField(db_column='HL19')  # Field name made lowercase.
    hl20 = models.IntegerField(db_column='HL20')  # Field name made lowercase.
    hl21 = models.IntegerField(db_column='HL21')  # Field name made lowercase.
    hl22 = models.IntegerField(db_column='HL22')  # Field name made lowercase.
    hl23 = models.IntegerField(db_column='HL23')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_ConcurrentUsers'


class TbConcurrentuserscount(models.Model):
    concurrentuserscountid = models.AutoField(db_column='ConcurrentUsersCountId', primary_key=True)  # Field name made lowercase.
    servername = models.CharField(db_column='ServerName', max_length=32)  # Field name made lowercase.
    count = models.IntegerField(db_column='Count')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_ConcurrentUsersCount'


class TbCurrency(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    value = CusDecimalField(db_column='Value', max_digits=18, decimal_places=0)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    icon = CusPictureField(db_column='Icon', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Currency'

class TbChargeflow(models.Model):
    id = models.BigIntegerField(db_column='Id', primary_key=True,verbose_name=_('ID'))  # Field name made lowercase.
    channel = models.ForeignKey(to=TbChannel,to_field='channel',db_constraint=False,db_column='Channel',verbose_name=_('Channel'))
    #channel = models.IntegerField(db_column='Channel')  # Field name made lowercase.
    productid = models.IntegerField(db_column='ProductId',verbose_name= _('ProductId') )# Field name made lowercase.
    createtime = models.CharField(db_column='CreateTime', max_length=27,verbose_name=_('CreateTime'))  # Field name made lowercase.
    callbacktime = models.CharField(db_column='CallbackTime', max_length=27, blank=True, null=True, verbose_name = _('CallbackTime'))  # Field name made lowercas
    accountid = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountId', verbose_name = _('Account'))
    #accountid = models.IntegerField(db_column='AccountId')  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount', verbose_name= _('Amount'))  # Field name made lowercase.
    success = models.IntegerField(db_column='Success', verbose_name= _('Success'))  
    credential = models.CharField(db_column='Credential', max_length=2048, verbose_name = _('Credential'))  # Field name made lowercase.
    error = models.CharField(db_column='Error', max_length=4096, blank=True, null=True)  # Field name made lowercase.
    providerid = models.CharField(db_column='ProviderId', max_length=64, blank=True, null=True)  # Field name made lowercase.
    currency = CusDecimalField(db_column='Currency', max_digits=18, decimal_places=0, verbose_name= _('Currency'))  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True, verbose_name = _('Remark'))  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_ChargeFlow'

class TbContacts(models.Model):
    contactsid = models.AutoField(db_column='ContactsId', primary_key=True)  # Field name made lowercase.
    accountid = models.IntegerField(db_column='AccountId')  # Field name made lowercase.
    contactaccountid = models.IntegerField(db_column='ContactAccountId')  # Field name made lowercase.
    commonlyused = models.BooleanField(db_column='CommonlyUsed')  # Field name made lowercase.
    blacklist = models.BooleanField(db_column='Blacklist')  # Field name made lowercase.
    sticky = models.BooleanField(db_column='Sticky')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Contacts'


class TbD9Userhttpreferer(models.Model):
    d9userhttprefererid = models.AutoField(db_column='D9UserHttpRefererID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=12)  # Field name made lowercase.
    referrer = models.CharField(db_column='Referrer', max_length=512)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=64)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_D9UserHttpReferer'


class TbEventbonusLog(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    eventid = models.IntegerField(db_column='EventID')  # Field name made lowercase.
    totalturnover = CusDecimalField(db_column='TotalTurnover', max_digits=18, decimal_places=4)  # Field name made lowercase.
    nowturnover = CusDecimalField(db_column='NowTurnover', max_digits=18, decimal_places=4)  # Field name made lowercase.
    bonus = CusDecimalField(db_column='Bonus', max_digits=18, decimal_places=4)  # Field name made lowercase.
    addwithdrawlimit = CusDecimalField(db_column='AddWithdrawLimit', max_digits=18, decimal_places=4)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=50)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    validtime = models.DateTimeField(db_column='ValidTime')  # Field name made lowercase.
    gifttime = models.DateTimeField(db_column='GiftTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_EventBonus_Log'


class TbEventbonustList(models.Model):
    eventid = models.IntegerField(db_column='EventID', primary_key=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.
    eventname = models.CharField(db_column='EventName', max_length=20)  # Field name made lowercase.
    bonuspa = CusDecimalField(db_column='BonusPa', max_digits=18, decimal_places=4)  # Field name made lowercase.
    maxbonus = CusDecimalField(db_column='MaxBonus', max_digits=18, decimal_places=4)  # Field name made lowercase.
    turnovermultiple = CusDecimalField(db_column='TurnoverMultiple', max_digits=18, decimal_places=2)  # Field name made lowercase.
    withdrawlimitmultiple = CusDecimalField(db_column='WithdrawlimitMultiple', max_digits=18, decimal_places=2)  # Field name made lowercase.
    validdays = models.IntegerField(db_column='ValidDays')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=100)  # Field name made lowercase.
    moneycategory = models.IntegerField(db_column='MoneyCategory')  # Field name made lowercase.
    status = models.BooleanField(db_column='Status')  # Field name made lowercase.
    multiplereceive = models.BooleanField(db_column='MultipleReceive')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    createuser = models.CharField(db_column='CreateUser', max_length=20)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    updateuser = models.CharField(db_column='UpdateUser', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_EventBonust_List'


class TbIpdata(models.Model):
    ipdataid = models.AutoField(db_column='IpDataID', primary_key=True)  # Field name made lowercase.
    startip = models.CharField(db_column='StartIP', max_length=16)  # Field name made lowercase.
    sartipnum = models.BigIntegerField(db_column='SartIPNum')  # Field name made lowercase.
    endip = models.CharField(db_column='EndIP', max_length=16)  # Field name made lowercase.
    endipnum = models.BigIntegerField(db_column='EndIPNum')  # Field name made lowercase.
    area = models.CharField(db_column='Area', max_length=128)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=512)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_IpData'


class TbLoginlog(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountId')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountId')  # Field name made lowercase.
    devicecode = models.CharField(db_column='DeviceCode',verbose_name=_('Device Code'), max_length=40)  # Field name made lowercase.
    deviceip = models.CharField(db_column='DeviceIP', verbose_name=_('Device Ip'),max_length=20)  # Field name made lowercase.    
    #devicecode = models.CharField(db_column='DeviceCode', max_length=40, blank=True, null=True)  # Field name made lowercase.
    #deviceip = models.CharField(db_column='DeviceIP', max_length=20)  # Field name made lowercase.
    ternimal = models.IntegerField(db_column='Ternimal',verbose_name=_('Terminal'))  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name=_('Login Time'))  # Field name made lowercase.
    appversion = models.CharField(db_column='AppVersion',verbose_name=_('Device Version'), max_length=20, blank=True, null=True)  # Field name made lowercase.
    devicename = models.CharField(db_column='DeviceName', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deviceversion = models.CharField(db_column='DeviceVersion', max_length=20, blank=True, null=True)  # Field name made lowercase.
    logintype = models.IntegerField(db_column='LoginType')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_LoginLog'


#class TbLoginlog(models.Model):
    #tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    #account = models.CharField(db_column='Account',verbose_name=_('Account'), max_length=30)  # Field name made lowercase.
  
    #logintype = models.SmallIntegerField(db_column='LoginType',verbose_name=_(
        #'Login Type'))  # Field name made lowercase.
    #createtime = models.DateTimeField(verbose_name=_('Login Time'),db_column='CreateTime')  # Field name made lowercase.
    #appversion = models.CharField(db_column='AppVersion',verbose_name=_('App Version'), max_length=20)  # Field name made lowercase.
    #devicename = models.CharField(db_column='DeviceName', verbose_name=_('Device Name'),max_length=40)  # Field name made lowercase.
    #deviceversion = models.CharField(db_column='DeviceVersion',verbose_name=_(
        #'Device Version'), max_length=20)  # Field name made lowercase.
    #logoutreason = models.SmallIntegerField(db_column='LogoutReason')  # Field name made lowercase.
    #logouttime = models.DateTimeField(db_column='LogoutTime',verbose_name=_(
        #'Logout Time'))  # Field name made lowercase.

    #class Meta:
        #managed = False
        #db_table = 'TB_LoginLog'


class TbMaintournament(models.Model):
    uniquetournamentid = models.IntegerField(db_column='UniqueTournamentID')  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=128)  # Field name made lowercase.
    createtimne = models.DateTimeField(db_column='CreateTimne')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_MainTournament'
        unique_together = (('uniquetournamentid', 'sportid', 'categoryid'),)


class TbMatches(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID',verbose_name=_('Match Category') ) # Field name made lowercase.
    tournamentid = models.IntegerField(db_column='TournamentID')  # Field name made lowercase.
    tournamentzh = models.CharField(db_column='TournamentZH',verbose_name=_('Tournament'), max_length=50)  # Field name made lowercase.
    matchid = models.IntegerField(db_column='MatchID',unique=True)  # Field name made lowercase.
    prematchdate = models.DateTimeField(db_column='PreMatchDate')  # Field name made lowercase.
    matchdate = models.DateTimeField(db_column='MatchDate',verbose_name=_('Match Date') )  # Field name made lowercase.
    currentperiodstart = models.DateTimeField(db_column='CurrentPeriodStart',verbose_name=_('CurrentPeriodStart'), blank=True, null=True)  # 结束时间 Field name made lowercase.
    team1id = models.IntegerField(db_column='Team1ID')  # Field name made lowercase.
    superteam1id = models.BigIntegerField(db_column='SuperTeam1Id')  # Field name made lowercase.
    team1zh = models.CharField(db_column='Team1ZH', verbose_name=_('Home Team'),max_length=20)  # Field name made lowercase.
    team2id = models.IntegerField(db_column='Team2ID')  # Field name made lowercase.
    superteam2id = models.BigIntegerField(db_column='SuperTeam2Id')  # Field name made lowercase.
    team2zh = models.CharField(db_column='Team2ZH', verbose_name=_('Away Team'),max_length=20)  # Field name made lowercase.
    matchscore = models.CharField(db_column='MatchScore', max_length=8,verbose_name=_('Match Score'),blank=True)  # Field name made lowercase.
    winner = models.IntegerField(db_column='Winner',verbose_name=_('Winner'))  # Field name made lowercase.
    statuscode = models.IntegerField(db_column='StatusCode',verbose_name=_('Status'))  # Field name made lowercase.
    roundinfo = models.IntegerField(db_column='RoundInfo',verbose_name=_('Round'))  # 轮数 Field name made lowercase.
    isrecommend = models.BooleanField(db_column='IsRecommend',verbose_name=_('IsRecommend'))  #推介 Field name made lowercase.
    livebet = models.BooleanField(db_column='LiveBet',verbose_name=_('LiveBet'))  # 滚球 Field name made lowercase.
    generatedat = models.DateTimeField(db_column='GeneratedAt',verbose_name=_('Create Time') )  # 生成日期 Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    weights = CusDecimalField(db_column='Weights', max_digits=18, decimal_places=2)  # Field name made lowercase.
    uniquetournamentid = models.BigIntegerField(db_column='UniqueTournamentId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Matches'
    
class TbMatchesoddsswitch(models.Model):
    matchesoddsswitchid = models.AutoField(db_column='MatchesOddsSwitchID', primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID',default=1)  # Field name made lowercase.
    types = models.IntegerField(db_column='Types', blank=True, null=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    oddstypegroup = models.ForeignKey(to='TbOddstypegroup',db_constraint=False,to_field='oddstypegroup',db_column='OddsTypeGroup', blank=True, null=True)  # Field name made lowercase.
    #oddstypegroup = models.IntegerField(db_column='OddsTypeGroup', blank=True, null=True)  # Field name made lowercase.
    specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=12, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime',auto_now=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_MatchesOddsSwitch'

#class TbMatchesoddsswitch(models.Model):
    #matchesoddsswitchid = models.AutoField(db_column='MatchesOddsSwitchID', primary_key=True)  # Field name made lowercase.
    #sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    #matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    #oddstypegroup = models.IntegerField(db_column='OddsTypeGroup')  # Field name made lowercase.
    #status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    #createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    #updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.

    #class Meta:
        #managed = False
        #db_table = 'TB_MatchesOddsSwitch'

class TbMatchesturnover(models.Model):
    tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    match = models.ForeignKey(TbMatches, db_column='MatchID', db_constraint= False, to_field= 'matchid')
    #matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    oddsid = models.BigIntegerField(db_column='OddsID')  # Field name made lowercase.
    specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=20)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    turnover = models.DecimalField(db_column='Turnover', max_digits=18, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_MatchesTurnover'

class TbMatchesBetstatus(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    betstatus = models.SmallIntegerField(db_column='BetStatus')  # Field name made lowercase.
    betstopreason = models.CharField(db_column='BetStopReason', max_length=50)  # Field name made lowercase.
    stopreasonid = models.IntegerField(db_column='StopReasonId')  # Field name made lowercase.
    stopreason = models.CharField(db_column='StopReason', max_length=50)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    score = models.CharField(max_length=10)
    redcardshome = models.IntegerField()
    redcardsaway = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'TB_Matches_BetStatus'


class TbMessageUnsend(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #toaccountsn = models.CharField(db_column='ToAccountSN', max_length=36)  # Field name made lowercase.
    body = models.CharField(db_column='Body', max_length=512)  # Field name made lowercase.
    type = models.SmallIntegerField(db_column='Type')  # Field name made lowercase.
    sender = models.CharField(db_column='Sender', max_length=20)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Message_Unsend'


class TbMessages(models.Model):
    messagesid = models.AutoField(db_column='MessagesId', primary_key=True)  # Field name made lowercase.
    accountid = models.IntegerField(db_column='AccountId')  # Field name made lowercase.
    spearkeraccountid = models.IntegerField(db_column='SpearkerAccountId')  # Field name made lowercase.
    spearkername = models.CharField(db_column='SpearkerName', max_length=10)  # Field name made lowercase.
    listeneraccountid = models.IntegerField(db_column='ListenerAccountId')  # Field name made lowercase.
    listenername = models.CharField(db_column='ListenerName', max_length=10)  # Field name made lowercase.
    body = models.CharField(db_column='Body', max_length=512)  # Field name made lowercase.
    haveread = models.BooleanField(db_column='HaveRead')  # Field name made lowercase.
    received = models.BooleanField(db_column='Received')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Messages'


class TbMoneyCategories(models.Model):
    balancecategoriesid = models.AutoField(db_column='BalanceCategoriesId', primary_key=True)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID')  # Field name made lowercase.
    cashflow = models.SmallIntegerField(db_column='CashFlow')  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', max_length=20)  # Field name made lowercase.
    categorytype = models.SmallIntegerField(db_column='CategoryType')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Money_Categories'


class TbNetworkerror(models.Model):
    networkerrorid = models.AutoField(db_column='NetworkErrorID', primary_key=True)  # Field name made lowercase.
    clientip = models.CharField(db_column='ClientIp', max_length=64)  # Field name made lowercase.
    apiname = models.CharField(db_column='ApiName', max_length=128)  # Field name made lowercase.
    elapsedtime = models.IntegerField(db_column='ElapsedTime')  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=1024)  # Field name made lowercase.
    sendtime = models.DateTimeField(db_column='SendTime')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_NetworkError'


class TbNotice(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=1024, blank=False, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=512, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now=True,verbose_name='修改时间')  # Field name made lowercase.
    #createuser = models.ForeignKey(to=User,db_column='CreateUser', blank=True, null=True,db_constraint=False)  #
    createuser = models.IntegerField(db_column='CreateUser', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True,choices=ONLINE_STATUS)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True,default='')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_Notice'

class TbOdds(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    msgnr = models.BigIntegerField(db_column='MsgNr')  # Field name made lowercase.
    #oddsid = models.BigIntegerField(db_column='OddsID')  # Field name made lowercase.
    oddstype = models.ForeignKey(to='TbOddstypes',db_column='OddsID',db_constraint=False,to_field='oddsid')  # Field name made lowercase.
    odds = CusDecimalField(db_column='Odds', max_digits=18, decimal_places=2)  # Field name made lowercase.
    specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=12)  # Field name made lowercase.
    oddsid_ori = models.BigIntegerField(db_column='OddsID_ori')  # Field name made lowercase.
    source = models.SmallIntegerField(db_column='Source')  # Field name made lowercase.
    uptodate = models.SmallIntegerField(db_column='UpToDate')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    score = models.CharField(db_column='Score', max_length=8)  # Field name made lowercase.
    fortherest = models.CharField(db_column='ForTheRest', max_length=12)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    optionzh = models.CharField(db_column='OptionZH', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Odds'


class TbOddsspread(models.Model):
    tid = models.AutoField(db_column='Tid',primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    oddstypegroup = models.IntegerField(db_column='OddsTypeGroup')  # Field name made lowercase.
    spread = CusDecimalField(db_column='Spread', max_digits=18, decimal_places=2)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    createuser = models.CharField(db_column='CreateUser', max_length=20)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    updateuser = models.CharField(db_column='UpdateUser', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_OddsSpread'


class TbOddstypes(models.Model):
    oddstypesid = models.BigAutoField(db_column='OddsTypesId', primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    oddsid = models.BigIntegerField(db_column='OddsID',unique=True)  # Field name made lowercase.
    oddskind = models.IntegerField(db_column='OddsKind')  # Field name made lowercase.
    oddstypegroup = models.ForeignKey(to='TbOddstypegroup',db_constraint=False,to_field='oddstypegroup',db_column='OddsTypeGroup')  # Field name made lowercase.
    #oddstypegroup = models.IntegerField(db_column='OddsTypeGroup')  # Field name made lowercase.
    oddstypeid = models.IntegerField(db_column='OddsTypeID')  # Field name made lowercase.
    subtype = models.IntegerField(db_column='Subtype', blank=True, null=True)  # Field name made lowercase.
    oddstypename = models.CharField(db_column='OddsTypeName', max_length=50)  # Field name made lowercase.
    oddstypenamezh = models.CharField(db_column='OddsTypeNameZH', max_length=10)  # Field name made lowercase.
    oddsoutcome = models.CharField(db_column='OddsOutcome', max_length=20)  # Field name made lowercase.
    outcome = models.IntegerField(db_column='Outcome')  # Field name made lowercase.
    outcomedesc = models.CharField(db_column='OutcomeDesc', max_length=200)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort', blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='Enabled', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_OddsTypes'

#class TbOddstypes(models.Model):
    #oddstypesid = models.AutoField(db_column='OddsTypesId', primary_key=True)  # Field name made lowercase.
    #sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    #oddsid = models.IntegerField(db_column='OddsID',unique=True)  # Field name made lowercase.
    #oddskind = models.SmallIntegerField(db_column='OddsKind')  # 1 早盘，2 滚球 Field name made lowercase.
    #oddstypegroup = models.SmallIntegerField(db_column='OddsTypeGroup')  # Field name made lowercase.
    #oddstypeid = models.IntegerField(db_column='OddsTypeID')  # Field name made lowercase.
    #subtype = models.IntegerField(db_column='Subtype', blank=True, null=True)  # Field name made lowercase.
    #oddstypename = models.CharField(db_column='OddsTypeName', max_length=50)  # Field name made lowercase.
    #oddstypenamezh = models.CharField(db_column='OddsTypeNameZH', max_length=10)  # Field name made lowercase.
    #oddsoutcome = models.CharField(db_column='OddsOutcome', max_length=20)  # Field name made lowercase.
    #outcome = models.IntegerField(db_column='Outcome')  # Field name made lowercase.
    #outcomedesc = models.CharField(db_column='OutcomeDesc', max_length=200)  # Field name made lowercase.
    #status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.

    #class Meta:
        #managed = False
        #db_table = 'TB_OddsTypes'


    
class TbOddstypegroup(models.Model):
    tid = models.IntegerField(db_column='TID', primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    oddstypegroup = models.IntegerField(db_column='OddsTypeGroup',unique=True)  # Field name made lowercase.
    oddstypenamezh = models.CharField(db_column='OddsTypeNameZH', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    enabled = models.IntegerField(db_column='Enabled')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_OddsTypeGroup'

class TbOddsHistory(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    oddstid = models.BigIntegerField(db_column='OddsTid')  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    msgnr = models.BigIntegerField(db_column='MsgNr')  # Field name made lowercase.
    oddsid = models.BigIntegerField(db_column='OddsID')  # Field name made lowercase.
    odds = CusDecimalField(db_column='Odds', max_digits=18, decimal_places=2)  # Field name made lowercase.
    specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=12)  # Field name made lowercase.
    oddsid_ori = models.BigIntegerField(db_column='OddsID_ori')  # Field name made lowercase.
    source = models.SmallIntegerField(db_column='Source')  # Field name made lowercase.
    uptodate = models.SmallIntegerField(db_column='UpToDate')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    score = models.CharField(db_column='Score', max_length=8)  # Field name made lowercase.
    fortherest = models.CharField(db_column='ForTheRest', max_length=12)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    optionzh = models.CharField(db_column='OptionZH', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Odds_History'


class TbOddsResult(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    matchid = models.IntegerField(db_column='MatchID')  # Field name made lowercase.
    oddskind = models.SmallIntegerField(db_column='OddsKind')  # Field name made lowercase.
    oddsid = models.IntegerField(db_column='OddsID')  # Field name made lowercase.
    oddsid_ori = models.BigIntegerField(db_column='OddsID_ori', blank=True, null=True)  # Field name made lowercase.
    oddsoucome = models.CharField(db_column='OddsOucome', max_length=20)  # Field name made lowercase.
    voidfactor = models.CharField(db_column='VoidFactor', max_length=10, blank=True, null=True)  # Field name made lowercase.
    specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=12, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Odds_Result'


class TbOutrightevent(models.Model):
    tid = models.AutoField(db_column='Tid',primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID')  # Field name made lowercase.
    tournamentid = models.BigIntegerField(db_column='TournamentID')  # Field name made lowercase.
    eventid = models.IntegerField(db_column='EventID')  # Field name made lowercase.
    eventinfo = models.CharField(db_column='EventInfo', max_length=50)  # Field name made lowercase.
    eventdate = models.DateTimeField(db_column='EventDate')  # Field name made lowercase.
    eventenddate = models.DateTimeField(db_column='EventEndDate')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_OutRightEvent'


class TbParlayrules(models.Model):
    parlayid = models.IntegerField(db_column='ParlayID', primary_key=True)  # Field name made lowercase.
    parlaycount = models.SmallIntegerField(db_column='ParlayCount')  # Field name made lowercase.
    stakecount = models.SmallIntegerField(db_column='StakeCount')  # Field name made lowercase.
    ticket1 = models.SmallIntegerField(db_column='Ticket1')  # Field name made lowercase.
    ticket2 = models.SmallIntegerField(db_column='Ticket2')  # Field name made lowercase.
    ticket3 = models.SmallIntegerField(db_column='Ticket3')  # Field name made lowercase.
    ticket4 = models.SmallIntegerField(db_column='Ticket4')  # Field name made lowercase.
    ticket5 = models.SmallIntegerField(db_column='Ticket5')  # Field name made lowercase.
    ticket6 = models.SmallIntegerField(db_column='Ticket6')  # Field name made lowercase.
    parlayname = models.CharField(db_column='ParlayName', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_ParlayRules'


class TbPasswordResettoken(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    resettoken = models.CharField(db_column='ResetToken', max_length=36)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    usetime = models.DateTimeField(db_column='UseTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Password_ResetToken'


class TbPaymentChannels(models.Model):
    channelid = models.IntegerField(db_column='ChannelID', primary_key=True)  # Field name made lowercase.
    channelname = models.CharField(db_column='ChannelName', max_length=20)  # Field name made lowercase.
    channeltype = models.CharField(db_column='ChannelType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    orderno = models.SmallIntegerField(db_column='OrderNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Payment_Channels'


class TbPlayers(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=50)  # Field name made lowercase.
    superid = models.CharField(db_column='SuperID', max_length=50)  # Field name made lowercase.
    international = models.CharField(db_column='International', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Players'


class TbQa(models.Model):
    qaid = models.AutoField(db_column='QAID', primary_key=True)  # Field name made lowercase.
    class_field = models.CharField(db_column='Class', max_length=1,default=0,blank=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    mtype = models.IntegerField(db_column='MType',verbose_name=_('Belong To'))  # 从属于Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.
    priority = models.SmallIntegerField(db_column='Priority',default=0,blank=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=100)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=1500)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status',choices=ONLINE_STATUS)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime',auto_now=True)  # Field name made lowercase.
    ver = models.IntegerField(db_column='Ver',default=0,blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_QA'


class TbRcFilter(models.Model):
    rc_rule_id = models.AutoField(db_column='RC_rule_id', primary_key=True)  # Field name made lowercase.
    rc_level = models.CharField(db_column='RC_Level',verbose_name=_('Level'), max_length=1)  # Field name made lowercase.
    rc_rule = models.IntegerField(db_column='RC_rule',verbose_name=_('Rule'))  # Field name made lowercase.
    rc_rule_name = models.CharField(db_column='RC_rule_Name',verbose_name = _('Rule Level'), max_length=30)  # Field name made lowercase.'
    rc_filter = CusDecimalField(db_column='RC_filter',verbose_name=_('Filter'), max_digits=18, decimal_places=2)  # Field name made lowercase.
    rc_active = models.SmallIntegerField(db_column='RC_active',verbose_name=_('Active'))  # Field name made lowercase.
    rc_days = models.IntegerField(db_column='RC_DAYS',verbose_name=_('Days'))  # Field name made lowercase.
    description = models.CharField(db_column='Description',verbose_name=_('Description'), max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_RC_Filter'


class TbRcLevel(models.Model):
    rc_level_id = models.AutoField(db_column='RC_Level_ID', primary_key=True, verbose_name = _('RcLevelID'))  # Field name made lowercase.
    rc_level = models.CharField(db_column='RC_Level', max_length=1, verbose_name = _('RcLevel'))  # Field name made lowercase.
    rc_level_type = models.IntegerField(db_column='RC_Level_Type', verbose_name= _('RcLevelType'))  # Field name made lowercase.
    rc_level_name = models.CharField(db_column='RC_Level_Name', max_length=20, verbose_name = _('RcLevelName'))  # Field name made lowercase.
    rc_level_filter = CusDecimalField(db_column='RC_Level_Filter', max_digits=18, decimal_places=2, verbose_name= _('RcLevelFilter'))  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_RC_Level'


class TbRcUser(models.Model):
    accountid = models.IntegerField(db_column='AccountID', primary_key=True, verbose_name= _('AccountID'))  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    accounttype = models.SmallIntegerField(db_column='AccountType', verbose_name= _('AccountType'))  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20, verbose_name = _('Account'))  # Field name made lowercase.
    rc_level = models.CharField(db_column='RC_Level', max_length=1, verbose_name = _('RcLevel'))  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_RC_USER'


class TbReturnmessage(models.Model):
    spid = models.IntegerField(db_column='SPID')  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=10)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=10)  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_ReturnMessage'
        unique_together = (('spid', 'language', 'code'),)


class TbSplist(models.Model):
    spid = models.IntegerField(db_column='SPID', primary_key=True)  # Field name made lowercase.
    spname = models.CharField(db_column='SPName', max_length=40)  # Field name made lowercase.
    needtoken = models.SmallIntegerField(db_column='needToken')  # Field name made lowercase.
    iscache = models.SmallIntegerField(db_column='isCache')  # Field name made lowercase.
    dbname = models.CharField(db_column='DBName', max_length=20)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_SPList'


class TbSetting(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    settingname = models.CharField(db_column='settingName', max_length=20)  # Field name made lowercase.
    settingkey = models.IntegerField(db_column='settingKey')  # Field name made lowercase.
    settingvalue = models.CharField(db_column='settingValue', max_length=50)  # Field name made lowercase.
    settingorder = models.IntegerField(db_column='settingOrder')  # Field name made lowercase.
    settingtime = models.DateTimeField(db_column='settingTime')  # Field name made lowercase.
    memo = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'TB_Setting'


class TbSport(models.Model):
    sportid = models.IntegerField(db_column='SportID', primary_key=True)  # Field name made lowercase.
    sportname = models.CharField(db_column='SportName', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Sport'


class TbSpreadingodds(models.Model):
    category = models.CharField(db_column='Category', max_length=20)  # Field name made lowercase.
    spreading = models.SmallIntegerField(db_column='Spreading')  # Field name made lowercase.
    book = CusDecimalField(db_column='Book', max_digits=18, decimal_places=3)  # Field name made lowercase.
    euro = CusDecimalField(db_column='EURO', max_digits=18, decimal_places=3)  # Field name made lowercase.
    hk = CusDecimalField(db_column='HK', max_digits=18, decimal_places=3)  # Field name made lowercase.
    malay = CusDecimalField(db_column='MALAY', max_digits=18, decimal_places=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_SpreadingOdds'
        unique_together = (('category', 'spreading', 'book'),)


class TbStatuscode(models.Model):
    statuscodeid = models.IntegerField(db_column='StatusCodeId')  # Field name made lowercase.
    sportid = models.SmallIntegerField(db_column='SportID')  # Field name made lowercase.
    statuscode = models.IntegerField(db_column='StatusCode', primary_key=True)  # Field name made lowercase.
    livestatus = models.SmallIntegerField(db_column='LiveStatus')  # Field name made lowercase.
    text = models.CharField(db_column='Text', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_StatusCode'


#class TbTicketmaster(models.Model):
    #ticketid = models.BigIntegerField(db_column='TicketID', primary_key=True)  # Field name made lowercase.
    #account = models.CharField(db_column='Account', max_length=200)  # Field name made lowercase.
    #stakeamount = CusDecimalField(db_column='StakeAmount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    #betamount = CusDecimalField(db_column='BetAmount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    #parlayrule = models.IntegerField(db_column='ParlayRule')  # Field name made lowercase.
    #allowauto = models.SmallIntegerField(db_column='AllowAuto')  # Field name made lowercase.
    #status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    #winbet = models.SmallIntegerField(db_column='WinBet')  # Field name made lowercase.
    #createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    #betoutcome = CusDecimalField(db_column='BetOutcome', max_digits=18, decimal_places=4)  # Field name made lowercase.
    #turnover = CusDecimalField(db_column='Turnover', max_digits=18, decimal_places=4)  # Field name made lowercase.
    #bonuspa = CusDecimalField(db_column='BonusPa', max_digits=18, decimal_places=4)  # Field name made lowercase.
    #bonus = CusDecimalField(db_column='Bonus', max_digits=18, decimal_places=4)  # Field name made lowercase.
    #rawdata = models.CharField(db_column='RawData', max_length=4000)  # Field name made lowercase.
    #settletime = models.DateTimeField(db_column='SettleTime', blank=True, null=True)  # Field name made lowercase.
    #stakecount = models.IntegerField(db_column='StakeCount')  # Field name made lowercase.
    #parlaycount = models.IntegerField(db_column='ParlayCount')  # Field name made lowercase.
    #reststakecount = models.IntegerField(db_column='RestStakeCount')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    #orderid = models.BigIntegerField(db_column='OrderID', unique=True)  # Field name made lowercase.
    #handicap = models.IntegerField(db_column='Handicap')  # Field name made lowercase.
    #possibleturnover = CusDecimalField(db_column='PossibleTurnover', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    #class Meta:
        #managed = False
        #db_table = 'TB_TicketMaster'


class TbTicketmaster(models.Model):
    "注单列表"
    ticketid = models.AutoField(db_column='TicketID',verbose_name=_('Ticket ID'), primary_key=True)
    account = models.CharField(db_column='Account',verbose_name=_('Account'), max_length=20)  # Field name made lowercase.
    stakeamount = CusDecimalField(db_column='StakeAmount',verbose_name=_('StakeAmount'), max_digits=18, decimal_places=4)  # 单注金额 .
    betamount = CusDecimalField(db_column='BetAmount',verbose_name=_('BetAmount'), max_digits=18, decimal_places=4)  # 总金额 Field name made lowercase.
    parlayrule = models.IntegerField(db_column='ParlayRule',verbose_name=_('ParlayRule'))  # 串关规则
    allowauto = models.SmallIntegerField(db_column='AllowAuto',verbose_name=_('AllowAuto'))  # 自动接收最新赔率
    status = models.IntegerField(db_column='Status',verbose_name=_('Status'))  # Field name made lowercase.
    winbet = models.SmallIntegerField(db_column='WinBet',verbose_name=_('WinBet'))  # 是否中注
    createtime = models.DateTimeField(verbose_name=_('CreateTime'),db_column='CreateTime')  # Field name made lowercase.
    betoutcome = CusDecimalField(db_column='BetOutcome',verbose_name= _('BetOutcome'), max_digits=18, decimal_places=4)  # 派彩金额
    turnover = CusDecimalField(db_column='Turnover', verbose_name='流水',max_digits=18, decimal_places=4)  # Field name made lowercase.
    bonuspa = CusDecimalField(db_column='BonusPa',verbose_name='反水比例', max_digits=18, decimal_places=4)  # Field name made lowercase.
    bonus = CusDecimalField(db_column='Bonus',verbose_name='反水/红利', max_digits=18, decimal_places=4)  # Field name made lowercase.
    rawdata = models.CharField(db_column='RawData',verbose_name='原始数据', max_length=4000)  # Field name made lowercase.
    settletime = models.DateTimeField(verbose_name='结算时间',db_column='SettleTime')  # Field name made lowercase.
    stakecount = models.IntegerField(db_column='StakeCount')  # Field name made lowercase.
    parlaycount = models.IntegerField(db_column='ParlayCount')  # Field name made lowercase.
    reststakecount = models.IntegerField(db_column='RestStakeCount')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    accountid = models.ForeignKey(TbAccount,db_column='AccountID',db_constraint=False) 
    orderid = models.BigIntegerField(db_column='OrderID', unique=True)  # Field name made lowercase.
    handicap = models.IntegerField(db_column='Handicap')  # Field name made lowercase.
    possibleturnover = CusDecimalField(db_column='PossibleTurnover', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.    

    class Meta:
        managed = False
        db_table = 'TB_TicketMaster'
    
    def __str__(self): 
        return str(self.ticketid)


class TbTicketparlay(models.Model):
    """串关规则"""
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #ticketid = models.BigIntegerField(db_column='TicketID')
    ticket_master = models.ForeignKey(TbTicketmaster,db_column='TicketID', db_constraint=False,verbose_name=_(
        'ticket master'))    
    #ticketid = models.CharField(db_column='TicketID', max_length=20)  # Field name made lowercase.
    parlay1tid = models.BigIntegerField(db_column='Parlay1Tid',verbose_name='子注单ID1')  # Field name made lowercase.
    parlay2tid = models.BigIntegerField(db_column='Parlay2Tid',verbose_name='子注单ID2')  # Field name made lowercase.
    parlay3tid = models.BigIntegerField(db_column='Parlay3Tid',verbose_name='子注单ID3')  # Field name made lowercase.
    parlay4tid = models.BigIntegerField(db_column='Parlay4Tid',verbose_name='子注单ID4')  # Field name made lowercase.
    parlay5tid = models.BigIntegerField(db_column='Parlay5Tid',verbose_name='子注单ID5')  # Field name made lowercase.
    parlay6tid = models.BigIntegerField(db_column='Parlay6Tid',verbose_name='子注单ID6')  # Field name made lowercase.
    odds = CusDecimalField(db_column='Odds',verbose_name='赔率', max_digits=18, decimal_places=2)  # Field name made lowercase.
    stakeamount = CusDecimalField(db_column='StakeAmount',verbose_name='每注金额', max_digits=18, decimal_places=4)  # Field name made lowercase.
    betoutcome = CusDecimalField(db_column='BetOutcome',verbose_name='派彩金额', max_digits=18, decimal_places=4)  # Field name made lowercase.
    winbet = models.SmallIntegerField(db_column='WinBet',verbose_name='中注')  # Field name made lowercase.
    turnover = CusDecimalField(db_column='Turnover',verbose_name='流水', max_digits=18, decimal_places=4)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='建立时间')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_TicketParlay'


class TbTicketstake(models.Model):
    """子注单"""
    tid = models.AutoField(db_column='Tid', primary_key=True,verbose_name='序号')  # Field name made lowercase.
    #ticketid = models.CharField(db_column='TicketID', max_length=20)  # Field name made lowercase.
    ticket_master = models.ForeignKey(TbTicketmaster,db_column='TicketID', db_constraint=False,verbose_name=_(
        'ticket master'))
    stakeid = models.SmallIntegerField(db_column='StakeID')  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    match = models.ForeignKey(TbMatches,db_constraint=False,db_column='MatchID',to_field='matchid')
    #matchid = models.IntegerField(db_column='MatchID',verbose_name='比赛')  # Field name made lowercase.
    dangeroustid = models.BigIntegerField(db_column='DangerousTid')  # Field name made lowercase.
    oddsid = models.BigIntegerField(db_column='OddsID')  # Field name made lowercase.
    specialbetvalue = models.CharField(db_column='SpecialBetValue',verbose_name='让分', max_length=12)  # Field name made lowercase.
    odds = CusDecimalField(db_column='Odds',verbose_name='赔率', max_digits=18, decimal_places=2)  # Field name made lowercase.
    confirmodds = CusDecimalField(db_column='ConfirmOdds',verbose_name='确认赔率', max_digits=18, decimal_places=2)  # Field name made lowercase.
    realodds = CusDecimalField(db_column='RealOdds',verbose_name='真实赔率', max_digits=18, decimal_places=2)  # Field name made lowercase.
    oddsid_ori = models.BigIntegerField(db_column='OddsID_ori')  # Field name made lowercase.
    confirmoddsid_ori = models.BigIntegerField(db_column='ConfirmOddsID_ori',verbose_name='结算值')  # Field name made lowercase.
    voidfactor = models.CharField(db_column='VoidFactor', max_length=10)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status',verbose_name='状态')  # Field name made lowercase.
    rawdata = models.CharField(db_column='RawData', max_length=3000)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='建立时间')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime',verbose_name='更新时间')  # Field name made lowercase.
    confirmoddstid = models.BigIntegerField(db_column='ConfirmOddsTid')  # Field name made lowercase.
    oddskind = models.IntegerField(db_column='OddsKind')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_TicketStake'


class TbTickets(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    match = models.ForeignKey(TbMatches,db_constraint=False,db_column='MatchID') #models.IntegerField(db_column='MatchID')  # Field name made lowercase.
    oddstid = models.IntegerField(db_column='OddsTid')  # Field name made lowercase.
    odds = CusDecimalField(db_column='Odds', max_digits=18, decimal_places=2)  # Field name made lowercase.
    betamount = models.IntegerField(db_column='BetAmount')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    betoutcome = CusDecimalField(db_column='BetOutcome', max_digits=18, decimal_places=2)  # Field name made lowercase.
    turnover = CusDecimalField(db_column='Turnover', max_digits=18, decimal_places=2)  # Field name made lowercase.
    bonuspa = CusDecimalField(db_column='BonusPa', max_digits=18, decimal_places=2)  # Field name made lowercase.
    bonus = CusDecimalField(db_column='Bonus', max_digits=18, decimal_places=2)  # Field name made lowercase.
    rawdata = models.CharField(db_column='RawData', max_length=500, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    settletime = models.DateTimeField(db_column='SettleTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Tickets'


#class TbTokencode(models.Model):
    #tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    #account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    #tokentypeid = models.SmallIntegerField(db_column='TokenTypeID')  # Field name made lowercase.
    #code = models.CharField(db_column='Code', max_length=10)  # Field name made lowercase.
    #tokento = models.CharField(db_column='TokenTo', max_length=50)  # Field name made lowercase.
    #isused = models.SmallIntegerField(db_column='IsUsed')  # Field name made lowercase.
    #createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    #creater = models.CharField(db_column='Creater', max_length=20)  # Field name made lowercase.
    #usetime = models.DateTimeField(db_column='UseTime', blank=True, null=True)  # Field name made lowercase.
    #validtime = models.DateTimeField(db_column='ValidTime', blank=True, null=True)  # Field name made lowercase.

    #class Meta:
        #managed = False
        #db_table = 'TB_TokenCode'


class TbTournament(models.Model):
    tournamentid = models.IntegerField(db_column='TournamentID', primary_key=True)  # Field name made lowercase.
    tournamentname = models.CharField(db_column='TournamentName', max_length=200)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    uniquetournamentid = models.IntegerField(db_column='UniqueTournamentID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Tournament'


class TbTournamentcup(models.Model):
    tournamentid = models.IntegerField(db_column='TournamentID', primary_key=True)  # Field name made lowercase.
    tournamentname = models.CharField(db_column='TournamentName', max_length=200)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate')  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate')  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='UpdateDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_TournamentCup'


class TbTrans(models.Model):
    tranid = models.CharField(db_column='TranID', primary_key=True, max_length=20)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    account = models.CharField(db_column='Account',verbose_name='账号', max_length=20)  # Field name made lowercase.
    channelid = models.ForeignKey(to=TbChannel,db_constraint=False,verbose_name='渠道',db_column='ChannelID')  
    #channelid = models.IntegerField(verbose_name='渠道',db_column='ChannelID')  # Field name made lowercase.
    bankaccountname = models.CharField(db_column='BankAccountName', max_length=20)  # Field name made lowercase.
    bankcardtid = models.IntegerField(db_column='BankCardTid')  # Field name made lowercase.
    cashflow = models.SmallIntegerField(db_column='CashFlow')  # Field name made lowercase.
    amount = CusDecimalField(db_column='Amount',verbose_name='金额', max_digits=18, decimal_places=2)  # Field name made lowercase.
    realamount = CusDecimalField(db_column='RealAmount',verbose_name='实际金额', max_digits=18, decimal_places=2)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=10)  # Field name made lowercase.
    paymentdata = models.CharField(db_column='PaymentData', max_length=2000)  # Field name made lowercase.
    fee = CusDecimalField(db_column='Fee',verbose_name='手续费', max_digits=18, decimal_places=2)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status',verbose_name='状态')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='建立时间')  # Field name made lowercase.
    exectime = models.DateTimeField(db_column='ExecTime',verbose_name='交易时间')  # Field name made lowercase.
    groupcode = models.CharField(db_column='GroupCode', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Trans'


class TbTransWithdraw(models.Model):
    tranid = models.CharField(db_column='TranID', primary_key=True, max_length=20)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    channelid = models.IntegerField(db_column='ChannelID')  # Field name made lowercase.
    bankaccountname = models.CharField(db_column='BankAccountName', max_length=20)  # Field name made lowercase.
    bankcardtid = models.IntegerField(db_column='BankCardTid')  # Field name made lowercase.
    cashflow = models.SmallIntegerField(db_column='CashFlow')  # Field name made lowercase.
    amount = CusDecimalField(db_column='Amount', max_digits=18, decimal_places=2)  # Field name made lowercase.
    realamount = CusDecimalField(db_column='RealAmount', max_digits=18, decimal_places=2)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=10)  # Field name made lowercase.
    paymentdata = models.CharField(db_column='PaymentData', max_length=2000)  # Field name made lowercase.
    fee = CusDecimalField(db_column='Fee', max_digits=18, decimal_places=2)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    rc_memo = models.CharField(db_column='RC_Memo', max_length=500)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    exectime = models.DateTimeField(db_column='ExecTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Trans_Withdraw'


class TbTurnoverMonthlyLog(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    logdate = models.DateTimeField(db_column='LogDate')  # Field name made lowercase.
    turnover = CusDecimalField(db_column='Turnover', max_digits=18, decimal_places=2)  # Field name made lowercase.
    newlv = models.SmallIntegerField(db_column='newLV')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Turnover_Monthly_Log'


class TbTurnoverUselog(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    turnover = CusDecimalField(db_column='Turnover', max_digits=18, decimal_places=2)  # Field name made lowercase.
    usetype = models.SmallIntegerField(db_column='UseType')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=20)  # Field name made lowercase.
    ticketid = models.CharField(db_column='TicketID', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Turnover_UseLog'


class TbVerifylog(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    verifytype = models.SmallIntegerField(db_column='VerifyType')  # Field name made lowercase.
    verifydata = models.CharField(db_column='VerifyData', max_length=200)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_VerifyLog'


class TbVipRescueLog(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    viplv = models.SmallIntegerField(db_column='VIPLv')  # Field name made lowercase.
    netprofit = CusDecimalField(db_column='NetProfit', max_digits=18, decimal_places=2)  # Field name made lowercase.
    returnbonus = CusDecimalField(db_column='ReturnBonus', max_digits=18, decimal_places=2)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Vip_Rescue_Log'


class TbBanner(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.
    picturename = CusPictureField(db_column='PictureName',verbose_name=_('Picture Name'), max_length=255)  # Field name made lowercase
    #picturename = models.CharField(db_column='PictureName',verbose_name=_('Picture Name'), max_length=255)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order',verbose_name=_('Priority'))  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now=True)  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status',verbose_name=_('status'), null=True,choices=ONLINE_STATUS,default=0)  # Field name made lowercase.
    navigateurl = models.CharField(db_column='NavigateUrl', max_length=512,verbose_name=_('Navigate Url'), blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Banner'

class TbWithdrawlimit(models.Model):
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    amount = CusDecimalField(db_column='Amount',verbose_name='提款限额', max_digits=18, decimal_places=4)  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount, db_column='AccountID',primary_key=True, db_constraint=False)  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_WithdrawLimit'


class TbWithdrawlimitlog(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID')  # Field name made lowercase.
    cashflow = models.SmallIntegerField(db_column='CashFlow')  # Field name made lowercase.
    beforeamount = CusDecimalField(db_column='BeforeAmount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    amount = CusDecimalField(db_column='Amount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    afteramount = CusDecimalField(db_column='AfterAmount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    creater = models.CharField(db_column='Creater', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_WithdrawLimitLog'


class Whiteiplist(models.Model):
    whiteiplistid = models.AutoField(db_column='WhiteIpListID', primary_key=True, verbose_name = _('WhiteIpListID'))  # Field name made lowercase.
    ip = models.CharField(db_column='Ip', max_length=16)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200, verbose_name = _('Remark'))  # Field name made lowercase.
    iswork = models.BooleanField(db_column='IsWork', verbose_name = _('IsWork'))  # Field name made lowercase.
    itype = models.IntegerField(db_column='IType')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WhiteIpList'


class Whiteuserlist(models.Model):
    whiteuserlistid = models.AutoField(db_column='WhiteUserListID', primary_key=True, verbose_name = _('WhiteUserListID'))  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True, verbose_name = _('UserName'))  # Field name made lowercase.
    #userid = models.IntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(TbAccount,db_column='UserID',db_constraint=False, verbose_name = _('Account'))
    itype = models.IntegerField(db_column='Itype', blank=True, null=True, verbose_name= _('Itype'))  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=100, blank=True, null=True, verbose_name = _('Memo'))  # Field name made lowercase.
    addtime = models.DateTimeField(db_column='AddTime', blank=True, null=True, verbose_name= _('AddTime'))  # Field name made lowercase.
    iswork = models.BooleanField(db_column='IsWork', verbose_name = _('IsWork'))  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WhiteUserList'
