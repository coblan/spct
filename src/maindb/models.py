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
from .cus_models_fields import CusPictureField, CusFileField,CloudFileField
from helpers.director.model_func.cus_fields.multichoice import MultiChoiceField,MultiChoiceTextField

from helpers.director.model_func.cus_fields.cus_picture import PictureField
from helpers.director.model_func.cus_fields.cus_decimal import CusDecimalField
#from helpers.director.shortcut import FormDatetime

from maindb.create_user import CreateUserField,UpdateUserField
from helpers.director.model_func.validator.integer import int_0_p
from helpers.director.model_func.cus_fields.richtext import RichtextField

class Blackiplist(models.Model):
    blackiplistid = models.AutoField(db_column='BlackIpListID', primary_key=True)  # Field name made lowercase.
    ip = models.CharField(db_column='Ip', max_length=16)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200)  # Field name made lowercase.
    iswork = models.BooleanField(db_column='IsWork')  # Field name made lowercase.
    itype = models.IntegerField(db_column='IType')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BlackIpList'


class Blackiprangelist(models.Model):
    blackiprangelistid = models.AutoField(db_column='BlackIpRangeListID', primary_key=True,
                                          verbose_name=_('ID'))  # Field name made lowercase.
    startip = models.CharField(db_column='StartIp', max_length=16,
                               verbose_name=_('StartIp'))  # Field name made lowercase.
    startipnum = models.BigIntegerField(db_column='StartIpNum',
                                        verbose_name=_('StartIpNum'))  # Field name made lowercase.
    endip = models.CharField(db_column='EndIp', max_length=16, verbose_name=_('EndIp'))  # Field name made lowercase.
    endipnum = models.BigIntegerField(db_column='EndIpNum', verbose_name=_('EndIpNum'))  # Field name made lowercase.

    iswork = models.BooleanField(db_column='IsWork', verbose_name=_('IsWork'),
                                 default=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BlackIpRangeList'


class TbAdvertisement(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    #image = models.CharField(db_column='Image', max_length=255,verbose_name='图片地址')  # Field name made lowercase.
    image = CusPictureField(db_column='Image', max_length=255,verbose_name='图片地址')
    target = models.CharField(db_column='Target',blank=True, max_length=255,verbose_name='跳转地址')  # Field name made lowercase.
    durationseconds = models.IntegerField(db_column='DurationSeconds',verbose_name='持续时间')  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled',verbose_name='启用',default=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Advertisement'


class TbAccount(models.Model):
    accountid = models.IntegerField(db_column='AccountID', primary_key=True,
                                    verbose_name='账号ID')  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=255, verbose_name='手机号码')  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True)  # Field name made lowercase.
    nickname = models.CharField(db_column='NickName', verbose_name='昵称', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status', choices=ACCOUNT_STATUS, null=False,
                                      default=0,verbose_name='用户状态')  # Field name made lowercase.
    agent = models.BigIntegerField(db_column='Agent')  # Field name made lowercase.
    #viplv = models.IntegerField(db_column='VIPLv', verbose_name=_('VIP Level'), choices=VIP_LEVEL, null=False,
                                #default=1)  # Field name made lowercase.
    viplv = models.ForeignKey(to='TbVip',db_column='VIPLv', verbose_name='VIP等级',  null=False,default=0)  # Field name made lowercase.
    
    createtime = models.DateTimeField(db_column='CreateTime', verbose_name='注册时间',
                              auto_now_add=True)  # 
    
    #createtime = FormDatetime(db_column='CreateTime', verbose_name='注册时间',
                              #auto_now_add=True)  # Field name made lowercase.
    pwupdatetime = models.DateTimeField(db_column='PWUpdateTime', auto_now=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4,
                                 verbose_name='游戏账户余额', default=0)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', verbose_name='手机号', max_length=64, blank=True,
                             null=True)  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=255, blank=True)  # Field name made lowercase.
    gender = models.IntegerField(db_column='Gender', default=0)  # Field name made lowercase.
    birthday = models.CharField(db_column='Birthday', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    points = models.IntegerField(db_column='Points', blank=True, null=True)  # Field name made lowercase.
    # actimestamp = models.TextField(db_column='AcTimestamp')  # Field name made lowercase. This field type is a guess.
    codeid = models.IntegerField(db_column='CodeID', default=0)  # Field name made lowercase.
    bonusrate = models.DecimalField(db_column='BonusRate', max_digits=18, decimal_places=4,
                                    verbose_name='反水比例',default=0)  # Field name made lowercase.
    agentamount = models.DecimalField(db_column='AgentAmount', max_digits=18, decimal_places=4, blank=True, null=True,
                                      verbose_name='代理账户余额')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID')  # Field name made lowercase.

    isenablewithdraw = models.BooleanField(db_column='IsEnableWithdraw',
                                           verbose_name='允许提现', default=True)  # Field name made lowercase.
    sumrechargecount = models.IntegerField(db_column='SumRechargeCount',
                                           verbose_name='充值次数', default=0)  # Field name made lowercase.
    fundspassword = models.CharField(db_column='FundsPassword', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    source = models.IntegerField(db_column='Source', verbose_name='来源',
                                 choices=Account_Source, default=3)  # Field name made lowercase.
    sumwithdrawcount = models.IntegerField(db_column='SumWithdrawCount', blank=True,
                                           default=0, verbose_name='提现次数')  # Field name made lowercase.
    accounttype = models.IntegerField(db_column='AccountType',verbose_name='账号类型',choices=ACCOUNT_TYPE)  # Field name made lowercase.
    #groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    groupid = models.ForeignKey(to='TbLimitusergroup',db_constraint=False,db_column='GroupID',verbose_name='用户组',default=0) 
    weight = models.DecimalField(db_column='Weight', max_digits=18, decimal_places=4,verbose_name='权重',default=1)  # Field name made lowercase.
    risklevel = models.IntegerField(db_column='RiskLevel',verbose_name='风控等级',default=1)  # Field name made lowercase.
    isriskleveldown = models.BooleanField(db_column='IsRiskLevelDown',default=False)  # Field name made lowercase.
    cashchannel = models.IntegerField(db_column='CashChannel',verbose_name='允许提款渠道',default=0)  # Field name made lowercase.
    ticketdelay = models.IntegerField(db_column='TicketDelay',verbose_name='注单延时',default=0,validators=[int_0_p])  # Field name made lowercase.
    anomalyticketnum = models.IntegerField(db_column='AnomalyTicketNum',default=0,verbose_name='异常单次数')  # Field name made lowercase.
    lastbettime = models.DateTimeField(db_column='LastBetTime', blank=True, null=True,verbose_name='最后投注时间')  # Field name made lowercase.
    csuserid = models.IntegerField(db_column='CSUserID', blank=True, null=True,verbose_name='所属客服')  # Field name made lowercase.
    powertype = MultiChoiceField(db_column='PowerType',max_length=50,seperator=',',full_choice='-1',blank=True,choices=ACCOUNT_POWERTYPE,verbose_name='允许游戏类型')  # Field name made lowercase.
    #powertype = models.CharField(db_column='PowerType', max_length=50)
    memo = models.TextField(db_column='Memo', blank=True, null=True,verbose_name='备注')  # Field name made lowercase.
    parlayoddscheck = models.BooleanField(db_column='ParlayOddsCheck',verbose_name='串关低赔限制',default=False)  # Field name made lowercase.
    singleoddscheck = models.BooleanField(db_column='SingleOddsCheck',verbose_name='单注低陪限制',default =False)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_Account'

    def __str__(self):
        return self.nickname or ''


class TbAgentrules(models.Model):
    agentruleid = models.AutoField(db_column='AgentRuleID', primary_key=True)  # Field name made lowercase.
    accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID', blank=True, null=True)  # Field name made lowercase.
    daus = models.IntegerField(db_column='DAUs', blank=True, null=True)  # Field name made lowercase.
    minamount = models.DecimalField(db_column='MinAmount', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    maxamount = models.DecimalField(db_column='MaxAmount', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    percentage = models.DecimalField(db_column='Percentage', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AgentRules'
        

class TbAgentqa(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=1024, blank=True, null=True,
                             verbose_name='标题')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', auto_now_add=True,
                                      verbose_name='创建时间')  # Field name made lowercase.
    createuser =CreateUserField(db_column='CreateUser', blank=True, null=True,
                                     verbose_name='创建人')  # Field name made lowe    rcase.
    #createuser = models.IntegerField(db_column='CreateUser', blank=True, null=True,
                                     #verbose_name='创建人')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', choices=ONLINE_STATUS, blank=True, default=1, null=True,
                                 verbose_name='状态')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort', default=0, blank=True, null=True,
                               verbose_name='排序')  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True,
                               verbose_name='内容')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AgentQA'


class TbAdjusttemplate(models.Model):
    templateid = models.AutoField(db_column='TemplateID', primary_key=True,verbose_name='模板ID')  # Field name made lowercase.
    templatename = models.CharField(db_column='TemplateName', max_length=200, blank=False, null=True,verbose_name='模板名')  # Field name made lowercase.
    adjustsettings = models.CharField(db_column='AdjustSettings', max_length=3000, blank=False, null=True,verbose_name='调水设置')  # Field name made lowercase.
    minlimit = models.DecimalField(db_column='MinLimit', max_digits=18, decimal_places=4,verbose_name='最小限制')  # Field name made lowercase.
    maxlimit = models.DecimalField(db_column='MaxLimit', max_digits=18, decimal_places=4,verbose_name='最大限制')  # Field name made lowercase.
    operateuser = UpdateUserField(db_column='OperateUserNo', blank=True, null=True,verbose_name='操作人')  # Field name made lowercase.
    #operateuserno = models.IntegerField(db_column='OperateUserNo', blank=True, null=True)  # Field name made lowercase.
    operatetime = models.DateTimeField(db_column='OperateTime', blank=True, null=True,verbose_name='操作时间',auto_now=True)  #
    status = models.IntegerField(db_column='Status',verbose_name='状态',choices=ZERO_ONE_STATUS,default=1)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200, blank=True, null=True,verbose_name='备注')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'TB_AdjustTemplate'
    
    def __str__(self):
        return self.templatename if self.templatename else ''
        

class TbAccountMatchFav(models.Model):
    accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Account_Match_Fav'
        unique_together = (('accountid', 'matchid'),)


class TbAgaccount(models.Model):
    accountid = models.ForeignKey(to=TbAccount,db_column='AccountId', primary_key=True,verbose_name='账号')
    agusername = models.CharField(db_column='AGUserName', max_length=150,verbose_name='AG用户名')  # Field name made lowercase.
    bonusrate = models.DecimalField(db_column='BonusRate', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='反点率')  # Field name made lowercase.
    transferin = models.DecimalField(db_column='TransferIn', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='转入')  # Field name made lowercase.
    transferout = models.DecimalField(db_column='TransferOut', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='转出')  # Field name made lowercase.
    winorloss = models.DecimalField(db_column='WinOrLoss', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='亏盈')  # Field name made lowercase.
    rebate = models.DecimalField(db_column='Rebate', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='总反水')  # Field name made lowercase.
    availablescores = models.DecimalField(db_column='AvailableScores', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='余额')  # Field name made lowercase.
    fishavailablescores = models.DecimalField(db_column='FishAvailableScores', max_digits=18, decimal_places=4, blank=True, null=True,)  # Field name made lowercase.
    lastfishupdatetime = models.DateTimeField(db_column='LastFishUpdateTime', blank=True, null=True,verbose_name='')  # Field name made lowercase.
    lastagupdatetime = models.DateTimeField(db_column='LastAgUpdateTime', blank=True, null=True,verbose_name='更新时间')  # Field name made lowercase.
    fundswitch = models.BooleanField(db_column='FundSwitch',verbose_name='资金开关')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AgAccount'

class TbAgprofitloss(models.Model):
    profitlossid = models.AutoField(db_column='ProfitLossID', primary_key=True,verbose_name='记录ID')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountId', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountId', blank=True, null=True,verbose_name='账号')  # Field name made lowercase.
    profitlosstime = models.DateTimeField(db_column='ProfitLossTime', blank=True, null=True,verbose_name='游戏时间')  # Field name made lowercase.
    profitlosstype = models.CharField(db_column='ProfitLossType', max_length=50, blank=True, null=True,verbose_name='')  # Field name made lowercase.
    profitlossmoney = models.DecimalField(db_column='ProfitLossMoney', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='投注额')  # Field name made lowercase.
    prizemoney = models.DecimalField(db_column='PrizeMoney', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='派奖额')  # Field name made lowercase.
    winmoney = models.DecimalField(db_column='WinMoney', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='亏盈')  # Field name made lowercase.
   
    memo = models.CharField(db_column='Memo', max_length=500, blank=True, null=True,verbose_name='描述')  # Field name made lowercase.
    playid = models.CharField(db_column='PlayID', max_length=50, blank=True, null=True,verbose_name ='AG游戏ID')  # Field name made lowercase.
    gametype = models.CharField(db_column='GameType', max_length=50, blank=True, null=True,verbose_name='游戏类型')  # Field name made lowercase.
    refid = models.IntegerField(db_column='RefID', blank=True, null=True,verbose_name='')  # Field name made lowercase.
    savetime = models.DateTimeField(db_column='SaveTime', blank=True, null=True,verbose_name='数据保存时间')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID', blank=True, null=True)  # Field name made lowercase.
    bettime = models.DateTimeField(db_column='BetTime', blank=True, null=True)  # Field name made lowercase.
    iswin = models.IntegerField(db_column='IsWin', blank=True, null=True,verbose_name='赢')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True,verbose_name='AG用户名')  # Field name made lowercase.
    validbetamount = models.DecimalField(db_column='ValidBetAmount', max_digits=18, decimal_places=4,verbose_name='有效流水')  # Field name made lowercase.
    rebate = models.DecimalField(db_column='Rebate', max_digits=18, decimal_places=4,verbose_name='返点金额')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AgProfitLoss'


class TbAppresource(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, verbose_name='编号')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, verbose_name='名称')  # Field name made lowercase.
    url = CusFileField(db_column='Url', max_length=255, verbose_name='文件')  # Field name made lowercase.
    isexpired = models.BooleanField(db_column='IsExpired', verbose_name='过期')  # Field name made lowercase.
    md5 = models.CharField(db_column='Md5', max_length=64, verbose_name='散列值')  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True,
                              verbose_name='备注')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', verbose_name='类型')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AppResource'


class TbActivity(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, verbose_name='编号')  # Field name made lowercase.
    indexcover = CusPictureField(db_column='IndexCover', verbose_name = '列表封面', max_length=512, null=True, help_text = '活动列表页面使用')  # Field name made lowercas
    cover = CusPictureField(db_column='Cover', max_length=512, null=True, blank = True, 
                            verbose_name='首页封面', help_text = 'app弹出使用')  # Field name made lowercase.
    zip = models.CharField(db_column='Zip', max_length=512,  null=True, verbose_name='压缩包')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser', blank=True, null=True,
                                     verbose_name='创建人')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', auto_now_add=True,
                                      verbose_name='创建时间')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', null=True, default=1,
                                 choices=ONLINE_STATUS)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True,
                                   verbose_name='优先级')  # Field name made lowercase.
   
    class Meta:
        managed = False
        db_table = 'TB_Activity'


class TbActivityV2(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=128,verbose_name='大标题')  # Field name made lowercase.
    subtitle = models.CharField(db_column='SubTitle', max_length=128,verbose_name='小标题', blank=True, null=True)  # Field name made lowercase.
    timedesp = models.CharField(db_column='TimeDesp', max_length=256,verbose_name='时间描述', blank=True, null=True,help_text='显示在活动页面中')  # Field name made lowercase.
    begintime = models.DateTimeField(db_column='BeginTime',verbose_name='开始时间',help_text='只是被service使用，不会显示在活动页面中')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime',verbose_name='结束时间',help_text='只是被service使用，不会显示在活动页面中')  # Field name made lowercase.
    
    displaytype = models.IntegerField(db_column='DisplayType',default=0,choices=BANNER_DISPLAYTYPE,verbose_name='对内/对外')  # Field name made lowercase.
    
    target = models.CharField(db_column='Target',verbose_name='活动对象', max_length=256, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=2048, blank=True, null=True,verbose_name='活动详情')  # Field name made lowercase.
    rules = models.CharField(db_column='Rules', max_length=3000,verbose_name='规则')  # Field name made lowercase.
    banner = CusPictureField(db_column='Banner', max_length=512, blank=True, null=True,verbose_name='列表封面')  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=512)  # Field name made lowercase.
    componentname = models.CharField(db_column='ComponentName', max_length=64, blank=True, null=True,verbose_name='前端组件名',choices=ACTIVITY_COM,help_text='注意首存再存等活动，必须选择对应的前端组件')  # Field name made lowercase.
    componentparams = models.CharField(db_column='ComponentParams', max_length=4000, blank=True, null=True,verbose_name='前端组件参数')  # Field name made lowercase.
    templateid = models.IntegerField(db_column='TemplateId',verbose_name='程序集',default=0)  # Field name made lowercase.
    #templateid = models.ForeignKey(to='TbActivityTemplate',db_constraint=False,db_column='TemplateId',verbose_name='程序集',blank=True)  # Field name made lowercase.
    ismutex = models.BooleanField(db_column='IsMutex',verbose_name='与其他活动互斥')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort',verbose_name='排序')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True,verbose_name='创建时间')  # Field name made lowercase.
    edittime = models.DateTimeField(db_column='EditTime',auto_now=True,verbose_name='更新时间')  # Field name made lowercase.
    creatorid = CreateUserField(db_column='CreatorId',verbose_name='创建者')  # Field name made lowercase.
    editorid= UpdateUserField(db_column='EditorId',verbose_name='修改人')
    #editorid = models.IntegerField(db_column='EditorId')  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=1024, blank=True, null=True,verbose_name='活动备注')  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled',verbose_name='启用')  # Field name made lowercase.
    #image = models.CharField(db_column='Image', max_length=512, blank=True, null=True)  # Field name made lowercase.
    image = CusPictureField(db_column='Image', max_length=512, blank=True, null=True,verbose_name='首页弹出图')  # Field name made lowercase.
   
    
    
    class Meta:
        managed = False
        db_table = 'TB_Activity_V2'
    
    def __str__(self):
        return self.title


class TbActivityRecord(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    #activityid = models.IntegerField(db_column='ActivityId')  # Field name made lowercase.
    activity = models.ForeignKey(to=TbActivityV2,db_constraint=False,db_column='ActivityId',verbose_name = '活动')  
    bid = models.BigIntegerField(db_column='BId')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountId')  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_constraint=False,to_field='accountid',db_column='AccountId',verbose_name='用户') 
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='生成时间')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=38, decimal_places=4,verbose_name='金额')  # Field name made lowercase.
    turnover = models.DecimalField(db_column='Turnover', max_digits=38, decimal_places=4,verbose_name='流水')  # Field name made lowercase.
    bonus = models.DecimalField(db_column='Bonus', max_digits=38, decimal_places=4,verbose_name='奖金')  # Field name made lowercase.
    state = models.IntegerField(db_column='State',verbose_name='状态',choices=ACTIVITY_RECORD_STATE)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Activity_Record'
        

class TbActivitySettings(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    activityid = models.ForeignKey(db_column='ActivityId',to=TbActivityV2,db_constraint=False)  # Field name made lowercase.
    #activityid = models.IntegerField(db_column='ActivityId')  # Field name made lowercase.
    friendlyname = models.CharField(db_column='FriendlyName', max_length=64,verbose_name='名称')  # Field name made lowercase.
    key = models.CharField(db_column='Key', max_length=64,verbose_name='键')  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=1024,verbose_name='值')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=1024, blank=True, null=True,verbose_name='描述')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Activity_Settings'

class TbActivityTemplate(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=128)  # Field name made lowercase.
    assembly = models.CharField(db_column='Assembly', max_length=128)  # Field name made lowercase.
    typefullname = models.CharField(db_column='TypeFullName', max_length=128)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Activity_Template'
    
    def __str__(self):
        return self.title

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
    terminal = models.IntegerField(db_column='Terminal', choices=PLATFORM,
                                   verbose_name='终端')  # Field name made lowercase.
    packageurl = models.CharField(db_column='PackageUrl', max_length=255, blank=True,
                                  null=True, verbose_name='文件')  # Field name made lowercase.
    md5 = models.CharField(db_column='Md5', max_length=32, blank=True, null=True,
                           verbose_name='散列值')  # Field name made lowercase.
    versionid = models.IntegerField(db_column='VersionId', default=0, verbose_name='版本ID')  # Field name made lowercase.
    versionname = models.CharField(db_column='VersionName', max_length=64, blank=False,
                                   verbose_name='版本名称')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=512, blank=True,
                                   null=True, verbose_name='描述')  # Field name made lowercase.
    required = models.IntegerField(db_column='Required', verbose_name=_('Force Update'), default=0,
                                   choices=REQUIRED)  # Field name made lowercase.
    size = models.FloatField(db_column='Size', default=0, verbose_name='大小')  # Field name made lowercase.
    valid = models.BooleanField(db_column='Valid', verbose_name='状态')  # Field name made lowercase.
    plisturl = models.CharField(db_column='PListUrl', max_length=200, blank=True,
                                null=True)  # Field name made lowercase.
    minversionname = models.CharField(db_column='MinVersionName', max_length=64, blank=True, null=True,verbose_name='最小版本号')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tb_AppVersion'

class TbBackendwhiteip(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    startip = models.CharField(db_column='StartIp', max_length=16,  null=True,verbose_name='开始IP')  # Field name made lowercase.
    startipnum = models.BigIntegerField(db_column='StartIpNum', blank=True, null=True)  # Field name made lowercase.
    endip = models.CharField(db_column='EndIp', max_length=16,  null=True,verbose_name='结束IP')  # Field name made lowercase.
    endipnum = models.BigIntegerField(db_column='EndIpNum', blank=True, null=True)  # Field name made lowercase.
    iswork = models.BooleanField(db_column='IsWork',verbose_name='启用')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BackendWhiteIP'

class TbBackendloginlog(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId',verbose_name='管理员ID')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50,verbose_name='管理员')  # Field name made lowercase.
    ipaddress = models.CharField(db_column='IPAddress', max_length=20,verbose_name='ip地址')  # Field name made lowercase.
    area = models.CharField(db_column='Area', max_length=200, blank=True, null=True,verbose_name="区域")  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='登录时间',auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BackendLoginLog'

class TbBalance(models.Model):
    # accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
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
    # accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    account = models.CharField(db_column='Account', verbose_name=_('Account'),
                               max_length=20)  # Field name made lowercase.
    categoryid = models.ForeignKey(to='TbMoneyCategories', verbose_name='类型', db_column='CategoryID',
                                   db_constraint=False, null=True, blank=True)  # Field name made lowercase.
    cashflow = models.SmallIntegerField(db_column='CashFlow')  # Field name made lowercase.
    beforeamount = CusDecimalField(db_column='BeforeAmount', verbose_name=_('BeforeAmount'), max_digits=18,
                                   decimal_places=4)  # Field name made lowercase.
    amount = CusDecimalField(db_column='Amount', verbose_name=_('ChangedAmount'), max_digits=18,
                             decimal_places=4)  # Field name made lowercase.
    afteramount = CusDecimalField(db_column='AfterAmount', verbose_name=_('AfterAmount'), max_digits=18,
                                  decimal_places=4)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', verbose_name='备注', max_length=50, blank=True,
                            null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(verbose_name=_('Change Time'),
                                      db_column='CreateTime', auto_now=True)  # Field name made lowercase.
    creater = models.CharField(db_column='Creater', verbose_name=_('Operator'), max_length=20, blank=True,
                               null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount, db_column='AccountID',
                                  db_constraint=False, verbose_name='用户昵称', blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BalanceLog'


class TbBankcard(models.Model):
    bankcardid = models.AutoField(db_column='BankCardId', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount, db_column='AccountId',
                                  db_constraint=False)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=50)  # Field name made lowercase.
    banktypeid = models.IntegerField(db_column='BankTypeID')  # Field name made lowercase.
    cardno = models.CharField(db_column='CardNo', max_length=50)  # Field name made lowercase.
    bankaccountname = models.CharField(db_column='BankAccountName', max_length=50)  # Field name made lowercase.
    bankaccountmobil = models.CharField(db_column='BankAccountMobil', max_length=50)  # Field name made lowercase.
    bankcity = models.CharField(db_column='BankCity', max_length=50)  # Field name made lowercase.
    banktypename = models.CharField(db_column='BankTypeName', max_length=150)  # Field name made lowercase.
    bankprovince = models.CharField(db_column='BankProvince', max_length=150)  # Field name made lowercase.
    banksitename = models.CharField(db_column='BankSiteName', max_length=250)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    active = models.BooleanField(db_column='Active')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BankCard'


# class TbBanktype(models.Model):
# banktypeid = models.IntegerField(db_column='BankTypeID', primary_key=True)  # Field name made lowercase.
# banktypename = models.CharField(db_column='BankTypeName', max_length=50, blank=True,
# null=True)  # Field name made lowercase.
# moneyintype = models.IntegerField(db_column='MoneyInType', blank=True, null=True)  # Field name made lowercase.

# class Meta:
# managed = False
# db_table = 'TB_BankType'

# class TbBanktypes(models.Model):
# banktypeid = models.AutoField(db_column='BankTypeID', primary_key=True)  # Field name made lowercase.
# banktypename = models.CharField(db_column='BankTypeName', max_length=50)  # Field name made lowercase.
# active = models.BooleanField(db_column='Active')  # Field name made lowercase.
# img = models.CharField(db_column='Img', max_length=200, blank=True, null=True)  # Field name made lowercase.
# sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.

# class Meta:
# managed = False
# db_table = 'TB_BankTypes'


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
    username = models.CharField(db_column='UserName', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=100)  # Field name made lowercase.
    addtime = models.DateTimeField(db_column='AddTime', blank=True, null=True)  # Field name made lowercase.
    ban_status = models.SmallIntegerField(db_column='Ban_Status', blank=True, null=True)  # Field name made lowercase.

    # adduser = models.CharField(db_column='AddUser', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BlackUserList'


class TbBlackuserlistLog(models.Model):
    blacklogid = models.IntegerField(db_column='BlackLogID')  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=100, blank=True, null=True)  # Field name made lowercase.
    addtime = models.DateTimeField(db_column='AddTime', blank=True, null=True)  # Field name made lowercase.
    before_ban_status = models.SmallIntegerField(db_column='Before_Ban_Status', blank=True,
                                                 null=True)  # Field name made lowercase.
    alter_ban_status = models.SmallIntegerField(db_column='Alter_Ban_Status', blank=True,
                                                null=True)  # Field name made lowercase.
    modify_user = models.CharField(db_column='Modify_user', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BlackUserList_Log'
        
        
RFTYPE=((1,'充值'),(2,'后台调整'),(3,'活动赠送'))
CONSUMSTATUS=((1,'等待消耗'),(2,'消耗完毕'))
class TbBetfullrecord(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    rfid = models.BigIntegerField(db_column='RfID', blank=True, null=True)  # Field name made lowercase.
    rftype = models.IntegerField(db_column='RfType',verbose_name='类型',choices=RFTYPE)  # Field name made lowercase.
    consumeamount = models.DecimalField(db_column='ConsumeAmount',verbose_name='剩余限额', max_digits=18, decimal_places=4)  # Field name made lowercase.
    consumestatus = models.IntegerField(db_column='ConsumeStatus',verbose_name='消费状态',choices=CONSUMSTATUS)  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount,db_constraint=False, db_column='AccountID')  # Field name made lowercase.
    #accountid = models.BigIntegerField(db_column='AccountID')  # Field name made lowercase.
    content = models.CharField(db_column='Content',verbose_name='详细说明', max_length=150, blank=True, null=True)  # Field name made lowercase.
    
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='创建时间', blank=True, null=True,auto_now=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount',verbose_name='原始限额', max_digits=18, decimal_places=4)  # Field name made lowercase.
    fundtype = models.IntegerField(db_column='FundType',default=0)  # Field name made lowercase.
    turnover = models.DecimalField(db_column='Turnover', max_digits=18, decimal_places=4)  # Field name made lowercase.
    multiple = models.DecimalField(db_column='Multiple', max_digits=18, decimal_places=1)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_BetFullRecord'



class TbBetstopreason(models.Model):
    id = models.IntegerField(primary_key=True,db_column='ID')
    description = models.CharField(max_length=2000, db_column='Description',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_BetStopReason'


class TbBonustype(models.Model):
    bonustypeid = models.AutoField(db_column='BonusTypeID',primary_key=True,verbose_name='红利ID')  # Field name made lowercase.
    bonustypename = models.CharField(db_column='BonusTypeName', max_length=50,verbose_name='红利名称')  # Field name made lowercase.
    withdrawlimitmultiple = models.DecimalField(db_column='WithdrawLimitMultiple', max_digits=18, decimal_places=4,verbose_name='倍数')  # Field name made lowercase.
    #createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createuser = CreateUserField(db_column='CreateUser',verbose_name='创建人',blank=True,null=True)  #
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True,verbose_name='创建时间')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BonusType'
    
    def __str__(self):
        return self.bonustypename

class TbBonuslog(models.Model):
    id = models.AutoField(db_column='Id',primary_key=True,)  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID',verbose_name='账号')  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountID',verbose_name='昵称')  # Field name made lowercase
    bonustypeid = models.ForeignKey(to=TbBonustype,db_column='BonusTypeID',verbose_name='红利类型')  # Field name made lowercase.
    #bonustypeid = models.IntegerField(db_column='BonusTypeID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4,verbose_name='金额')  # Field name made lowercase.
    withdrawlimitamount = models.DecimalField(db_column='WithdrawLimitAmount', max_digits=18, decimal_places=4,verbose_name='提款限额增加')  # Field name made lowercase.
    createuser = CreateUserField(db_column='CreateUser',verbose_name='操作人',blank=True,null=True) # models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True,verbose_name='时间')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=100, blank=True, null=True,verbose_name='备注')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BonusLog'
            
            
class TbCategory(models.Model):
    categoryid = models.IntegerField(db_column='CategoryID', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', max_length=200)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Category'


class TbChannel(models.Model):
    channelid = models.IntegerField(db_column='ChannelID', verbose_name='渠道ID',
                                    primary_key=True)  # Field name made lowercase.
    channel = models.IntegerField(db_column='Channel', verbose_name=_('Channel'),
                                  unique=True)  # Field name made lowercase.
    channelname = models.CharField(db_column='ChannelName', verbose_name=_('Channel Name'),
                                   max_length=30)  # Field name made lowercase.
    # channelgroup = models.CharField(db_column='ChannelGroup', verbose_name='渠道群组',max_length=20)  # Field name made lowercase.
    # cashflow = models.SmallIntegerField(db_column='CashFlow',verbose_name='存提状态',choices=CHANNEL_CASHFLOW,default=0)  # Field name made lowercase.
    # returntype = models.CharField(db_column='ReturnType',verbose_name='回传类型', max_length=10)  # Field name made lowercase.
    maxlimit = CusDecimalField(db_column='MaxLimit', verbose_name=_('Max Limit Amount'), max_digits=18,
                               decimal_places=4)  # Field name made lowercase.
    minlimit = CusDecimalField(db_column='MinLimit', verbose_name=_('Min Limit Amount'), max_digits=18,
                               decimal_places=4)  # Field name made lowercase.
    grouptitle = models.CharField(db_column='GroupTitle', verbose_name=_('Group Title'),
                                  max_length=20)  # Field name made lowercase.
    # btnname = models.CharField(db_column='BtnName',verbose_name='类型名', max_length=20)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status', verbose_name=_('Status'), choices=CHANNEL_STATUS,
                                      default=0)  # Field name made lowercase.
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


class TbCurrency(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    price = models.IntegerField(db_column='Price', verbose_name='价格', help_text='单位(分)')  # Field name made lowercase.
    value = CusDecimalField(db_column='Value', max_digits=18, decimal_places=4, verbose_name='金币数',
                            help_text='可以为小数')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    icon = CusPictureField(db_column='Icon', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Currency'


class TbChargeflow(models.Model):
    id = models.BigIntegerField(db_column='Id', primary_key=True, verbose_name=_('ID'))  # Field name made lowercase.
    channel = models.ForeignKey(to=TbChannel, to_field='channel', db_constraint=False, db_column='Channel',
                                verbose_name=_('Channel'))
    # channel = models.IntegerField(db_column='Channel')  # Field name made lowercase.
    productid = models.IntegerField(db_column='ProductId', verbose_name=_('ProductId'))  # Field name made lowercase.
    createtime = models.CharField(db_column='CreateTime', max_length=27,
                                  verbose_name=_('CreateTime'))  # Field name made lowercase.
    callbacktime = models.CharField(db_column='CallbackTime', max_length=27, blank=True, null=True,
                                    verbose_name=_('CallbackTime'))  # Field name made lowercas
    accountid = models.ForeignKey(to=TbAccount, db_constraint=False, db_column='AccountId', verbose_name=_('Account'))
    # accountid = models.IntegerField(db_column='AccountId')  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount', verbose_name=_('Amount'))  # Field name made lowercase.
    success = models.IntegerField(db_column='Success', verbose_name=_('Success'))
    credential = models.CharField(db_column='Credential', max_length=2048,
                                  verbose_name=_('Credential'))  # Field name made lowercase.
    error = models.CharField(db_column='Error', max_length=4096, blank=True, null=True)  # Field name made lowercase.
    providerid = models.CharField(db_column='ProviderId', max_length=64, blank=True,
                                  null=True)  # Field name made lowercase.
    currency = CusDecimalField(db_column='Currency', max_digits=18, decimal_places=0,
                               verbose_name=_('Currency'))  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=255, blank=True, null=True,
                              verbose_name=_('Remark'))  # Field name made lowercase.

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


class TbDomain(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=255,verbose_name='域名')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status',default=1,choices=ZERO_ONE_STATUS,verbose_name='状态')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Domain'


class TbD9Userhttpreferer(models.Model):
    d9userhttprefererid = models.AutoField(db_column='D9UserHttpRefererID',
                                           primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=12)  # Field name made lowercase.
    referrer = models.CharField(db_column='Referrer', max_length=512)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=64)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_D9UserHttpReferer'


class TbEventbonusLog(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    # accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    eventid = models.IntegerField(db_column='EventID')  # Field name made lowercase.
    totalturnover = CusDecimalField(db_column='TotalTurnover', max_digits=18,
                                    decimal_places=4)  # Field name made lowercase.
    nowturnover = CusDecimalField(db_column='NowTurnover', max_digits=18,
                                  decimal_places=4)  # Field name made lowercase.
    bonus = CusDecimalField(db_column='Bonus', max_digits=18, decimal_places=4)  # Field name made lowercase.
    addwithdrawlimit = CusDecimalField(db_column='AddWithdrawLimit', max_digits=18,
                                       decimal_places=4)  # Field name made lowercase.
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
    turnovermultiple = CusDecimalField(db_column='TurnoverMultiple', max_digits=18,
                                       decimal_places=2)  # Field name made lowercase.
    withdrawlimitmultiple = CusDecimalField(db_column='WithdrawlimitMultiple', max_digits=18,
                                            decimal_places=2)  # Field name made lowercase.
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


class TbGamemoneyininfo(models.Model):
    moneyinid = models.AutoField(db_column='MoneyInID', primary_key=True,verbose_name='记录ID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='金额')  # Field name made lowercase.
    orderid = models.CharField(db_column='OrderID', max_length=50, blank=True, null=True,verbose_name='订单号')  # Field name made lowercase.
    ordertime = models.DateTimeField(db_column='OrderTime', blank=True, null=True,verbose_name='时间')  # Field name made lowercase.
    handle = models.CharField(db_column='Handle', max_length=50, blank=True, null=True,verbose_name='操作者')  # Field name made lowercase.
    handtime = models.DateTimeField(db_column='HandTime', blank=True, null=True,verbose_name='操作时间')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True,verbose_name='账号')  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountID', blank=True, null=True,verbose_name='账号')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True,verbose_name='用户名')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True,verbose_name='状态',choices=GAMEMONEY_IN_STATUS)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=2000, blank=True, null=True,verbose_name='备注')  # Field name made lowercase.
    #tsamp = models.TextField(db_column='Tsamp', blank=True, null=True,)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'TB_GameMoneyInInfo'

class TbGamemoneyoutinfo(models.Model):
    moneyoutid = models.AutoField(db_column='MoneyOutID', primary_key=True,verbose_name='记录ID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='金额')  # Field name made lowercase.
    orderid = models.CharField(db_column='OrderID', max_length=50, blank=True, null=True,verbose_name='订单号')  # Field name made lowercase.
    ordertime = models.DateTimeField(db_column='OrderTime', blank=True, null=True,verbose_name='时间')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountID', blank=True, null=True,verbose_name='账号')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True,verbose_name='AG用户名')  # Field name made lowercase.
    handle = models.CharField(db_column='Handle', max_length=50, blank=True, null=True,verbose_name='操作者')  # Field name made lowercase.
    handtime = models.DateTimeField(db_column='HandTime', blank=True, null=True,verbose_name='操作时间')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True,choices=GAMEMONEY_OUT_STATUS,verbose_name='状态')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=2000, blank=True, null=True,verbose_name='备注')  # Field name made lowercase.
    #tsamp = models.TextField(db_column='Tsamp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'TB_GameMoneyOutInfo'

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
    accountid = models.ForeignKey(to=TbAccount, db_constraint=False,
                                  db_column='AccountId', verbose_name='账号')  # Field name made lowercase.
    # accountid = models.IntegerField(db_column='AccountId')  # Field name made lowercase.
    devicecode = models.CharField(db_column='DeviceCode', verbose_name=_('Device Code'),
                                  max_length=40)  # Field name made lowercase.
    deviceip = models.CharField(db_column='DeviceIP', verbose_name=_('Device Ip'),
                                max_length=20)  # Field name made lowercase.
    # devicecode = models.CharField(db_column='DeviceCode', max_length=40, blank=True, null=True)  # Field name made lowercase.
    # deviceip = models.CharField(db_column='DeviceIP', max_length=20)  # Field name made lowercase.
    ternimal = models.IntegerField(db_column='Ternimal', verbose_name=_('Terminal'))  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',
                                      verbose_name=_('Login Time'))  # Field name made lowercase.
    appversion = models.CharField(db_column='AppVersion', verbose_name='App版本', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    devicename = models.CharField(db_column='DeviceName', max_length=40, blank=True,
                                  null=True, verbose_name='设备名称')  # Field name made lowercase.
    deviceversion = models.CharField(db_column='DeviceVersion', max_length=20, blank=True,
                                     null=True, verbose_name='设备版本号')  # Field name made lowercase.
    logintype = models.IntegerField(db_column='LoginType', verbose_name='登录方式')  # Field name made lowercase.
    area = models.CharField(db_column='Area', max_length=200, blank=True, null=True,
                            verbose_name='地区')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_LoginLog'


class TbLimitusergroup(models.Model):
    groupid = models.IntegerField(db_column='GroupID', primary_key=True,verbose_name='分组ID')  # Field name made lowercase.
    groupname = models.CharField(db_column='GroupName', max_length=200,verbose_name='分组名')  # Field name made lowercase.
    betbase = models.DecimalField(db_column='BetBase', max_digits=18, decimal_places=4,verbose_name='限额基数')  # Field name made lowercase.
    singleweight = models.DecimalField(db_column='SingleWeight', max_digits=18, decimal_places=4,verbose_name='单注权重系数')  # Field name made lowercase.
    betmatch = models.DecimalField(db_column='BetMatch', max_digits=18, decimal_places=4,verbose_name='单场限额系数')  # Field name made lowercase.
    enable = models.BooleanField(db_column='Enable',verbose_name='启用')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True,verbose_name='描述')  # Field name made lowercase.
    extension = models.CharField(db_column='Extension', max_length=300, blank=True, null=True,verbose_name='颜色')  # Field name made lowercase.
    ticketdelay = models.IntegerField(db_column='TicketDelay',verbose_name='注单延时',default=0,validators=[int_0_p])  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_LimitUserGroup'
    
    def __str__(self):
        return self.groupname

class TbLimit(models.Model):
    tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    # matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    matchid = models.ForeignKey(to='TbMatch', db_constraint=False, to_field='matchid', db_column='MatchID',
                                verbose_name='比赛')  # Field name made lowercase.
    limittype = models.IntegerField(db_column='LimitType', choices=LIMIT_TYPE, default=11,
                                    verbose_name='玩法控制')  # Field name made lowercase.
    # accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(to='TbAccount', verbose_name='账号', db_constraint=True, to_field='accountid',
                                  db_column='AccountID', blank=True, null=True)  #
    relationno = models.IntegerField(db_column='RelationNo', verbose_name='玩法/等级', blank=True,
                                     default=0)  # Field name made lowercase.
    maxsinglepayout = models.DecimalField(verbose_name='最大赔付值', db_column='MaxSinglePayout', max_digits=18,
                                          decimal_places=2, null=True, default=0)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True, default=1,
                                 verbose_name='启用')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True,
                                   null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True, auto_now_add=True,
                                      editable=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime', blank=True, null=True, auto_now=True,
                                      editable=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Limit'


class TbLivescout(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    servertime = models.DateTimeField(db_column='ServerTime',auto_now_add=True,verbose_name='服务器时间')  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchId',verbose_name='比赛ID')  # Field name made lowercase.
    eventid = models.CharField(db_column='EventId', max_length=50)  # Field name made lowercase.
    matchstatus = models.CharField(db_column='MatchStatus', max_length=50)  # Field name made lowercase.
    matchstatusid = models.IntegerField(db_column='MatchStatusId')  # Field name made lowercase.
    scoutfeedtype = models.IntegerField(db_column='ScoutFeedType')  # Field name made lowercase.
    betstatus = models.IntegerField(db_column='BetStatus',verbose_name='投注状态')  # Field name made lowercase.
    side = models.IntegerField(db_column='Side',default=0)  # Field name made lowercase.
    typeid = models.IntegerField(db_column='TypeId')  # Field name made lowercase.
    matchtime = models.CharField(db_column='MatchTime', max_length=50, blank=True, null=True,verbose_name='比赛时间')  # Field name made lowercase.
    matchscore = models.CharField(db_column='MatchScore', max_length=50, blank=True, null=True,verbose_name='比赛分数')  # Field name made lowercase.
    player1 = models.BigIntegerField(db_column='Player1',default=0)  # Field name made lowercase.
    player2 = models.BigIntegerField(db_column='Player2',default=0)  # Field name made lowercase.
    posx = models.IntegerField(db_column='PosX',default=0)  # Field name made lowercase.
    posy = models.IntegerField(db_column='PosY',default=0)  # Field name made lowercase.
    brextrainfo = models.CharField(db_column='BrExtraInfo', max_length=150,verbose_name='产生原因')  # Field name made lowercase.
    eventtypeid = models.IntegerField(db_column='EventTypeId')  # Field name made lowercase.
    extrainfo = models.IntegerField(db_column='ExtraInfo',default=0)  # Field name made lowercase.
    eventdesc = models.CharField(db_column='EventDesc', max_length=150, blank=True, null=True,verbose_name='事件描述')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True,verbose_name='创建时间')  # Field name made lowercase.
    remainingtimeinperiod = models.CharField(db_column='RemainingTimeInPeriod', max_length=20, blank=True, null=True)  # Field name made lowercase.
    periodnumber = models.IntegerField(db_column='PeriodNumber', blank=True, null=True)  # Field name made lowercase.
    periodscore = models.CharField(db_column='PeriodScore', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_LiveScout'

class TbLivefeed(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportId',verbose_name='体育类型')  # Field name made lowercase.
    livefeedid = models.BigIntegerField(db_column='LiveFeedId',verbose_name='FeedID')  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchId')  # Field name made lowercase.
    eventid = models.BigIntegerField(db_column='EventId')  # Field name made lowercase.
    eventtypeid = models.IntegerField(db_column='EventTypeId',verbose_name='')  # Field name made lowercase.
    extrainfo = models.IntegerField(db_column='ExtraInfo')  # Field name made lowercase.
    side = models.IntegerField(db_column='Side')  # Field name made lowercase.
    matchtime = models.CharField(db_column='MatchTime', max_length=32, blank=True, null=True,verbose_name='比赛时间')  # Field name made lowercase.
    matchscore = models.CharField(db_column='MatchScore', max_length=32, blank=True, null=True,verbose_name='比分')  # Field name made lowercase.
    eventdesc = models.CharField(db_column='EventDesc', max_length=255, blank=True, null=True,verbose_name='描述')  # Field name made lowercase.
    eventdesczh = models.CharField(db_column='EventDescZh', max_length=255, blank=True, null=True)  # Field name made lowercase.
    statuscode = models.IntegerField(db_column='StatusCode')  # Field name made lowercase.
    betstatus = models.IntegerField(db_column='BetStatus',verbose_name='投注状态')  # Field name made lowercase.
    servertime = models.DateTimeField(db_column='ServerTime',auto_now=True,verbose_name='服务器时间')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now=True,verbose_name='创建时间')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Livefeed'


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

WINNER_TYPE=(
    (0,''),
    (1,'主胜'),
    (2,'客胜'),
    (3,'平局'),
)

class TbMatch(models.Model):
    sportid = models.IntegerField(db_column='SportID',verbose_name='运动类型')  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID', primary_key=True,verbose_name='比赛ID')  # Field name made lowercase.
    eventid = models.CharField(db_column='EventID', unique=True, max_length=50)  # Field name made lowercase.
    tournamentid = models.IntegerField(db_column='TournamentID',verbose_name='联赛')  # Field name made lowercase.
    uniquetournamentid = models.IntegerField(db_column='UniqueTournamentId')  # Field name made lowercase.
    roundinfo = models.IntegerField(db_column='RoundInfo')  # Field name made lowercase.
    team1id = models.IntegerField(db_column='Team1ID')  # Field name made lowercase.
    team1en = models.CharField(db_column='Team1EN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    team1zh = models.CharField(db_column='Team1ZH', max_length=100, blank=True, null=True,verbose_name='主队')  # Field name made lowercase.
    team2id = models.IntegerField(db_column='Team2ID')  # Field name made lowercase.
    team2en = models.CharField(db_column='Team2EN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    team2zh = models.CharField(db_column='Team2ZH', max_length=100, blank=True, null=True,verbose_name='客队')  # Field name made lowercase.
    prematchdate = models.DateTimeField(db_column='PreMatchDate')  # Field name made lowercase.
    matchdate = models.DateTimeField(db_column='MatchDate',verbose_name='比赛日期')  # Field name made lowercase.
    marketstatus = models.IntegerField(db_column='MarketStatus',choices=MATCH_MARKETSTATUS,
                                       verbose_name='市场状态')  # Field name made lowercase.
    statuscode = models.IntegerField(db_column='StatusCode',verbose_name='状态',
                                     choices=NEW_MATCH_STATUS)  # Field name made lowercase.
    score = models.CharField(db_column='Score', max_length=20, blank=True, null=True,verbose_name='比分')  # Field name made lowercase.
    hasliveodds = models.BooleanField(db_column='HasLiveOdds',verbose_name='走地盘')  # Field name made lowercase.
    isrecommend = models.BooleanField(db_column='IsRecommend',verbose_name='推荐')  # Field name made lowercase.
    ishidden = models.BooleanField(db_column='IsHidden',verbose_name='隐藏')  # Field name made lowercase.
    iscloseliveodds = models.IntegerField(db_column='IsCloseLiveOdds', blank=True, null=True)  # Field name made lowercase.
    winner = models.IntegerField(db_column='Winner',verbose_name='胜者',choices=WINNER_TYPE)  # Field name made lowercase.
    terminator = models.CharField(db_column='Terminator', max_length=20, blank=True, null=True)  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=18, decimal_places=4, blank=True, null=True ,verbose_name='权重')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime', blank=True, null=True)  # Field name made lowercase.
    ticketdelay = models.IntegerField(db_column='TicketDelay',verbose_name='注单延时',default=0,validators=[int_0_p])  # Field name made lowercase.
    isdangerous = models.IntegerField(db_column='IsDangerous', blank=True, null=True,verbose_name='危险球')  # Field name made lowercase.
   
    oddsadjustment = models.DecimalField(db_column='OddsAdjustment', max_digits=2, decimal_places=2,verbose_name='赔率调整值')  # Field name made lowercase.
    oddsadjustmax = models.DecimalField(db_column='OddsAdjustMax', max_digits=2, decimal_places=2,verbose_name='赔率调整最大值')  # Field name made lowercase.
    baseticketeamout = models.DecimalField(db_column='BaseTicketeAmout', max_digits=18, decimal_places=2,verbose_name='投注差额基数',help_text='每投注X元赔率调整一次')  # Field name made lowercase.
    coveragesource = models.CharField(db_column='CoverageSource', max_length=16, blank=True, null=True)  # Field name made lowercase.
    coveragelevel = models.CharField(db_column='CoverageLevel', max_length=16, blank=True, null=True)  # Field name made lowercase.
    source = models.IntegerField(db_column='Source',choices=MATCH_SOURCE,verbose_name='数据源')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_Match'
        
    def __str__(self):
        return '[%(matchid)s]%(home)s vs %(away)s' % {'matchid': self.matchid, 'home': self.team1zh,
                                                     'away': self.team2zh, }

#class TbMatches(models.Model):
    #"""老表，废弃"""
    #tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    #categoryid = models.IntegerField(db_column='CategoryID',
                                     #verbose_name=_('Match Category'))  # Field name made lowercase.
    #tournamentid = models.IntegerField(db_column='TournamentID')  # Field name made lowercase.
    ##tournamentid = models.ForeignKey(to='TbTournament', db_constraint=False, db_column='TournamentID')
    #tournamentzh = models.CharField(db_column='TournamentZH', verbose_name=_('Tournament'),
                                    #max_length=50)  # Field name made lowercase.
    #matchid = models.IntegerField(db_column='MatchID', unique=True)  # Field name made lowercase.
    #prematchdate = models.DateTimeField(db_column='PreMatchDate')  # Field name made lowercase.
    #matchdate = models.DateTimeField(db_column='MatchDate', verbose_name=_('Match Date'))  # Field name made lowercase.
    #currentperiodstart = models.DateTimeField(db_column='CurrentPeriodStart', verbose_name=_('CurrentPeriodStart'),
                                              #blank=True, null=True)  # 结束时间 Field name made lowercase.
    #team1id = models.IntegerField(db_column='Team1ID')  # Field name made lowercase.
    #superteam1id = models.BigIntegerField(db_column='SuperTeam1Id')  # Field name made lowercase.
    #team1zh = models.CharField(db_column='Team1ZH', verbose_name=_('Home Team'),
                               #max_length=100)  # Field name made lowercase.
    #team2id = models.IntegerField(db_column='Team2ID')  # Field name made lowercase.
    #superteam2id = models.BigIntegerField(db_column='SuperTeam2Id')  # Field name made lowercase.
    #team2zh = models.CharField(db_column='Team2ZH', verbose_name=_('Away Team'),
                               #max_length=100)  # Field name made lowercase.
    #matchscore = models.CharField(db_column='MatchScore', max_length=20, verbose_name='全场比分',
                                  #blank=True)  # Field name made lowercase.
    #winner = models.IntegerField(db_column='Winner', verbose_name=_('Winner'),
                                 #choices=WINNER)  # Field name made lowercase.
    #statuscode = models.IntegerField(db_column='StatusCode', verbose_name=_('Status'),
                                     #choices=MATCH_STATUS)  # Field name made lowercase.
    #roundinfo = models.IntegerField(db_column='RoundInfo', verbose_name=_('Round'))  # 轮数 Field name made lowercase.
    #isrecommend = models.BooleanField(db_column='IsRecommend',
                                      #verbose_name=_('IsRecommend'))  # 推介 Field name made lowercase.
    #livebet = models.BooleanField(db_column='LiveBet', verbose_name='走地')  # 滚球 Field name made lowercase.
    #generatedat = models.DateTimeField(db_column='GeneratedAt',
                                       #verbose_name=_('Create Time'))  # 生成日期 Field name made lowercase.
    #createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    #weights = CusDecimalField(db_column='Weights', max_digits=18, decimal_places=2)  # Field name made lowercase.
    #uniquetournamentid = models.BigIntegerField(db_column='UniqueTournamentId')  # Field name made lowercase.

    #period1score = models.CharField(db_column='Period1Score', max_length=20, blank=True,
                                    #verbose_name='半场比分')  # Field name made lowercase.
    #eventid = models.CharField(db_column='EventID', unique=True, max_length=50, blank=True,
                               #null=True)  # Field name made lowercase.
    #tournamenten = models.CharField(db_column='TournamentEN', max_length=100, blank=True,
                                    #null=True)  # Field name made lowercase.
    #team1en = models.CharField(db_column='Team1EN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    #team2en = models.CharField(db_column='Team2EN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    #homescore = models.IntegerField(db_column='HomeScore')  # Field name made lowercase.
    #awayscore = models.IntegerField(db_column='AwayScore')  # Field name made lowercase.
    #team1icon = models.CharField(db_column='Team1Icon', max_length=255, blank=True,
                                 #null=True)  # Field name made lowercase.
    #team2icon = models.CharField(db_column='Team2Icon', max_length=255, blank=True,
                                 #null=True)  # Field name made lowercase.
    #terminator = models.CharField(db_column='Terminator', max_length=20, blank=True,
                                  #null=True)  # Field name made lowercase.
    #ishidden = models.BooleanField(db_column='IsHidden', default=False,
                                   #verbose_name='隐藏')  # Field name made lowercase.
    #marketstatus = models.IntegerField(db_column='MarketStatus', choices=MATCH_MARKETSTATUS,
                                       #verbose_name='市场状态')  # Field name made lowercase.
    #satimestam = models.DateTimeField(db_column='SaTimestam')  # Field name made lowercase.
    #closelivebet = models.IntegerField(db_column='CloseLiveBet', blank=True, null=True, choices=MATCH_CLOSELIVEBET,
                                       #verbose_name='关闭走地')  # Field name made lowercase.
    #matchstatustype = models.CharField(db_column='MatchStatusType', max_length=50)  # Field name made lowercase.
    #settlestatus = models.IntegerField(db_column='SettleStatus', blank=True, null=True)  # Field name made lowercase.
    #specialcategoryid = models.IntegerField(db_column='SpecialCategoryID')  # Field name made lowercase.
    #mainleagueid = models.IntegerField(db_column='MainLeagueID')  # Field name made lowercase.
    #mainhomeid = models.IntegerField(db_column='MainHomeID')  # Field name made lowercase.
    #mainawayid = models.IntegerField(db_column='MainAwayID')  # Field name made lowercase.
    #mainmatchid = models.IntegerField(db_column='MainMatchID')  # Field name made lowercase.
    #maineventid = models.CharField(db_column='MainEventID', max_length=100, blank = True)  # Field name made lowercase.    
    
    #settletime = models.DateTimeField(db_column='SettleTime', blank=True, null=True)  # Field name made lowercase.
    #source = models.IntegerField(db_column='Source',choices=DATA_SOURCE,verbose_name='数据源')  # Field name made lowercase.
    #liveodds = models.BooleanField(db_column='LiveOdds',verbose_name='走地盘')  # Field name made lowercase.
    #overtimescore = models.CharField(db_column='OvertimeScore', max_length=20,blank=True)  # Field name made lowercase.
    #cornerkicks = models.CharField(db_column='CornerKicks', max_length=255,blank=True)  # Field name made lowercase.
    #period1cornerkicks = models.CharField(db_column='Period1CornerKicks', max_length=255,blank=True)  # Field name made lowercase.    
    
    #class Meta:
        #managed = False
        #db_table = 'TB_Matches'

    #def __str__(self):
        #return '[%(matchid)s]%(home)s vs %(away)s' % {'matchid': self.matchid, 'home': self.team1zh,
                                                      #'away': self.team2zh, }


class TbMatchesoddsswitch(models.Model):
    matchesoddsswitchid = models.AutoField(db_column='MatchesOddsSwitchID',
                                           primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    types = models.IntegerField(db_column='Types', blank=True,
                                help_text='初始值(0)/封比赛(1)/玩法(2)/盘口(3)')  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    oddstypegroup = models.ForeignKey(to='TbOddstypegroup', db_constraint=False, to_field='oddstypegroup',
                                      db_column='OddsTypeGroup', blank=True, default=0)  # Field name made lowercase.
    # oddstypegroup = models.IntegerField(db_column='OddsTypeGroup', blank=True, null=True)  # Field name made lowercase.
    specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=12,
                                       blank=True, )  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', help_text='0无用/1启用')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', auto_now=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime', auto_now=True)  # Field name made lowercase.

    bettypeid = models.IntegerField(db_column='BetTypeID', blank=True, default=0)  # Field name made lowercase.
    periodtype = models.IntegerField(db_column='PeriodType', blank=True, default=0)  # Field name made lowercase.
    handicapkey = models.IntegerField(db_column='HandicapKey', blank=True, default=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_MatchesOddsSwitch'

#class TbMatchesturnover(models.Model):
    #tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #match = models.ForeignKey(TbMatches, db_column='MatchID', db_constraint=False, to_field='matchid')
    ## matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    #oddsid = models.BigIntegerField(db_column='OddsID')  # Field name made lowercase.
    #specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=20)  # Field name made lowercase.
    #amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    #turnover = models.DecimalField(db_column='Turnover', max_digits=18, decimal_places=4)  # Field name made lowercase.

    #class Meta:
        #managed = False
        #db_table = 'TB_MatchesTurnover'


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


class TbMaxpayout(models.Model):
    tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    limittype = models.ForeignKey(to='TbMaxpayouttype', db_constraint=False,
                                  db_column='LimitType', verbose_name='限制类型')  # Field name made lowercase.
    # tournamentid = models.IntegerField(db_column='TournamentID', blank=True, null=True)  # Field name made lowercase.
    tournamentid = models.ForeignKey(to='TbTournament',to_field='tournamentid', db_constraint=False, db_column='TournamentID', blank=True,
                                     default=0, null=True, verbose_name='联赛')  # Field name made lowercase.
    # matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    matchid = models.ForeignKey(to=TbMatch, db_constraint=False, to_field='matchid', db_column='MatchID', blank=True,
                                default=0, null=True, verbose_name='比赛')  # Field name made lowercase.
    # limittype = models.IntegerField(db_column='LimitType')  # Field name made lowercase.

    # accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount, db_constraint=False, db_column='AccountID', blank=True,
                                  null=True, verbose_name='用户昵称')  # Field name made lowercase.
    # oddstypegroup = models.IntegerField(db_column='OddsTypeGroup')  # Field name made lowercase.
    oddstypegroup = models.ForeignKey(to='TbOddstypegroup', db_constraint=False, db_column='OddsTypeGroup', blank=True,
                                      null=True, verbose_name='玩法类型')
    viplv = models.IntegerField(db_column='VIPLv', blank=True, null=True,
                                choices=VIP_LEVEL, verbose_name='VIP等级')  # Field name made lowercase.
    maxpayout = models.DecimalField(db_column='MaxPayout', max_digits=18,
                                    decimal_places=2, verbose_name='最大赔付')  # Field name made lowercase.
    # issingle = models.BooleanField(db_column='IsSingle')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', default=1, blank=True, verbose_name='状态',
                                 choices=COMMON_STATUS)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True,
                                   null=True, verbose_name='备注')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True, auto_now=True,
                                      verbose_name='创建时间')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_MaxPayout'


class TbMaxpayouttype(models.Model):
    limittype = models.IntegerField(db_column='LimitType', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.
    level = models.IntegerField(db_column='Level')  # Field name made lowercase.
    defaultmaxpayout = models.DecimalField(db_column='DefaultMaxPayout', max_digits=18, decimal_places=2, blank=True,
                                           null=True)  # Field name made lowercase.
    isenable = models.BooleanField(db_column='IsEnable')  # Field name made lowercase.
    enum = models.CharField(db_column='Enum', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_MaxPayoutType'

    def __str__(self):
        return self.description

#class TbMaxpayoutBasketball(models.Model):
    #tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #limittype = models.ForeignKey(to='TbMaxpayouttype', db_constraint=False,
                               #db_column='LimitType', verbose_name='限制类型')  # Field name     made lo
    #tournamentid = models.ForeignKey(to='TbTournamentBasketball',to_field='tournamentid', db_constraint=False, db_column='TournamentID', blank=True,
                                     #default=0, null=True, verbose_name='联赛')  # Field name made lowerc    ase.
    ##tournamentid = models.IntegerField(db_column='TournamentID', blank=True, null=True)  # Field name made lowercase.
    #matchid = models.ForeignKey(to= 'TbMatchesBasketball', db_constraint=False, to_field='matchid', db_column='MatchID', blank=True,
                                #default=0, null=True, verbose_name='比赛')  # Field name made lowerc    ase.
    ##matchid = models.BigIntegerField(db_column='MatchID', blank=True, null=True)  # Field name made lowercase.
    
 
    ##limittype = models.IntegerField(db_column='LimitType')  # Field name made lowercase.
    
    #accountid = models.ForeignKey(to=TbAccount, db_constraint=False, db_column='AccountID', blank=True,
                                  #null=True, verbose_name='用户昵称')  # Field name made lo    wercase.
    ##accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    #oddstypegroup = models.ForeignKey(to='TbOddstypegroup', db_constraint=False, db_column='OddsTypeGroup', blank=True,
                                      #null=True, verbose_name='玩法类型')
    ##oddstypegroup = models.IntegerField(db_column='OddsTypeGroup', blank=True, null=True)  # Field name made lowercase.
    #viplv = models.IntegerField(db_column='VIPLv', blank=True, null=True, 
                                #choices=VIP_LEVEL,verbose_name='VIP等级')  # Field name made lowercase.
    #maxpayout = models.DecimalField(db_column='MaxPayout', max_digits=18, decimal_places=2, verbose_name= '最大赔付')  # Field name made lowercase.
    #status = models.IntegerField(db_column='Status', default= 1)  # Field name made lowercase.
    #description = models.CharField(db_column='Description', max_length=500, blank=True, null=True,
                                   #verbose_name = '描述')  # Field name made lowercase.
    #createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True, auto_now_add= True, verbose_name= '创建时间')  # Field name made lowercase.
    #updatetime = models.DateTimeField(db_column='UpdateTime', blank=True, null=True, auto_now= True)  # Field name made lowercase.

    #class Meta:
        #managed = False
        #db_table = 'TB_MaxPayout_Basketball'

class TbMessageUnsend(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    # toaccountsn = models.CharField(db_column='ToAccountSN', max_length=36)  # Field name made lowercase.
    body = models.CharField(db_column='Body', max_length=512)  # Field name made lowercase.
    type = models.SmallIntegerField(db_column='Type')  # Field name made lowercase.
    sender = models.CharField(db_column='Sender', max_length=20)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True)  # Field name made lowercase.
    accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    relationno = models.CharField(db_column='RelationNo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    haveread = models.NullBooleanField(db_column='HaveRead',default=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Message_Unsend'

class TbVip(models.Model):
    level = models.IntegerField(db_column='Level', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=300, blank=True, null=True)  # Field name made lowercase.
    icon = models.CharField(db_column='Icon', max_length=300, blank=True, null=True)  # Field name made lowercase.
    points = models.DecimalField(db_column='Points', max_digits=18, decimal_places=4)  # Field name made lowercase.
    keeppoints = models.DecimalField(db_column='KeepPoints', max_digits=18, decimal_places=4)  # Field name made lowercase.
    keepdays = models.IntegerField(db_column='KeepDays')  # Field name made lowercase.
    rankgifts = models.DecimalField(db_column='RankGifts', max_digits=18, decimal_places=4)  # Field name made lowercase.
    rebate = models.DecimalField(db_column='Rebate', max_digits=18, decimal_places=4)  # Field name made lowercase.
    game1rebate = models.DecimalField(db_column='Game1Rebate', max_digits=18, decimal_places=4)  # Field name made lowercase.
    game2rebate = models.DecimalField(db_column='Game2Rebate', max_digits=18, decimal_places=4)  # Field name made lowercase.
    game3rebate = models.DecimalField(db_column='Game3Rebate', max_digits=18, decimal_places=4)  # Field name made lowercase.
    rebatemaxamount = models.DecimalField(db_column='RebateMaxAmount', max_digits=18, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Vip'
    
    def __str__(self):
        return self.name
        
class TbVipgift(models.Model):
    tid = models.AutoField(db_column='TId', primary_key=True,verbose_name='TID')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=500, blank=True, null=True,verbose_name='标题')  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True,verbose_name='内容')  # Field name made lowercase. This field type is a guess.
    image = CusPictureField(db_column='Image', max_length=200, blank=True, null=True,verbose_name='APP图片')  # Field name made lowercase.
    #image = models.CharField(db_column='Image', max_length=200, blank=True, null=True)  #
    image2 = CusPictureField(db_column='Image2', max_length=200, blank=True, null=True,verbose_name='WEB图片')  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled',verbose_name = '启用')  # Field name made lowercase.
    #image2 = models.CharField(db_column='Image2', max_length=200, blank=True, null=True)  # Field name made lowercase.
   

    class Meta:
        managed = False
        db_table = 'TB_VIPGift'
        
    def __str__(self):
        return self.title or '未命名'
        

class TbVipbonus(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountID',verbose_name='账号')
    #level = models.IntegerField(db_column='Level')  # Field name made lowercase.
    level = models.ForeignKey(to=TbVip,db_constraint=False,db_column='Level',verbose_name='VIP等级')  # Field name made lowercase.
    #ruleid = models.IntegerField(db_column='RuleId')  # Field name made lowercase.
    ruleid = models.ForeignKey(to='TbMoneyCategories',db_constraint=False,db_column='RuleId',verbose_name='发放规则')  # Field name made lowercase.
    
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4,verbose_name='红利金额')  # Field name made lowercase.
 
    drawtime = models.DateTimeField(db_column='DrawTime', blank=True, null=True,verbose_name='领取时间')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='创建时间')  # Field name made lowercase.
    arrivetime = models.DateTimeField(db_column='ArriveTime', blank=True, null=True,verbose_name='发放到账时间')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True,verbose_name='领取过期截止时间')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status',verbose_name='状态')  # Field name made lowercase.
    loginfo = models.CharField(db_column='LogInfo', max_length=3000, blank=True, null=True,verbose_name='日志信息')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=3000, blank=True, null=True,verbose_name='备注')  # Field name made lowercase.
    sourceid = models.BigIntegerField(db_column='SourceId',verbose_name='关联ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_VipBonus'


class TbProductContactUser(models.Model):
    accountid = models.IntegerField(db_column='AccountId', primary_key=True)  # Field name made lowercase.
    userrealname = models.CharField(db_column='UserRealName', max_length=30)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=11)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=32, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=32, blank=True, null=True)  # Field name made lowercase.
    county = models.CharField(db_column='County', max_length=32, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Product_Contact_User'

class TbMessagetype(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64)  # Field name made lowercase.
    needread = models.BooleanField(db_column='NeedRead')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_MessageType'
    
    def __str__(self):
        return self.name

class TbMessage(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    #typeid = models.IntegerField(db_column='TypeId')  # Field name made lowercase.
    typeid = models.ForeignKey(to= TbMessagetype,db_constraint=False,db_column='TypeId',verbose_name='消息类别')
    title = models.CharField(db_column='Title', max_length=255,verbose_name='标题')  # Field name made lowercase.
    
    abstract = models.CharField(db_column='Abstract', max_length=512, blank=True, null=True,verbose_name='摘要')  # Field name made lowercase.
    sender = models.CharField(db_column='Sender', max_length=64,verbose_name='创建者')  # Field name made lowercase.
    sendway = models.IntegerField(db_column='SendWay',verbose_name='发送方式',choices=MESSAGE_SENDWAY,default= 0)  # Field name made lowercase.
    sendtime = models.DateTimeField(db_column='SendTime', blank=True, null=True,verbose_name='预计发送时间')  # Field name made lowercase.
    userids = models.TextField(db_column='UserIds', blank=True, null=True,verbose_name='玩家id',help_text='用分号分割，例如1234;1235;1236')  # Field name made lowercase. This field type is a guess.
    #usergroupids = models.TextField(db_column='UserGroupIds', blank=True, null=True,verbose_name='用户组别')  # Field name made lowercase. This field type is a guess.
    usergroupids = MultiChoiceTextField(db_column='UserGroupIds', blank=True, null=True,verbose_name='用户组别', choices=lambda:[(x.pk,str(x)) for x in TbLimitusergroup.objects.all()]) 
    #vipgroupids = MultiChoiceFromFunField(db_column='UserGroupIds', blank=True, null=True,verbose_name='用户组别',choices=lambda:[(x.pk,str(x)) for x in TbVip.objects.all()])
    vipgroupids = MultiChoiceTextField(db_column='VipGroupIds', blank=True, null=True,verbose_name='VIP组别',choices=lambda:[(x.pk,str(x)) for x in TbVip.objects.all()])
    #vipgroupids = models.TextField(db_column='VipGroupIds', blank=True, null=True,verbose_name='VIP组别')  # Field name made lowercase. This field type is a guess.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True,verbose_name='创建时间')  # Field name made lowercase.
    #content = models.TextField(db_column='Content',verbose_name='内容')  # Field name made lowercase.
    
    issent = models.BooleanField(db_column='IsSent',verbose_name='发送')  # Field name made lowercase.
    content = RichtextField(db_column='Content',verbose_name='内容')
    receivertype = models.IntegerField(db_column='ReceiverType',default=0,blank=True)  # Field name made lowercase.
    
    
    class Meta:
        managed = False
        db_table = 'TB_Message'
    
    def __str__(self):
        return self.title


class TbMessageReceiver(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    messageid = models.IntegerField(db_column='MessageId')  # Field name made lowercase.
    receiverid = models.IntegerField(db_column='ReceiverId')  # Field name made lowercase.
    receivertype = models.IntegerField(db_column='ReceiverType',choices=MESSAGE_RECIVER_TYPE)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Message_Receiver'
        

class TbMoneyCategories(models.Model):
    categoryid = models.IntegerField(db_column='CategoryID', primary_key=True)  # Field name made lowercase.
    cashflow = models.SmallIntegerField(db_column='CashFlow')  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Money_Categories'

    def __str__(self):
        return self.categoryname


class TbMarketgroup(models.Model):
    groupid = models.IntegerField(db_column='GroupID', primary_key=True,verbose_name='组ID')  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID',verbose_name='体育类型')  #  choices=SPORTID_OPTION_2, Field name made lowercase.
    groupname = models.CharField(db_column='GroupName', max_length=100,verbose_name='组名')  # Field name made lowercase.
    groupnamezh = models.CharField(db_column='GroupNameZH', max_length=100,verbose_name='中文名')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True,verbose_name='描述')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort',verbose_name='组排序')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_MarketGroup'
        verbose_name='玩法组(表)'
    
    def __str__(self):
        return self.groupnamezh

class TbMarketgroupwithmarket(models.Model):
    tid = models.AutoField(db_column='TID', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID',verbose_name='玩法组')  # Field name made lowercase.
    #sportid = models.IntegerField(db_column='SportID',choices=SPORTID_OPTION_2,verbose_name='体育类型')  # Field name made lowercase.
    #marketid = models.IntegerField(db_column='MarketID')  # Field name made lowercase.
    marketid = models.ForeignKey(to='TbMarkets',db_constraint=False, db_column='MarketID',verbose_name='玩法')
    #templateid = models.IntegerField(db_column='TemplateID')  # Field name made lowercase.
    #templateid = models.ForeignKey(to='TbTemplate',db_constraint=False,db_column='TemplateID',verbose_name='模板')  # Field name made lowercase.
    #groupsort = models.IntegerField(db_column='GroupSort',verbose_name='组排序')  # Field name made lowercase.
    marketsort = models.IntegerField(db_column='MarketSort',verbose_name='组内玩法排序',default=0)  # Field name made lowercase.
    #sort = models.IntegerField(db_column='Sort',verbose_name='全部玩法排序')  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled',verbose_name='启用',default=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True,verbose_name='描述')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_MarketGroupWithMarket'     


class TbMarkets(models.Model):
    marketid = models.IntegerField(db_column='MarketID', primary_key=True,verbose_name='玩法ID')  # Field name made lowercase.
    marketname = models.CharField(db_column='MarketName', max_length=200, blank=True, null=True,verbose_name='玩法名称')  # Field name made lowercase.
    marketnamezh = models.CharField(db_column='MarketNameZH', max_length=200, blank=True, null=True,verbose_name='玩法中文名')  # Field name made lowercase.
    includesoutcomestype = models.CharField(db_column='IncludesOutcomesType', max_length=200, blank=True, null=True,)  # Field name made lowercase.
    outcometype = models.CharField(db_column='OutcomeType', max_length=200, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True,verbose_name='描述')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort',verbose_name='排序')  # Field name made lowercase.
    enabled = models.NullBooleanField(db_column='Enabled',verbose_name='启用',blank=False)  # Field name made lowercase.
    isasian = models.NullBooleanField(db_column='IsAsian')  # Field name made lowercase.    
    #templateid = models.IntegerField(db_column='TemplateID', blank=True, null=True)  # Field name made lowercase.
    templateid = models.ForeignKey(to='TbTemplate',db_constraint=False,db_column='TemplateID',verbose_name='模板',null=True)  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=18, decimal_places=4,verbose_name='权重')  # Field name made lowercase.
    ticketdelay = models.IntegerField(db_column='TicketDelay',verbose_name='注单延时',default=0,validators=[int_0_p])  # Field name made lowercase.
    extendweight = models.DecimalField(db_column='ExtendWeight', max_digits=18, decimal_places=2 ,verbose_name='扩展权重')  # Field name made lowercase.
   
    class Meta:
        managed = False
        db_table = 'TB_Markets'
    
    def __str__(self):
        return '%s:%s'%(self.marketid ,self.marketnamezh)


class TbMarkethcpswitch(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type',help_text='初始值(0)/封比赛(1)/玩法(2)/盘口(3)')  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    #marketid = models.IntegerField(db_column='MarketID')  # Field name made lowercase.
    marketid = models.ForeignKey(to=TbMarkets,db_constraint=False,db_column='MarketID') 
    specifiers = models.CharField(db_column='Specifiers', max_length=100)  # Field name made lowercase.
    specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=50)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime',auto_now=True)  # Field name made lowercase.
    marketname = models.CharField(db_column='MarketName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    specialbetname = models.CharField(db_column='SpecialBetName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fortherest = models.CharField(db_column='ForTheRest', max_length=50, blank=True,)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_MarketHcpSwitch'

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
    title = models.CharField(db_column='Title', max_length=1024, blank=False, null=True,
                             verbose_name='标题')  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=512, blank=True, null=True,
                           verbose_name='链接Url')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', auto_now=True,
                                      verbose_name='创建时间')  # Field name made lowercase.
    displaytype = models.IntegerField(db_column='DisplayType',default=0,choices=BANNER_DISPLAYTYPE,verbose_name='对内/对外')  # Field name made lowercase.

    createuser = CreateUserField(db_column='CreateUser', blank=True, null=True,
                                 verbose_name='创建人')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', default=1, null=True,
                                 choices=ONLINE_STATUS)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True, default='',
                               verbose_name='内容')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_Notice'


class TbOdds(models.Model):
    tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    msgnr = models.BigIntegerField(db_column='MsgNr')  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    oddskind = models.IntegerField(db_column='OddsKind')  # Field name made lowercase.
    marketid = models.IntegerField(db_column='MarketID', blank=True, null=True)  # Field name made lowercase.
    #marketid = models.ForeignKey(db_column='MarketID',to=TbMarkets,db_constraint=False, blank=True, null=True)
    marketname = models.CharField(db_column='MarketName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    uniqueoutcomeid = models.IntegerField(db_column='UniqueOutcomeID', blank=True, null=True)  # Field name made lowercase.
    outcomeid = models.CharField(db_column='OutcomeID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    outcomename = models.CharField(db_column='OutcomeName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    specifiers = models.CharField(db_column='Specifiers', max_length=100, blank=True, null=True)  # Field name made lowercase.
    specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=12)  # Field name made lowercase.
    specialbetname = models.CharField(db_column='SpecialBetName', max_length=12)  # Field name made lowercase.
    fortherest = models.CharField(db_column='ForTheRest', max_length=12)  # Field name made lowercase.
    isfavorite = models.BooleanField(db_column='IsFavorite')  # Field name made lowercase.
    odds = models.DecimalField(db_column='Odds', max_digits=18, decimal_places=2)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    handicapkey = models.BigIntegerField(db_column='HandicapKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Odds'

#class TbOdds(models.Model):
    #tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    ## matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    #match = models.ForeignKey(to=TbMatches, db_constraint=False, to_field='matchid', db_column='MatchID')
    #msgnr = models.BigIntegerField(db_column='MsgNr')  # Field name made lowercase.
    ## oddsid = models.BigIntegerField(db_column='OddsID')  # Field name made lowercase.
    #oddstype = models.ForeignKey(to='TbOddstypes', db_column='OddsID', db_constraint=False,
                                 #to_field='oddsid')  # Field name made lowercase.
    #odds = CusDecimalField(db_column='Odds', max_digits=18, decimal_places=2)  # Field name made lowercase.
    #specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=12)  # Field name made lowercase.
    #oddsid_ori = models.BigIntegerField(db_column='OddsID_ori')  # Field name made lowercase.
    #source = models.SmallIntegerField(db_column='Source')  # Field name made lowercase.
    #uptodate = models.SmallIntegerField(db_column='UpToDate')  # Field name made lowercase.
    #status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    #score = models.CharField(db_column='Score', max_length=8)  # Field name made lowercase.
    #fortherest = models.CharField(db_column='ForTheRest', max_length=12)  # Field name made lowercase.
    #createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    #updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    #optionzh = models.CharField(db_column='OptionZH', max_length=30)  # Field name made lowercase.

    #specialbetvalue_show = models.CharField(db_column='SpecialBetValue_Show',
                                            #max_length=12)  # Field name made lowercase.
    #oddstypegroup = models.IntegerField(db_column='OddsTypeGroup')  # Field name made lowercase.
    #handicapvalue = models.CharField(db_column='HandicapValue', max_length=10)  # Field name made lowercase.
    #homescore = models.IntegerField(db_column='HomeScore')  # Field name made lowercase.
    #awayscore = models.IntegerField(db_column='AwayScore')  # Field name made lowercase.
    #favouritetype = models.IntegerField(db_column='FavouriteType')  # Field name made lowercase.
    #handicapkey = models.IntegerField(db_column='HandicapKey')  # Field name made lowercase.    
    #outcome = models.IntegerField(db_column='Outcome')  # Field name made lowercase.
    #mainmatchid = models.BigIntegerField(db_column='MainMatchID')  # Field name made lowercase.
    
    #class Meta:
        #managed = False
        #db_table = 'TB_Odds'

#class TbOddsBasketball(models.Model):
    #tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #match = models.ForeignKey(to='TbMatchesBasketball', db_constraint=False, to_field='matchid', db_column='MatchID')
    ##matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    #msgnr = models.BigIntegerField(db_column='MsgNr')  # Field name made lowercase.
    ##oddsid = models.BigIntegerField(db_column='OddsID')  # Field name made lowercase.
    #oddstype = models.ForeignKey(to='TbOddstypes', db_column='OddsID', db_constraint=False,
                                 #to_field='oddsid')  # Field name made lowercase.    
    #odds = models.DecimalField(db_column='Odds', max_digits=18, decimal_places=2)  # Field name made lowercase.
    #specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=12)  # Field name made lowercase.
    #oddsid_ori = models.BigIntegerField(db_column='OddsID_ori')  # Field name made lowercase.
    #source = models.SmallIntegerField(db_column='Source')  # Field name made lowercase.
    #uptodate = models.SmallIntegerField(db_column='UpToDate')  # Field name made lowercase.
    #status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    #score = models.CharField(db_column='Score', max_length=8)  # Field name made lowercase.
    #fortherest = models.CharField(db_column='ForTheRest', max_length=12)  # Field name made lowercase.
    #createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    #updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    #optionzh = models.CharField(db_column='OptionZH', max_length=80, blank=True, null=True)  # Field name made lowercase.
    #specialbetvalue_show = models.CharField(db_column='SpecialBetValue_Show', max_length=12)  # Field name made lowercase.
    #oddstypegroup = models.IntegerField(db_column='OddsTypeGroup')  # Field name made lowercase.
    #handicapvalue = models.CharField(db_column='HandicapValue', max_length=10)  # Field name made lowercase.
    #homescore = models.IntegerField(db_column='HomeScore')  # Field name made lowercase.
    #awayscore = models.IntegerField(db_column='AwayScore')  # Field name made lowercase.
    #favouritetype = models.IntegerField(db_column='FavouriteType')  # Field name made lowercase.
    #handicapkey = models.IntegerField(db_column='HandicapKey')  # Field name made lowercase.
    #outcome = models.IntegerField(db_column='Outcome', blank=True, null=True)  # Field name made lowercase.
    #mainmatchid = models.IntegerField(db_column='MainMatchID')  # Field name made lowercase.

    #class Meta:
        #managed = False
        #db_table = 'TB_Odds_Basketball'


class TbOddsspread(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
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
    oddsid = models.BigIntegerField(db_column='OddsID', unique=True)  # Field name made lowercase.
    oddskind = models.IntegerField(db_column='OddsKind')  # Field name made lowercase.
    oddstypegroup = models.ForeignKey(to='TbOddstypegroup', db_constraint=False, to_field='oddstypegroup',
                                      db_column='OddsTypeGroup', )  # Field name made lowercase.
    # oddstypegroup = models.IntegerField(db_column='OddsTypeGroup')  # Field name made lowercase.
    oddstypeid = models.IntegerField(db_column='OddsTypeID')  # Field name made lowercase.
    periodtype = models.IntegerField(db_column='PeriodType', blank=True, null=True)  # Field name made lowercase.
    oddstypename = models.CharField(db_column='OddsTypeName', max_length=50)  # Field name made lowercase.
    oddstypenamezh = models.CharField(db_column='OddsTypeNameZH', max_length=10)  # Field name made lowercase.
    oddsoutcome = models.CharField(db_column='OddsOutcome', max_length=20)  # Field name made lowercase.
    outcome = models.IntegerField(db_column='Outcome')  # Field name made lowercase.
    outcomedesc = models.CharField(db_column='OutcomeDesc', max_length=200)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort', blank=True, null=True)  # Field name made lowercase.
    # enabled = models.IntegerField(db_column='Enabled', blank=True, null=True)  # Field name made lowercase.
    source = models.IntegerField(db_column='Source')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_OddsTypes'
    
    def __str__(self):
        return self.oddstypenamezh


class TbOddstypegroup(models.Model):
    """
    """
    tid = models.IntegerField(db_column='TID', primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID', choices= SPORTID_OPTION, verbose_name= '运动类型')  # Field name made lowercase.
    oddstypegroup = models.IntegerField(db_column='OddsTypeGroup', unique=True)  # Field name made lowercase.
    oddstypenamezh = models.CharField(db_column='OddsTypeNameZH', max_length=100, blank=True,
                                      null=True, verbose_name='玩法')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    enabled = models.IntegerField(db_column='Enabled', verbose_name='状态')  # Field name made lowercase.
    periodtype = models.IntegerField(db_column='PeriodType', blank=True, null=True, verbose_name='半/全场',
                                     choices=periodtype_CHOICE)  # Field name made lowercase.
    bettype = models.IntegerField(db_column='BetType', verbose_name='编号')  # Field name made lowercase.
    spread = models.DecimalField(db_column='Spread', max_digits=18, decimal_places=4,
                                 verbose_name='水位')  # Field name made lowercase.
    isspecial = models.BooleanField(db_column='IsSpecial')  # Field name made lowercase.
    gametypeid = models.IntegerField(db_column='GameTypeId')  # Field name made lowercase.    

    class Meta:
        managed = False
        db_table = 'TB_OddsTypeGroup'

    def __str__(self):
        return self.oddstypenamezh


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
    voidfactor = models.CharField(db_column='VoidFactor', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    specialbetvalue = models.CharField(db_column='SpecialBetValue', max_length=12, blank=True,
                                       null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Odds_Result'


class TbOutrightevent(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
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


class TbOutcomes(models.Model):
    uniqueoutcomid = models.IntegerField(db_column='UniqueOutcomID', primary_key=True)  # Field name made lowercase.
    outcomeid = models.CharField(db_column='OutcomeID', max_length=200)  # Field name made lowercase.
    outcomename = models.CharField(db_column='OutcomeName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    outcomenamezh = models.CharField(db_column='OutcomeNameZH', max_length=200, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Outcomes'


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
    
    def __str__(self):
        return self.parlayname


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
    channeltype = models.CharField(db_column='ChannelType', max_length=10, blank=True,
                                   null=True)  # Field name made lowercase.
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

P_TYPE=(
    (1,'比分'),
    (2,'黄牌'),
    (3,'红牌'),
    (4,'红黄牌'),
    (5,'角球'),
)

PERIOD_TYP=(
    (0,'常规时间'),
    (1,'加时'),
    (2,'点球大战'),
    (3,'其他')
)
class TbPeriodscore(models.Model):
    tid = models.BigAutoField(db_column='TID', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID', blank=True, null=True,verbose_name='比赛ID')  # Field name made lowercase.
    statuscode = models.IntegerField(db_column='StatusCode', blank=True, null=True,verbose_name='阶段',choices=NEW_MATCH_STATUS)  # Field name made lowercase.
    scoretype = models.IntegerField(db_column='ScoreType', blank=True, null=True,verbose_name='记分类型',choices=P_TYPE)  # Field name made lowercase.
    periodnumber = models.IntegerField(db_column='PeriodNumber', blank=True, null=True,verbose_name='阶段')  # Field name made lowercase.
    home = models.IntegerField(db_column='Home', blank=True, null=True,verbose_name='主队')  # Field name made lowercase.
    away = models.IntegerField(db_column='Away', blank=True, null=True,verbose_name='客队')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True,verbose_name='创建时间',auto_now=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True,verbose_name='常规/加时',choices=PERIOD_TYP)  # Field name made lowercase.
    #periodtype = models.IntegerField(db_column='PeriodType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_PeriodScore'


class TbQa(models.Model):
    qaid = models.AutoField(db_column='QAID', primary_key=True)  # Field name made lowercase.
    class_field = models.CharField(db_column='Class', max_length=1, default=0,
                                   blank=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    mtype = models.IntegerField(db_column='MType', default=0,
                                verbose_name=_('Belong To'))  # 从属于Field name made lowercase.
    type = models.IntegerField(db_column='Type',default=0)  # Field name made lowercase.
    priority = models.SmallIntegerField(db_column='Priority', default=0, verbose_name='优先级',help_text='大的数字优先级高')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=100, verbose_name='标题')  # Field name made lowercase.
    description = models.TextField(db_column='Description',verbose_name='详细')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status', default=1,verbose_name='状态',
                                      choices=ONLINE_STATUS)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime', auto_now=True)  # Field name made lowercase.
    ver = models.IntegerField(db_column='Ver', default=0, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_QA'
    
    def __str__(self):
        return self.title


class TbRcFilter(models.Model):
    rc_rule_id = models.AutoField(db_column='RC_rule_id', primary_key=True)  # Field name made lowercase.
    rc_level = models.CharField(db_column='RC_Level', verbose_name=_('Level'),
                                max_length=1)  # Field name made lowercase.
    rc_rule = models.IntegerField(db_column='RC_rule', verbose_name=_('Rule'))  # Field name made lowercase.
    rc_rule_name = models.CharField(db_column='RC_rule_Name', verbose_name=_('Rule Level'),
                                    max_length=30)  # Field name made lowercase.'
    rc_filter = CusDecimalField(db_column='RC_filter', verbose_name=_('Filter'), max_digits=18,
                                decimal_places=2)  # Field name made lowercase.
    rc_active = models.SmallIntegerField(db_column='RC_active', verbose_name=_('Active'))  # Field name made lowercase.
    rc_days = models.IntegerField(db_column='RC_DAYS', verbose_name=_('Days'))  # Field name made lowercase.
    description = models.CharField(db_column='Description', verbose_name=_('Description'), max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_RC_Filter'


class TbRcLevel(models.Model):
    rc_level_id = models.AutoField(db_column='RC_Level_ID', primary_key=True,
                                   verbose_name=_('RcLevelID'))  # Field name made lowercase.
    rc_level = models.CharField(db_column='RC_Level', max_length=1,
                                verbose_name=_('RcLevel'))  # Field name made lowercase.
    rc_level_type = models.IntegerField(db_column='RC_Level_Type',
                                        verbose_name=_('RcLevelType'))  # Field name made lowercase.
    rc_level_name = models.CharField(db_column='RC_Level_Name', max_length=20,
                                     verbose_name=_('RcLevelName'))  # Field name made lowercase.
    rc_level_filter = CusDecimalField(db_column='RC_Level_Filter', max_digits=18, decimal_places=2,
                                      verbose_name=_('RcLevelFilter'))  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_RC_Level'


class TbRcUser(models.Model):
    accountid = models.IntegerField(db_column='AccountID', primary_key=True,
                                    verbose_name=_('AccountID'))  # Field name made lowercase.
    # accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    accounttype = models.SmallIntegerField(db_column='AccountType',
                                           verbose_name=_('AccountType'))  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20,
                               verbose_name=_('Account'))  # Field name made lowercase.
    rc_level = models.CharField(db_column='RC_Level', max_length=1,
                                verbose_name=_('RcLevel'))  # Field name made lowercase.

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

class TbRisklevellog(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    accountid = models.BigIntegerField(db_column='AccountID')  # Field name made lowercase.
    oldrisklevel = models.IntegerField(db_column='OldRiskLevel')  # Field name made lowercase.
    newrisklevel = models.IntegerField(db_column='NewRiskLevel')  # Field name made lowercase.
    upordown = models.IntegerField(db_column='UpOrDown')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True)  # Field name made lowercase.
    createuser = models.CharField(db_column='CreateUser', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_RiskLevelLog'

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


class TbSourcecontrol(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    source = models.IntegerField(db_column='Source', blank=True, null=True)  # Field name made lowercase.
    sporttype = models.IntegerField(db_column='SportType', blank=True, null=True)  # Field name made lowercase.
    oddskind = models.IntegerField(db_column='OddsKind', blank=True, null=True)  # Field name made lowercase.
    sites = models.CharField(db_column='Sites', max_length=100, blank=True, null=True)  # Field name made lowercase.
    begintime = models.DateTimeField(db_column='BeginTime', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    enabled = models.NullBooleanField(db_column='Enabled')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_SourceControl'

# 沙巴 --start

class TbSportaccount(models.Model):
    accountid = models.ForeignKey(to=TbAccount,db_column='AccountId', primary_key=True,verbose_name='账号')
    #accountid = models.BigIntegerField(db_column='AccountId', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50,verbose_name='沙巴用户名')  # Field name made lowercase.
    transferin = models.DecimalField(db_column='TransferIn', max_digits=18, decimal_places=4,verbose_name='转入')  # Field name made lowercase.
    transferout = models.DecimalField(db_column='TransferOut', max_digits=18, decimal_places=4,verbose_name='转出')  # Field name made lowercase.
    winorloss = models.DecimalField(db_column='WinOrLoss', max_digits=18, decimal_places=4,verbose_name='亏盈')  # Field name made lowercase.
    bonusrate = models.DecimalField(db_column='BonusRate', max_digits=18, decimal_places=4,verbose_name='反点率')  # Field name made lowercase.
    rebate = models.DecimalField(db_column='Rebate', max_digits=18, decimal_places=4,verbose_name='总反水')  # Field name made lowercase.
    availablescores = models.DecimalField(db_column='AvailableScores', max_digits=18, decimal_places=4,verbose_name='余额')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='创建时间')  # Field name made lowercase.
    fundswitch = models.BooleanField(db_column='FundSwitch',verbose_name='资金开关')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_SportAccount'

class TbSportmoneyininfo(models.Model):
    moneyinid = models.AutoField(db_column='MoneyInID', primary_key=True,verbose_name='记录ID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='金额')  # Field name made lowercase.
    orderid = models.CharField(db_column='OrderID', max_length=50, blank=True, null=True,verbose_name='订单号')  # Field name made lowercase.
    ordertime = models.DateTimeField(db_column='OrderTime', blank=True, null=True,verbose_name='时间')  # Field name made lowercase.
    handle = models.CharField(db_column='Handle', max_length=50, blank=True, null=True,verbose_name='操作者')  # Field name made lowercase.
    handtime = models.DateTimeField(db_column='HandTime', blank=True, null=True,verbose_name='操作时间')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountId', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountID', blank=True, null=True,verbose_name='账号')  # Fie
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True,verbose_name='沙巴用户名')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True,verbose_name='状态',choices=GAMEMONEY_IN_STATUS)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=2000, blank=True, null=True,verbose_name='备注')  # Field name made lowercase.
    tsamp = models.TextField(db_column='Tsamp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'TB_SportMoneyInInfo'
        
class TbSportmoneyoutinfo(models.Model):
    moneyoutid = models.AutoField(db_column='MoneyOutID', primary_key=True,verbose_name='记录ID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='金额')  # Field name made lowercase.
    orderid = models.CharField(db_column='OrderID', max_length=50, blank=True, null=True,verbose_name='订单号')  # Field name made lowercase.
    ordertime = models.DateTimeField(db_column='OrderTime', blank=True, null=True,verbose_name='时间')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountID', blank=True, null=True,verbose_name='账号')  # Fiel
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True,verbose_name='沙巴用户名')  # Field name made lowercase.
    handle = models.CharField(db_column='Handle', max_length=50, blank=True, null=True,verbose_name='操作者')  # Field name made lowercase.
    handtime = models.DateTimeField(db_column='HandTime', blank=True, null=True,verbose_name='操作时间')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True,choices=GAMEMONEY_OUT_STATUS,verbose_name='状态')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=2000, blank=True, null=True,verbose_name='备注')  # Field name made lowercase.
    tsamp = models.TextField(db_column='Tsamp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'TB_SportMoneyOutInfo'

class TbSportprofitloss(models.Model):
    profitlossid = models.AutoField(db_column='ProfitLossID', primary_key=True,verbose_name='记录ID')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountId', blank=True, null=True,verbose_name='账号')
    profitlosstime = models.DateTimeField(db_column='ProfitLossTime', blank=True, null=True,verbose_name='游戏时间')  # Field name made lowercase.
    profitlosstype = models.CharField(db_column='ProfitLossType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    profitlossmoney = models.DecimalField(db_column='ProfitLossMoney', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='投注额')  # Field name made lowercase.
    winmoney = models.DecimalField(db_column='WinMoney', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='亏盈')  # Field name made lowercase.
    prizemoney = models.DecimalField(db_column='PrizeMoney', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='派奖额')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=500, blank=True, null=True,verbose_name='描述')  # Field name made lowercase.
    playid = models.CharField(db_column='PlayID', max_length=50, blank=True, null=True,verbose_name ='游戏ID')  # Field name made lowercase.
    gametype = models.CharField(db_column='GameType', max_length=50, blank=True, null=True,verbose_name='游戏类型')  # Field name made lowercase.
    refid = models.IntegerField(db_column='RefID', blank=True, null=True,verbose_name='')  # Field name made lowercase.
    savetime = models.DateTimeField(db_column='SaveTime', blank=True, null=True,verbose_name='数据保存时间')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID', blank=True, null=True)  # Field name made lowercase.
    bettime = models.DateTimeField(db_column='BetTime', blank=True, null=True)  # Field name made lowercase.
    iswin = models.IntegerField(db_column='IsWin', blank=True, null=True,verbose_name='赢')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True,verbose_name='沙巴用户名')  # Field name made lowercase.
    rebate = models.DecimalField(db_column='Rebate', max_digits=18, decimal_places=4,verbose_name='返点金额')  # Field name made lowercase.
    turnover = models.DecimalField(db_column='Turnover', max_digits=18, decimal_places=0,verbose_name='流水')  # Field name made lowercase.
     
    class Meta:
        managed = False
        db_table = 'TB_SportProfitLoss'

# 沙巴 --over

class TbLcityaccount(models.Model):
    accountid = models.ForeignKey(to=TbAccount,db_column='AccountId', primary_key=True,verbose_name='账号')
    #accountid = models.BigIntegerField(db_column='AccountId', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50,verbose_name='龙城用户名')  # Field name made lowercase.
    transferin = models.DecimalField(db_column='TransferIn', max_digits=18, decimal_places=4,verbose_name='转入')  # Field name made lowercase.
    transferout = models.DecimalField(db_column='TransferOut', max_digits=18, decimal_places=4,verbose_name='转出')  # Field name made lowercase.
    winorloss = models.DecimalField(db_column='WinOrLoss', max_digits=18, decimal_places=4,verbose_name='亏盈')  # Field name made lowercase.
    bonusrate = models.DecimalField(db_column='BonusRate', max_digits=18, decimal_places=4,verbose_name='反点率')  # Field name made lowercase.
    rebate = models.DecimalField(db_column='Rebate', max_digits=18, decimal_places=4,verbose_name='总反水')  # Field name made lowercase.
    availablescores = models.DecimalField(db_column='AvailableScores', max_digits=18, decimal_places=4,verbose_name='余额')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='创建时间')  # Field name made lowercase.
    fundswitch = models.BooleanField(db_column='FundSwitch',verbose_name='资金开关')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_LCityAccount'
        
class TbLcitymoneyininfo(models.Model):
    moneyinid = models.AutoField(db_column='MoneyInID', primary_key=True,verbose_name='记录ID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='金额')  # Field name made lowercase.
    orderid = models.CharField(db_column='OrderID', max_length=50, blank=True, null=True,verbose_name='订单号')  # Field name made lowercase.
    ordertime = models.DateTimeField(db_column='OrderTime', blank=True, null=True,verbose_name='时间')  # Field name made lowercase.
    handle = models.CharField(db_column='Handle', max_length=50, blank=True, null=True,verbose_name='操作者')  # Field name made lowercase.
    handtime = models.DateTimeField(db_column='HandTime', blank=True, null=True,verbose_name='操作时间')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountId', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountID', blank=True, null=True,verbose_name='账号')  # Fie
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True,verbose_name='龙城用户名')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True,verbose_name='状态',choices=GAMEMONEY_IN_STATUS)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=2000, blank=True, null=True,verbose_name='备注')  # Field name made lowercase.
    tsamp = models.TextField(db_column='Tsamp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    

    class Meta:
        managed = False
        db_table = 'TB_LCityMoneyInInfo'
        
class TbLcitymoneyoutinfo(models.Model):
    moneyoutid = models.AutoField(db_column='MoneyOutID', primary_key=True,verbose_name='记录ID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='金额')  # Field name made lowercase.
    orderid = models.CharField(db_column='OrderID', max_length=50, blank=True, null=True,verbose_name='订单号')  # Field name made lowercase.
    ordertime = models.DateTimeField(db_column='OrderTime', blank=True, null=True,verbose_name='时间')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountID', blank=True, null=True,verbose_name='账号')  # Fiel
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True,verbose_name='龙城用户名')  # Field name made lowercase.
    handle = models.CharField(db_column='Handle', max_length=50, blank=True, null=True,verbose_name='操作者')  # Field name made lowercase.
    handtime = models.DateTimeField(db_column='HandTime', blank=True, null=True,verbose_name='操作时间')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True,choices=GAMEMONEY_OUT_STATUS,verbose_name='状态')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=2000, blank=True, null=True,verbose_name='备注')  # Field name made lowercase.
    tsamp = models.TextField(db_column='Tsamp', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    
    class Meta:
        managed = False
        db_table = 'TB_LCityMoneyOutInfo'

class TbLcityprofitloss(models.Model):
    profitlossid = models.AutoField(db_column='ProfitLossID', primary_key=True,verbose_name='记录ID')  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_constraint=False,db_column='AccountId', blank=True, null=True,verbose_name='账号')
    profitlosstime = models.DateTimeField(db_column='ProfitLossTime', blank=True, null=True,verbose_name='游戏时间')  # Field name made lowercase.
    profitlosstype = models.CharField(db_column='ProfitLossType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    profitlossmoney = models.DecimalField(db_column='ProfitLossMoney', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='投注额')  # Field name made lowercase.
    winmoney = models.DecimalField(db_column='WinMoney', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='亏盈')  # Field name made lowercase.
    prizemoney = models.DecimalField(db_column='PrizeMoney', max_digits=18, decimal_places=4, blank=True, null=True,verbose_name='派奖额')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=500, blank=True, null=True,verbose_name='描述')  # Field name made lowercase.
    playid = models.CharField(db_column='PlayID', max_length=50, blank=True, null=True,verbose_name ='游戏ID')  # Field name made lowercase.
    gametype = models.CharField(db_column='GameType', max_length=50, blank=True, null=True,verbose_name='游戏类型')  # Field name made lowercase.
    refid = models.IntegerField(db_column='RefID', blank=True, null=True,verbose_name='')  # Field name made lowercase.
    savetime = models.DateTimeField(db_column='SaveTime', blank=True, null=True,verbose_name='数据保存时间')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID', blank=True, null=True)  # Field name made lowercase.
    bettime = models.DateTimeField(db_column='BetTime', blank=True, null=True)  # Field name made lowercase.
    iswin = models.IntegerField(db_column='IsWin', blank=True, null=True,verbose_name='赢')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True,verbose_name='龙城用户名')  # Field name made lowercase.
    rebate = models.DecimalField(db_column='Rebate', max_digits=18, decimal_places=4,verbose_name='返点金额')  # Field name made lowercase.
    turnover = models.DecimalField(db_column='Turnover', max_digits=18, decimal_places=0,verbose_name='流水')  # Field name made lowercase.
    

    class Meta:
        managed = False
        db_table = 'TB_LCityProfitLoss'
# ---- 龙城结束        
  
class TbTeams(models.Model):
    tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    zhname = models.CharField(db_column='ZHName', max_length=50, blank=True,
                              verbose_name='中文名称')  # Field name made lowercase.
    enname = models.CharField(db_column='ENName', max_length=50, verbose_name='英文名称')  # Field name made lowercase.
    icon = models.CharField(db_column='Icon', max_length=200, blank=True, null=True,
                            verbose_name='球队Icon')  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=20, blank=True,
                               verbose_name='国家')  # Field name made lowercase.
    leaguename = models.CharField(db_column='LeagueName', max_length=30, blank=True,
                                  verbose_name='联赛')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, choices=TEAM_STATUS,
                                 default=0)  # Field name made lowercase.
    saenname = models.CharField(db_column='SAEnName', max_length=50, blank=True,
                                null=True, verbose_name='SA英文名称 ')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Teams'
        
class TbTeamsBasketball(models.Model):
    tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    zhname = models.CharField(db_column='ZHName', max_length=50, blank=True,
                              verbose_name='中文名称')  # Field name made lowercase.
    enname = models.CharField(db_column='ENName', max_length=50, verbose_name='英文名称')  # Field name made lowercase.
    icon = models.CharField(db_column='Icon', max_length=200, blank=True, null=True,
                            verbose_name='球队Icon')  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=20, blank=True,
                               verbose_name='国家')  # Field name made lowercase.
    leaguename = models.CharField(db_column='LeagueName', max_length=30, blank=True,
                                  verbose_name='联赛')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, choices=TEAM_STATUS,
                                 default=0)  # Field name made lowercase.
    saenname = models.CharField(db_column='SAEnName', max_length=50, blank=True,
                                null=True, verbose_name='SA英文名称 ')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Teams_Basketball'


class TbTemplate(models.Model):
    templateid = models.IntegerField(db_column='TemplateID', primary_key=True)  # Field name made lowercase.
    templatename = models.CharField(db_column='TemplateName', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Template'
        
    def __str__(self):
        return self.templatename


class TbTicketmaster(models.Model):
    "注单列表"
    ticketid = models.AutoField(db_column='TicketID', verbose_name=_('Ticket ID'), primary_key=True)
    #accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    stakeamount = CusDecimalField(db_column='StakeAmount', verbose_name=_('StakeAmount'), max_digits=18,
                                  decimal_places=4)  # 单注金额 .
    betamount = CusDecimalField(db_column='BetAmount', verbose_name=_('BetAmount'), max_digits=18,
                                decimal_places=4)  # 总金额 Field name made lowercase.
    #parlayrule = models.IntegerField(db_column='ParlayRule', verbose_name=_('ParlayRule'))  # 串关规则
    parlayrule = models.ForeignKey(to=TbParlayrules,db_constraint=False,db_column='ParlayRule', verbose_name=_('ParlayRule'))  # 串关规则
    allowauto = models.SmallIntegerField(db_column='AllowAuto', verbose_name=_('AllowAuto'))  # 自动接收最新赔率
    status = models.IntegerField(db_column='Status', verbose_name=_('Status'),
                                 choices=TbTicketmaster_STATUS)  # Field name made lowercase.
    winbet = models.SmallIntegerField(db_column='WinBet', verbose_name='胜平负', choices=TbTicketmaster_WINBET)  # 是否中注
    createtime = models.DateTimeField(verbose_name=_('CreateTime'),
                                      db_column='CreateTime')  # Field name made lowercase.
    betoutcome = CusDecimalField(db_column='BetOutcome', verbose_name=_('BetOutcome'), max_digits=18,
                                 decimal_places=4)  # 派彩金额
    turnover = CusDecimalField(db_column='Turnover', verbose_name='流水', max_digits=18,
                               decimal_places=4)  # Field name made lowercase.
    bonuspa = CusDecimalField(db_column='BonusPa', verbose_name='反水比例', max_digits=18,
                              decimal_places=4, digits=3)  # Field name made lowercase.
    bonus = CusDecimalField(db_column='Bonus', verbose_name='反水', max_digits=18,
                            decimal_places=4)  # Field name made lowercase.
    rawdata = models.CharField(db_column='RawData', verbose_name='原始数据', max_length=4000)  # Field name made lowercase.
    settletime = models.DateTimeField(verbose_name='结算时间', db_column='SettleTime')  # Field name made lowercase.
    stakecount = models.IntegerField(db_column='StakeCount')  # Field name made lowercase.
    parlaycount = models.IntegerField(db_column='ParlayCount')  # Field name made lowercase.
    reststakecount = models.IntegerField(db_column='RestStakeCount')  # Field name made lowercase.
    # accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    accountid = models.ForeignKey(TbAccount, db_column='AccountID', db_constraint=False, verbose_name='用户昵称')
    orderid = models.BigIntegerField(db_column='OrderID', unique=True, verbose_name='订单号')  # Field name made lowercase.
    #handicap = models.IntegerField(db_column='Handicap')  # Field name made lowercase.
    possibleturnover = CusDecimalField(db_column='PossibleTurnover', max_digits=18, decimal_places=4, blank=True,
                                       null=True)  # Field name made lowercase.
    minendcount = models.IntegerField(db_column='MinEndCount')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=200, blank=True, null=True,
                            verbose_name='备注')  # Field name made lowercase.
    voidreason = models.CharField(db_column='VoidReason', max_length=200, blank=True, null=True,
                            verbose_name='作废原因')  # Field name made lowercase.
    handicap = models.IntegerField(db_column='Handicap', blank=True, null=True)  # Field name made lowercase.
    terminal = models.IntegerField(db_column='Terminal', blank=True, null=True,choices= TERMINAL_TYPE,verbose_name='终端')  # Field name made lowercase.
    audit = models.IntegerField(db_column='Audit',verbose_name='待审核',choices=AUDIT_OPTIONS)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_TicketMaster'

    def __str__(self):
        return str(self.ticketid)


class TbTicketparlay(models.Model):
    """串关规则"""
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    # ticketid = models.BigIntegerField(db_column='TicketID')
    ticket_master = models.ForeignKey(to='TbTicketmaster', db_column='TicketID', db_constraint=False,
                                      verbose_name=_('ticket master'), to_field='ticketid')

    # ticketid = models.CharField(db_column='TicketID', max_length=20)  # Field name made lowercase.
    parlay1tid = models.ForeignKey(to='TbTicketstake', db_constraint=False, db_column='Parlay1Tid',
                                   verbose_name='子注单ID1', related_name='Ticketparlay1', null=True)
    parlay2tid = models.ForeignKey(to='TbTicketstake', db_constraint=False, db_column='Parlay2Tid',
                                   verbose_name='子注单ID2', related_name='Ticketparlay2', null=True)
    parlay3tid = models.ForeignKey(to='TbTicketstake', db_constraint=False, db_column='Parlay3Tid',
                                   verbose_name='子注单ID3', related_name='Ticketparlay3', null=True)
    parlay4tid = models.ForeignKey(to='TbTicketstake', db_constraint=False, db_column='Parlay4Tid',
                                   verbose_name='子注单ID4', related_name='Ticketparlay4', null=True)
    parlay5tid = models.ForeignKey(to='TbTicketstake', db_constraint=False, db_column='Parlay5Tid',
                                   verbose_name='子注单ID5', related_name='Ticketparlay5', null=True)
    parlay6tid = models.ForeignKey(to='TbTicketstake', db_constraint=False, db_column='Parlay6Tid',
                                   verbose_name='子注单ID6', related_name='Ticketparlay6', null=True)

    # parlay1tid = models.BigIntegerField(db_column='Parlay1Tid',verbose_name='子注单ID1')  # Field name made lowercase.
    # parlay2tid = models.BigIntegerField(db_column='Parlay2Tid',verbose_name='子注单ID2')  # Field name made lowercase.
    # parlay3tid = models.BigIntegerField(db_column='Parlay3Tid',verbose_name='子注单ID3')  # Field name made lowercase.
    # parlay4tid = models.BigIntegerField(db_column='Parlay4Tid',verbose_name='子注单ID4')  # Field name made lowercase.
    # parlay5tid = models.BigIntegerField(db_column='Parlay5Tid',verbose_name='子注单ID5')  # Field name made lowercase.
    # parlay6tid = models.BigIntegerField(db_column='Parlay6Tid',verbose_name='子注单ID6')  # Field name made lowercase.
    odds = CusDecimalField(db_column='Odds', verbose_name='赔率', max_digits=18,
                           decimal_places=2)  # Field name made lowercase.
    stakeamount = CusDecimalField(db_column='StakeAmount', verbose_name='每注金额', max_digits=18,
                                  decimal_places=4)  # Field name made lowercase.
    betoutcome = CusDecimalField(db_column='BetOutcome', verbose_name='派彩金额', max_digits=18,
                                 decimal_places=4)  # Field name made lowercase.
    winbet = models.SmallIntegerField(db_column='WinBet', verbose_name='中注')  # Field name made lowercase.
    turnover = CusDecimalField(db_column='Turnover', verbose_name='流水', max_digits=18,
                               decimal_places=4)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', verbose_name='建立时间')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_TicketParlay'


class TbTicketstake(models.Model):
    """子注单"""
    tid = models.AutoField(db_column='Tid', primary_key=True, verbose_name='记录ID')  # Field name made lowercase.
    #ticketid = models.BigIntegerField(db_column='TicketID')  # Field name made lowercase.
    ticket_master = models.ForeignKey(TbTicketmaster, db_column='TicketID',
                                      db_constraint=False, verbose_name=_('ticket master'))
    stakeid = models.SmallIntegerField(db_column='StakeID')  # Field name made lowercase.
    matchid = models.ForeignKey(to=TbMatch,db_constraint=False,db_column='MatchID',verbose_name='比赛ID')  # Field name made lowercase.
    dangeroustid = models.BigIntegerField(db_column='DangerousTid')  # Field name made lowercase.
    #marketid = models.IntegerField(db_column='MarketID', blank=True, null=True)  # Field name made lowercase.
    marketid = models.ForeignKey(to=TbMarkets,db_constraint=False,db_column='MarketID', blank=True, null=True,verbose_name='玩法')  # Field name made lowercase.
    
    specifiers = models.CharField(db_column='Specifiers', max_length=100, blank=True, null=True)  # Field name made lowercase.
    uniqueoutcomeid = models.IntegerField(db_column='UniqueOutcomeID', blank=True, null=True)  # Field name made lowercase.
    outcomeid = models.CharField(db_column='OutcomeID', max_length=100, blank=True, null=True)  # Field name made lowercase.
       
    specialbetvalue = models.CharField(db_column='SpecialBetValue', verbose_name='盘口值',
                                       max_length=12)  # Field name made lowercase.
    specialbetname = models.CharField(db_column='SpecialBetName', max_length=50, blank=True, null=True,verbose_name='盘口')  # Field name made lowercase.
    odds = CusDecimalField(db_column='Odds', verbose_name='赔率', max_digits=18,
                           decimal_places=2)  # Field name made lowercase.
    confirmodds = CusDecimalField(db_column='ConfirmOdds', verbose_name='确认赔率', max_digits=18,
                                  decimal_places=2)  # Field name made lowercase.
    realodds = CusDecimalField(db_column='RealOdds', verbose_name='真实赔率', max_digits=18,
                               decimal_places=2)  # Field name made lowercase.
    #oddsid_ori = models.BigIntegerField(db_column='OddsID_ori')  # Field name made lowercase.
    #confirmoddsid_ori = models.BigIntegerField(db_column='ConfirmOddsID_ori',
                                               #verbose_name='结算值')  # Field name made lowercase.
    #voidfactor = models.CharField(db_column='VoidFactor', max_length=10)  # Field name made lowercase.
    voidfactor = models.CharField(db_column='VoidFactor', max_length=10)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', verbose_name='状态',
                                 choices=TicketStake_STATUS)  # Field name made lowercase.
    rawdata = models.CharField(db_column='RawData', max_length=3000)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', verbose_name='建立时间')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime', verbose_name='更新时间')  # Field name made lowercase.
    #confirmoddstid = models.BigIntegerField(db_column='ConfirmOddsTid')  # Field name made lowercase.
    oddskind = models.IntegerField(db_column='OddsKind',choices=ODDSKIND,verbose_name='早盘/走地')  # Field name made lowercase.
   

    #homescore = models.IntegerField(db_column='HomeScore')  # Field name made lowercase.
    #awayscore = models.IntegerField(db_column='AwayScore')  # Field name made lowercase.
    parlayrule = models.IntegerField(db_column='ParlayRule', blank=True, null=True)  # Field name made lowercase.
    winbet = models.IntegerField(db_column='WinBet')  # Field name made lowercase.
    handicapkey = models.BigIntegerField(db_column='HandicapKey')  # Field name made lowercase.
    accountid = models.IntegerField(db_column='AccountID')  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    #mainmatchid = models.IntegerField(db_column='MainMatchID')  # Field name made lowercase.
    marketname = models.CharField(db_column='MarketName', max_length=100, blank=True, null=True,verbose_name='玩法')  # Field name made lowercase.
    outcomename = models.CharField(db_column='OutcomeName', max_length=50, blank=True, null=True,verbose_name='投注项')  # Field name made lowercase.    
    score = models.CharField(db_column='Score', max_length=50, blank=True, null=True,verbose_name = '当时比分')  # Field name made lowercase.
    ticketbetstopdiff = models.IntegerField(db_column='TicketBetStopDiff',verbose_name='BetStop时间差(S)')  # Field name made lowercase.
    oddsource = models.IntegerField(db_column='OddSource',choices=ODDSOURCE,verbose_name='赔率来源')  # Field name made lowercase.
    #@property
    #def match(self): 
        #if self.sportid == 0:
            #return TbMatches.objects.get(matchid = self.matchid)
        #elif self.sportid == 1:
            #return TbMatchesBasketball.objects.get(matchid = self.matchid)
        #else:
            #raise UserWarning('没有比赛能同matchid=%s匹配！' % self.matchid)
    
    class Meta:
        managed = False
        db_table = 'TB_TicketStake'
    
    def __str__(self):
        return self.outcomename


#class TbTickets(models.Model):
    #tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    ## accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    #account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    #match = models.ForeignKey(TbMatch, db_constraint=False,
                              #db_column='MatchID')  # models.IntegerField(db_column='MatchID')  # Field name made lowercase.
    #oddstid = models.IntegerField(db_column='OddsTid')  # Field name made lowercase.
    #odds = CusDecimalField(db_column='Odds', max_digits=18, decimal_places=2)  # Field name made lowercase.
    #betamount = models.IntegerField(db_column='BetAmount')  # Field name made lowercase.
    #status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    #betoutcome = CusDecimalField(db_column='BetOutcome', max_digits=18, decimal_places=2)  # Field name made lowercase.
    #turnover = CusDecimalField(db_column='Turnover', max_digits=18, decimal_places=2)  # Field name made lowercase.
    #bonuspa = CusDecimalField(db_column='BonusPa', max_digits=18, decimal_places=2)  # Field name made lowercase.
    #bonus = CusDecimalField(db_column='Bonus', max_digits=18, decimal_places=2)  # Field name made lowercase.
    #rawdata = models.CharField(db_column='RawData', max_length=500, blank=True, null=True)  # Field name made lowercase.
    #createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    #settletime = models.DateTimeField(db_column='SettleTime', blank=True, null=True)  # Field name made lowercase.

    #class Meta:
        #managed = False
        #db_table = 'TB_Tickets'


class TbTournament(models.Model):
    tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #sportid = models.IntegerField(db_column='SportID', blank=True, null=True,choices=SPORTID_OPTION_2,verbose_name='运动类型')  # Field name made lowercase.
    tournamentid = models.IntegerField(db_column='TournamentID', verbose_name='联赛ID',unique=True,)  # Field name made lowercase.
    tournamentname = models.CharField(db_column='TournamentName', max_length=200,
                                      verbose_name='英文名')  # Field name made lowercase.
    tournamentnamezh = models.CharField(db_column='TournamentNameZH', max_length=200,verbose_name='中文名')  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    
    uniquetournamentid = models.IntegerField(db_column='UniqueTournamentID',
                                             verbose_name='联赛ID')  # Field name made lowercase.
    typegroupswitch = models.CharField(db_column='TypeGroupSwitch', max_length=200, blank=True, null=True,
                                       verbose_name='已关闭玩法')  # Field name made lowercase.
    issubscribe = models.IntegerField(db_column='IsSubscribe',default=1, verbose_name='已订阅')  # Field name made lowercase.
    closelivebet = models.IntegerField(db_column='CloseLiveBet', verbose_name='关闭滚球')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort', null=True, verbose_name='排序')  # Field name made lowercase.
   
    #closelivebet = models.IntegerField(db_column='CloseLiveBet', blank=True, null=True, verbose_name= '关闭滚球')  # Field name made lowercase.
    #specialcategoryid = models.IntegerField(db_column='SpecialCategoryID')  # Field name made lowercase.    
    #source = models.IntegerField(db_column='Source',choices=DATA_SOURCE,verbose_name='数据源')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True)  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=18, decimal_places=4,verbose_name='权重',null=True,blank=True)  # Field name made lowercase.
    ticketdelay = models.IntegerField(db_column='TicketDelay',verbose_name='注单延时',null=True,default=0,validators=[int_0_p])  # Field name made lowercase.
    #sportid = models.IntegerField(db_column='SportID',)  # Field name made lowercase.
    sport = models.ForeignKey(to= 'TbSporttypes',to_field='sportid',db_column='SportID',db_constraint=False,verbose_name='体育类型')  # Field name made lowercase.
    isrecommend = models.BooleanField(db_column='IsRecommend',verbose_name = '推荐')  # Field name made lowercase.
    
    oddsadjustment = models.DecimalField(db_column='OddsAdjustment', max_digits=2, decimal_places=2,verbose_name='赔率调整值')  # Field name made lowercase.
    oddsadjustmax = models.DecimalField(db_column='OddsAdjustMax', max_digits=2, decimal_places=2,verbose_name='赔率调整最大值')  # Field name made lowercase.
    baseticketeamout = models.DecimalField(db_column='BaseTicketeAmout', max_digits=18, decimal_places=2,verbose_name='投注差额基数',help_text='每投注X元赔率调整一次')  # Field name made lowercase.
    #adjusttemplateid = models.IntegerField(db_column='AdjustTemplateID')  # Field name made lowercase.
    adjusttemplate = models.ForeignKey(TbAdjusttemplate,to_field='templateid',db_column='AdjustTemplateID',db_constraint=False,verbose_name='早盘调水模板',null=True,blank=True)  # Field name made lowercase.
    liveadjusttemplateid = models.ForeignKey(TbAdjusttemplate,to_field='templateid',related_name='liveLeague',db_column='LiveAdjustTemplateID', blank=True, null=True,verbose_name='走地调水模板')
    handicapcount = models.IntegerField(db_column='HandicapCount',verbose_name='走地盘口显示数量',null=True,blank=True)  # Field name made lowercase.
    minodds = models.DecimalField(db_column='MinOdds', max_digits=18, decimal_places=2,null=True,blank=True,verbose_name='最小赔率',help_text='上下盘玩法非主盘口封盘最低赔率')  # Field name made lowercase.
    #groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    group = models.ForeignKey(to='TbLeagueGroup',db_constraint=False,db_column='GroupID',verbose_name='联赛组')  # Field name made lowercase.
    #reopenmarketsdelay = models.IntegerField(db_column='ReOpenMarketsDelay')  # Field name made lowercase.
    #liveadjusttemplateid = models.IntegerField(db_column='LiveAdjustTemplateID', blank=True, null=True)  # Field name made lowercase.
   
    
    class Meta:
        managed = False
        db_table = 'TB_Tournament'

    def __str__(self):
        return self.tournamentname


class TbBanner(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255, null=True,
                             verbose_name='标题')  # Field name made lowercase.
    picturename = CusPictureField(db_column='PictureName', verbose_name='app图片',
                                  max_length=255)  # Field name made lowercase
    pcpicturename = CusPictureField(db_column='PcPictureName', max_length=255, null=True,verbose_name ='pc图片')  # Field name made lowercase.
    # picturename = models.CharField(db_column='PictureName',verbose_name=_('Picture Name'), max_length=255)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', verbose_name=_('Priority'))  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', auto_now=True,
                                      verbose_name='创建时间')  # Field name made lowercase.
    #createuser = models.IntegerField(db_column='CreateUser', blank=True, null=True,
                                     #verbose_name='创建人')  # Field name made lowercase.
    createuser = CreateUserField(db_column='CreateUser', blank=True, null=True,
                                     verbose_name='创建人')  # Field name made lowercase.    
    
    description = models.CharField(db_column='Description', max_length=1024, blank=True,
                                   null=True, verbose_name='描述')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', verbose_name=_('status'), null=True, choices=ONLINE_STATUS,
                                 default=1)  # Field name made lowercase.
    navigateurl = models.CharField(db_column='NavigateUrl', max_length=512, verbose_name=_('Navigate Url'), blank=True,
                                   null=True)
    displaytype = models.IntegerField(db_column='DisplayType',default=0,choices=BANNER_DISPLAYTYPE,verbose_name='对内/对外')  # Field name made lowercase.
    #pcpicturename = models.CharField(db_column='PcPictureName', max_length=255, blank=True, null=True)  # Field name made lowercase.
   

    class Meta:
        managed = False
        db_table = 'TB_Banner'


class TbWithdrawlimitlog(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    # accountsn = models.CharField(db_column='AccountSN', max_length=36)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID')  # Field name made lowercase.
    cashflow = models.SmallIntegerField(db_column='CashFlow')  # Field name made lowercase.
    beforeamount = CusDecimalField(db_column='BeforeAmount', max_digits=18,
                                   decimal_places=4)  # Field name made lowercase.
    amount = CusDecimalField(db_column='Amount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    afteramount = CusDecimalField(db_column='AfterAmount', max_digits=18,
                                  decimal_places=4)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    creater = models.CharField(db_column='Creater', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_WithdrawLimitLog'


class Whiteiplist(models.Model):
    whiteiplistid = models.AutoField(db_column='WhiteIpListID', primary_key=True,
                                     verbose_name=_('WhiteIpListID'))  # Field name made lowercase.
    ip = models.CharField(db_column='Ip', max_length=16)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=200,
                              verbose_name=_('Remark'))  # Field name made lowercase.
    iswork = models.BooleanField(db_column='IsWork', verbose_name=_('IsWork'),
                                 default=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_WhiteIpList'


class Whiteuserlist(models.Model):
    whiteuserlistid = models.AutoField(db_column='WhiteUserListID', primary_key=True,
                                       verbose_name=_('WhiteUserListID'))  # Field name made lowercase.

    # userid = models.IntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    account = models.ForeignKey(TbAccount, db_column='UserID', db_constraint=False, verbose_name='用户昵称')

    memo = models.CharField(db_column='Memo', max_length=100, blank=True, null=True,
                            verbose_name=_('Memo'))  # Field name made lowercase.
    addtime = models.DateTimeField(db_column='AddTime', blank=True, null=True,
                                   verbose_name=_('AddTime'))  # Field name made lowercase.
    iswork = models.BooleanField(db_column='IsWork', verbose_name=_('IsWork'),
                                 default=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_WhiteUserList'


class TbBankcard(models.Model):
    bankcardid = models.AutoField(db_column='BankCardId', primary_key=True,
                                  verbose_name='卡ID')  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount, db_column='AccountId',
                                  db_constraint=False, verbose_name='用户昵称')  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=50)  # Field name made lowercase.
    #banktypeid = models.IntegerField(db_column='BankTypeID')  # Field name made lowercase.
    banktypeid = models.ForeignKey(to='TbBanktypes',db_constraint=False,db_column='BankTypeID',verbose_name='银行卡类型')  # Field name made lowercase.
    cardno = models.CharField(db_column='CardNo', max_length=50, verbose_name='卡号')  # Field name made lowercase.
    bankaccountname = models.CharField(db_column='BankAccountName', max_length=50,
                                       verbose_name='开户人')  # Field name made lowercase.
    bankaccountmobil = models.CharField(db_column='BankAccountMobil', max_length=50,
                                        verbose_name='银行预留手机号')  # Field name made lowercase.
    bankcity = models.CharField(db_column='BankCity', max_length=50, verbose_name='城市')  # Field name made lowercase.
    banktypename = models.CharField(db_column='BankTypeName', max_length=150,
                                    verbose_name='银行卡类型')  # Field name made lowercase.
    bankprovince = models.CharField(db_column='BankProvince', max_length=150,
                                    verbose_name='省份')  # Field name made lowercase.
    banksitename = models.CharField(db_column='BankSiteName', max_length=250,
                                    verbose_name='支行名称')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', auto_now=True,
                                      verbose_name='创建时间')  # Field name made lowercase.
    active = models.BooleanField(db_column='Active', verbose_name='激活')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BankCard'


class TbPaychanneljoinlevel(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    paychannelid = models.ForeignKey(to='TbPaychannel', db_column='PayChannelId',
                                     db_constraint=False, verbose_name='渠道', )  # Field name made lowercase.
    accountlevel = models.IntegerField(db_column='AccountLevel', verbose_name='风控等级', )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_PayChannelJoinLevel'


class TbSetting(models.Model):
    settingname = models.CharField(db_column='settingName', primary_key=True,
                                   max_length=200)  # Field name made lowercase.
    settingvalue = models.TextField(db_column='settingValue')  # Field name made lowercase. This field type is a guess.
    memo = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TB_Setting'


class TbPaychannel(models.Model):
    paychannelid = models.AutoField(db_column='PayChannelId', primary_key=True,
                                    verbose_name='渠道ID')  # Field name made lowercase.
    channelname = models.CharField(db_column='ChannelName', max_length=50,
                                   verbose_name='Apolo渠道名称')  # Field name made lowercase.
    channeltype = models.CharField(db_column='ChannelType', max_length=50,
                                   verbose_name='渠道名称')  # Field name made lowercase.
    active = models.BooleanField(db_column='Active', default=True)  # Field name made lowercase.
    minamount = models.DecimalField(db_column='MinAmount', max_digits=18, default = 0, 
                                    decimal_places=2, verbose_name='最小金额')  # Field name made lowercase.
    maxamount = models.DecimalField(db_column='MaxAmount', max_digits=18, default = 0,
                                    decimal_places=2, verbose_name='最大金额')  # Field name made lowercase.
    optionalamount = models.CharField(db_column='OptionalAmount', max_length=500, verbose_name='快捷金额',
                                      help_text='多个金额以,分割')  # Field name made lowercase.
    channelicon = models.CharField(db_column='ChannelIcon', max_length=150,
                                   verbose_name='Icon')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=150, verbose_name='备注',
                            blank=True)  # Field name made lowercase.
    channelgroupid = models.ForeignKey(to='TbPaychannelgroup', db_constraint=False, db_column='ChannelGroupID',
                                       verbose_name='分组')  # Field name made lowercase.
    isonline = models.BooleanField(db_column='IsOnline',verbose_name='是否三方')  # Field name made lowercase.
    isrecommend = models.BooleanField(db_column='IsRecommend',verbose_name = '推荐')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort',verbose_name='排序')  # Field name made lowercase.
    helpurl = CusPictureField(db_column='HelpUrl', max_length=255, blank=True, null=True,verbose_name='帮助地址')  # Field name made lowercase.

    tips = models.CharField(db_column='Tips', max_length=100, blank=True, null=True,verbose_name='提示')  # Field name made lowercase.
    ispaytocard = models.IntegerField(db_column='IsPayToCard', blank=True, null=True,verbose_name='是否转卡',default=0,choices=REQUIRED)  # Field name made lowercase.
    isfixedamount = models.BooleanField(db_column='IsFixedAmount',verbose_name='是否固定金额',default=False)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_PayChannel'

    def __str__(self):
        return self.channeltype


class TbWithdraw(models.Model):
    withdrawid = models.AutoField(db_column='WithdrawId', primary_key=True,
                                  verbose_name='记录ID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=2,
                                 verbose_name='金额')  # Field name made lowercase.
    orderid = models.CharField(db_column='OrderID', max_length=50, verbose_name='订单号')  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount, db_constraint=False, db_column='AccountID',
                                  verbose_name='昵称')  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=50)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', verbose_name='创建时间')  # Field name made lowercase.
    bankcardid = models.IntegerField(db_column='BankCardId')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=500, blank=True, null=True,
                            verbose_name='备注')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', choices=WITHDRAW_STATUS)  # Field name made lowercase.
    apollomsg = models.CharField(db_column='ApolloMsg', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    apollocode = models.CharField(db_column='ApolloCode', max_length=100, blank=True,
                                  null=True)  # Field name made lowercase.
    amounttype = models.IntegerField(db_column='AmountType', verbose_name='类型',
                                     choices=AMOUNT_TYPE)  # Field name made lowercase.
    confirmtime = models.DateTimeField(db_column='ConfirmTime', blank=True, null=True,
                                       verbose_name='处理时间')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Withdraw'
    
    def __str__(self):
        return str(self.withdrawid)


class TbRecharge(models.Model):
    rechargeid = models.AutoField(db_column='RechargeId', primary_key=True,
                                  verbose_name='记录ID')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=18, decimal_places=2,
                                 verbose_name='金额')  # Field name made lowercase.
    orderid = models.CharField(db_column='OrderID', max_length=50, verbose_name='订单号')  # Field name made lowercase.
    isauto = models.IntegerField(db_column='IsAuto', verbose_name='自动', default=0,choices=IS_AUTO,
                                 blank=True)  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount, db_column='AccountID', db_constraint=False,
                                  verbose_name='昵称', null=True)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=255)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', verbose_name='创建时间')  # Field name made lowercase.
    channelname = models.CharField(db_column='ChannelName', max_length=50)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', choices=RECHARGE_STATUS)  # Field name made lowercase.
    # channelid = models.IntegerField(db_column='ChannelID')  # Field name made lowercase.
    channelid = models.ForeignKey(to=TbPaychannel, db_constraint=False, db_column='ChannelID',
                                  verbose_name='充值渠道', null=True)  # Field name made lowercase.
    apollomsg = models.CharField(db_column='ApolloMsg', max_length=500)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=150, verbose_name='备注')  # Field name made lowercase.
    amounttype = models.IntegerField(db_column='AmountType', choices=AMOUNT_TYPE,
                                     verbose_name='类型')  # Field name made lowercase.
    apolloinfo = models.CharField(db_column='ApolloInfo', max_length=800, blank=True,
                                  null=True)  # Field name made lowercase.
    confirmtime = models.DateTimeField(db_column='ConfirmTime', blank=True, null=True,
                                       verbose_name='处理时间')  # Field name made lowercase.
    confirmamount = models.DecimalField(db_column='ConfirmAmount', max_digits=18, decimal_places=2,
                                        verbose_name='确认金额')  # Field name made lowercase.
    consumeamount = models.DecimalField(db_column='ConsumeAmount', max_digits=18, decimal_places=2)  # Field name made lowercase.
    consumestatus = models.IntegerField(db_column='ConsumeStatus')  # Field name made lowercase.
    bankcardno = models.CharField(db_column='BankCardNo', max_length=50, blank=True, null=True,verbose_name='申请转账卡号')  # Field name made lowercase.
    accountip = models.CharField(db_column='AccountIP', max_length=50, blank=True, null=True,verbose_name='充值ip')  # Field name made lowercase.    

    class Meta:
        managed = False
        db_table = 'TB_Recharge'
    
    def __str__(self):
        return str(self.rechargeid)


class TbParameterinfo(models.Model):
    tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    tag = models.CharField(db_column='Tag', max_length=50)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=50, verbose_name='配置值')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=50, blank=True, null=True,
                            verbose_name='配置项')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive', verbose_name='状态')  # Field name made lowercase.
    daysnumber = models.IntegerField(db_column='DaysNumber', verbose_name='天数')  # Field name made lowercase.
    leveltype = models.CharField(db_column='LevelType', max_length=50,
                                 verbose_name='用户等级')  # Field name made lowercase.
    levelid = models.IntegerField(db_column='LevelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_ParameterInfo'


class TbBanktypes(models.Model):
    banktypeid = models.AutoField(db_column='BankTypeID', primary_key=True,
                                  verbose_name='编号')  # Field name made lowercase.
    banktypename = models.CharField(db_column='BankTypeName', max_length=50, verbose_name='银行卡类型',
                                    unique=True)  # Field name made lowercase.
    active = models.BooleanField(db_column='Active', default=True)  # Field name made lowercase.
    img = CusPictureField(db_column='Img', max_length=200, blank=True, null=True)
    # img = models.CharField(db_column='Img', max_length=200, blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort', verbose_name='排序')  # Field name made lowercase.
    bgimg = CusPictureField(db_column='BgImg', max_length=200, blank=True, null=True,
                            verbose_name='背景图')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BankTypes'
    
    def __str__(self):
        return self.banktypename

class TbAgentcommission(models.Model):
    commid = models.BigAutoField(db_column='CommID', primary_key=True, verbose_name='记录ID')  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount, db_column='AccountID',
                                  db_constraint=False, verbose_name='用户昵称')  # Field name made lowercase.
    agent = models.BigIntegerField(db_column='Agent')  # Field name made lowercase.
    amount = CusDecimalField(db_column='Amount', max_digits=18, decimal_places=4, blank=True,
                             null=True, verbose_name='佣金')  # Field name made lowercase.
    daus = models.IntegerField(db_column='DAUs', blank=True, null=True,
                               verbose_name='活跃用户数')  # Field name made lowercase.
    lostamount = CusDecimalField(db_column='LostAmount', max_digits=18, decimal_places=4, blank=True,
                                 null=True, verbose_name='本月净盈利')  # Field name made lowercase.
    balancelostamount = CusDecimalField(db_column='BalanceLostAmount', max_digits=18, decimal_places=4, blank=True,
                                        null=True, verbose_name='累计净盈利')  # Field name made lowercase.
    percentage = models.DecimalField(db_column='Percentage', max_digits=18, decimal_places=2, blank=True,
                                     null=True, verbose_name='佣金比例')  # Field name made lowercase.
    settleyear = models.IntegerField(db_column='SettleYear', blank=True, null=True,
                                     verbose_name='结算年')  # Field name made lowercase.
    settlemonth = models.IntegerField(db_column='SettleMonth', blank=True, null=True,
                                      verbose_name='结算月')  # Field name made lowercase.
    settledate = models.CharField(db_column='SettleDate', max_length=10, blank=True,
                                  null=True, verbose_name='结算日期')  # Field name made lowercase.
    creater = models.CharField(db_column='Creater', max_length=100, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True,
                                      verbose_name='创建时间')  # Field name made lowercase.
    updater = models.CharField(db_column='Updater', max_length=100, blank=True, null=True)  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime', blank=True, null=True)  # Field name made lowercase.
    applytime = models.DateTimeField(db_column='ApplyTime', blank=True, null=True,
                                     verbose_name='审核时间')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True, default=0,
                                 choices=AGENT_COMMISION_STATUS)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True,
                                   null=True)  # Field name made lowercase.
    betamount = CusDecimalField(db_column='BetAmount', max_digits=18, decimal_places=4, blank=True,
                                null=True, verbose_name='投注金额')  # Field name made lowercase.
    bonusamount = CusDecimalField(db_column='BonusAmount', max_digits=18, decimal_places=4, blank=True,
                                  null=True, verbose_name='返水')  # Field name made lowercase.
    expendamount = CusDecimalField(db_column='ExpendAmount', max_digits=18, decimal_places=4, blank=True,
                                   null=True, verbose_name='系统红利')  # Field name made lowercase.
    rechargeamount = CusDecimalField(db_column='RechargeAmount', max_digits=18, decimal_places=4, blank=True,
                                     null=True, verbose_name='充值金额')  # Field name made lowercase.
    withdrawalamount = CusDecimalField(db_column='WithdrawalAmount', max_digits=18, decimal_places=4, blank=True,
                                       null=True, verbose_name='提现金额')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AgentCommission'


class TbPaychannelgroup(models.Model):
    groupid = models.AutoField(db_column='GroupID', primary_key=True,verbose_name='ID')  # Field name made lowercase.
    groupway = models.CharField(db_column='GroupWay', max_length=50,verbose_name='组名')  # Field name made lowercase.
    groupicon = models.CharField(db_column='GroupIcon', max_length=50,verbose_name='图标')  # Field name made lowercase.
    groupsubtitle = models.CharField(db_column='GroupSubTitle', max_length=50, blank=True,
                                     null=True,verbose_name='子标题')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort',verbose_name='排序')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_PayChannelGroup'

    def __str__(self):
        return self.groupway


class TbAgentleavemsg(models.Model):
    msgid = models.BigAutoField(db_column='MsgID', primary_key=True)  # Field name made lowercase.
    accountid = models.ForeignKey(to=TbAccount, db_column='AccountID', db_constraint=False,
                                  verbose_name='用户昵称')  # Field name made lowercase.
    msg = models.CharField(db_column='Msg', max_length=3000, blank=True, null=True,
                           verbose_name='内容')  # Field name made lowercase.
    answer = models.CharField(db_column='Answer', max_length=3000, blank=True, null=True,
                              verbose_name='回复内容')  # Field name made lowercase.
    isanswer = models.NullBooleanField(db_column='IsAnswer', verbose_name='是否回复')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True,
                                      verbose_name='创建时间')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=3000, blank=True, null=True,
                             verbose_name='标题')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AgentLeaveMsg'


class TbPaychannelblackaccount(models.Model):
    blackaccountid = models.AutoField(db_column='BlackAccountID', primary_key=True)  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountID', blank=True, null=True)  # Field name made lowercase.
    accountid = models.ForeignKey(db_column='AccountID',to=TbAccount, blank=True, null=True,verbose_name='账号') 
    account = models.CharField(db_column='Account', max_length=255, blank=True, null=True,verbose_name='账号')  # Field name made lowercase.
    iswork = models.BooleanField(db_column='IsWork',default=True,verbose_name='启用')  # Field name made lowercase.
    #paychannelid = models.IntegerField(db_column='PayChannelID')  # Field name made lowercase.
    paychannelid = models.ForeignKey(to=TbPaychannel, db_column='PayChannelID', db_constraint=False,
                                     verbose_name='充值渠道')  # Field name made lo    wercase.

    class Meta:
        managed = False
        db_table = 'TB_PayChannelBlackAccount'


class TbPaychannelblackiprange(models.Model):
    blackiprangelistid = models.AutoField(db_column='BlackIpRangeListID', primary_key=True,
                                          verbose_name=_('ID'))  # Field name made lowercase.
    startip = models.CharField(db_column='StartIp', max_length=16,
                               verbose_name=_('StartIp'))  # Field name made lowercase.
    startipnum = models.BigIntegerField(db_column='StartIpNum',
                                        verbose_name=_('StartIpNum'))  # Field name made lowercase.
    endip = models.CharField(db_column='EndIp', max_length=16, verbose_name=_('EndIp'),help_text='起始ip相同则表示控制单个ip')  # Field name made lowercase.
    endipnum = models.BigIntegerField(db_column='EndIpNum', verbose_name=_('EndIpNum'))  # Field name made lowercase.

    iswork = models.BooleanField(db_column='IsWork', verbose_name=_('IsWork'),
                                 default=True)  # Field name made lowercase.
    paychannelid = models.ForeignKey(to=TbPaychannel, db_column='PayChannelID', db_constraint=False,
                                     verbose_name='充值渠道')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_PayChannelBlackIPRange'


class TbOperationlog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=500, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=2000)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=1000)  # Field name made lowercase.
    createuser = models.CharField(db_column='CreateUser', max_length=100, blank=True,
                                  null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_OperationLog'


class TbAreablacklist(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='编号')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', default=1)  # Field name made lowercase.
    area = models.CharField(db_column='Area', max_length=200, verbose_name='地区')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AreaBlackList'


class TbRechargeareablacklist(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', default=1)  # Field name made lowercase.
    paychannelid = models.ForeignKey(to=TbPaychannel, db_column='PayChannelID', db_constraint=False,
                                     verbose_name='充值渠道')  # Field name made lowercase.
    area = models.CharField(db_column='Area', max_length=200, verbose_name='地区')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_RechargeAreaBlackList'


class TbWhiteiprangelist(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='编号')  # Field name made lowercase.
    startip = models.CharField(db_column='StartIp', max_length=16, blank=True, null=True,
                               verbose_name='开始IP')  # Field name made lowercase.
    startipnum = models.BigIntegerField(db_column='StartIpNum', blank=True, null=True)  # Field name made lowercase.
    endip = models.CharField(db_column='EndIp', max_length=16, blank=True, null=True,
                             verbose_name='结束IP')  # Field name made lowercase.
    endipnum = models.BigIntegerField(db_column='EndIpNum', blank=True, null=True)  # Field name made lowercase.
    iswork = models.BooleanField(db_column='IsWork', default=True, verbose_name='状态')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True, default=0, verbose_name='类型',
                               choices=WhiteIP_Type)

    class Meta:
        managed = False
        db_table = 'TB_WhiteIpRangeList'


class TbOperationlog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=500, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=2000, verbose_name='内容')  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=1000, verbose_name='备注')  # Field name made lowercase.
    createuser = models.CharField(db_column='CreateUser', max_length=100, blank=True, null=True,
                                  verbose_name='操作人')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', verbose_name='创建时间', auto_now_add= True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_OperationLog'


# class TbLeagueGroup(models.Model):
# groupid = models.IntegerField(db_column='GroupId', primary_key=True, blank= True)  # Field name made lowercase.
# groupname = models.CharField(db_column='GroupName', max_length=50)  # Field name made lowercase.
# enabled = models.SmallIntegerField(db_column='Enabled', default = 1, blank= True)  # Field name made lowercase.
##members = models.ManyToManyField(
##TbTournament,
##through='TbLeagueidInGroup',
##through_fields=('groupid', 'leagueid'),
##)

# class Meta:
# managed = False
# db_table = 'TB_League_Group'

class TbLeagueGroup(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    groupname = models.CharField(db_column='GroupName', max_length=50, verbose_name='分组名')  # Field name made lowercase.
    enabled = models.SmallIntegerField(db_column='Enabled', default=1, blank=True,verbose_name='启用')  # Field name made lowercase.
    riskleveldelay = models.CharField(db_column='RiskLevelDelay', max_length=3000,verbose_name='风控等级延迟')  # Field name made lowercase
    minodds = models.DecimalField(db_column='MinOdds', max_digits=18, decimal_places=2,verbose_name='最小赔率',help_text='上下盘玩法非主盘口封盘最低赔率')  # Field name made lowercase.
    handicapcount = models.IntegerField(db_column='HandicapCount',verbose_name='走地盘口显示数量')  # Field name made lowercase.
    ticketdelay = models.IntegerField(db_column='TicketDelay',verbose_name='注单延时',default=0,validators=[int_0_p])  # Field name made lowercase.
    #adjusttemplateid = models.IntegerField(db_column='AdjustTemplateID')  # Field name made lowercase.
    adjusttemplate = models.ForeignKey(TbAdjusttemplate,to_field='templateid',db_column='AdjustTemplateID',db_constraint=False,verbose_name='早盘调水模板')  # Field name made lowercase.
    liveadjusttemplateid = models.ForeignKey(TbAdjusttemplate,to_field='templateid',db_column='LiveAdjustTemplateID',related_name='liveLeagueGroup',null=True,verbose_name='走地调水模板')
    weight = models.DecimalField(db_column='Weight', max_digits=18, decimal_places=4,verbose_name='权重')  # Field name made lowercase.
    #reopenmarketsdelay = models.IntegerField(db_column='ReOpenMarketsDelay',verbose_name='进球后延迟开盘时间',help_text='单位秒',default=0)  # Field name made lowercase.
    #marketweight = models.CharField(verbose_name='玩法权重', db_column='MarketWeight', max_length=6000,blank=True)  # Field name made lowercase. This field type is a guess.  # Field name made lowercase. This field type is a guess.
    #liveadjusttemplateid = models.IntegerField(db_column='LiveAdjustTemplateID', blank=True, null=True,verbose_name='走地调水模板')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_League_Group'
    
    def __str__(self):
        return self.groupname

class TbLeaguegroupMarketweight(models.Model):
    tid = models.AutoField(db_column='TID', primary_key=True)  # Field name made lowercase.
    #leaguegroupid = models.IntegerField(db_column='LeagueGroupID')  # Field name made lowercase.
    leaguegroup = models.ForeignKey(to=TbLeagueGroup,db_constraint=False, db_column='LeagueGroupID',verbose_name='玩法组')
    #marketid = models.IntegerField(db_column='MarketID')  # Field name made lowercase.
    market = models.ForeignKey(to=TbMarkets,db_constraint=False,db_column='MarketID',verbose_name='玩法')
    preweight = models.DecimalField(db_column='PreWeight', max_digits=18, decimal_places=4,verbose_name='早盘权重')  # Field name made lowercase.
    liveweight = models.DecimalField(db_column='LiveWeight', max_digits=18, decimal_places=4,verbose_name='走地权重')  # Field name made lowercase.
    extendweight = models.DecimalField(db_column='ExtendWeight', max_digits=18, decimal_places=2,default=1,verbose_name='扩展权重')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_LeagueGroup_MarketWeight'
    
    def __str__(self):
        return '玩法权重'

class TbLeagueGroupSpread(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupId')  # Field name made lowercase.
    # groupid = models.ForeignKey(to= TbLeagueGroup, db_constraint= False, db_column='GroupId')
    bettype = models.IntegerField(db_column='BetType')  # Field name made lowercase.
    periodtype = models.IntegerField(db_column='PeriodType')  # Field name made lowercase.
    spread = models.DecimalField(db_column='Spread', max_digits=18, decimal_places=3, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_League_Group_Spread'


class TbLeagueidInGroup(models.Model):
    groupid = models.IntegerField(db_column='GroupId')  # Field name made lowercase.
    # groupid = models.ForeignKey(to= TbLeagueGroup, db_constraint= False, db_column='GroupId')
    leagueid = models.IntegerField(db_column='LeagueId', primary_key=True)  # Field name made lowercase.

    # leagueid = models.ForeignKey(to = TbTournament, db_constraint= False, db_column='LeagueId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_LeagueId_In_Group'


class TbAgentnotice(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=1024, blank=False, null=True,
                             verbose_name='标题')  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=512, blank=True, null=True,
                           verbose_name='链接Url')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', auto_now=True,
                                      verbose_name='创建时间')  # Field name made lowercase.

    createuser = CreateUserField(db_column='CreateUser', blank=True, null=True,
                                 verbose_name='创建人')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', default=1, null=True,
                                 choices=ONLINE_STATUS)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True, default='',
                               verbose_name='内容')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_AgentNotice'


#class TbMatchesBasketball(models.Model):
    #tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    #categoryid = models.IntegerField(db_column='CategoryID')  # Field name made lowercase.
    
    ##tournamentid = models.ForeignKey(to='TbTournamentBasketball', db_constraint=False, db_column='TournamentID')
    #tournamentid = models.IntegerField(db_column='TournamentID')  # Field name made lowercase.
    #tournamentzh = models.CharField(db_column='TournamentZH', max_length=100, blank=True, null=True,verbose_name='联赛')  # Field name made lowercase.
    #matchid = models.BigIntegerField(db_column='MatchID', primary_key=True)  # Field name made lowercase.
    #prematchdate = models.DateTimeField(db_column='PreMatchDate')  # Field name made lowercase.
    #matchdate = models.DateTimeField(db_column='MatchDate',verbose_name='比赛日期')  # Field name made lowercase.
    #currentperiodstart = models.DateTimeField(db_column='CurrentPeriodStart', blank=True, null=True)  # Field name made lowercase.
    #team1id = models.IntegerField(db_column='Team1ID')  # Field name made lowercase.
    #superteam1id = models.BigIntegerField(db_column='SuperTeam1Id')  # Field name made lowercase.
    #team1zh = models.CharField(db_column='Team1ZH', max_length=100, blank=True, null=True,verbose_name='主队')  # Field name made lowercase.
    #team2id = models.IntegerField(db_column='Team2ID')  # Field name made lowercase.
    #superteam2id = models.BigIntegerField(db_column='SuperTeam2Id')  # Field name made lowercase.
    #team2zh = models.CharField(db_column='Team2ZH', max_length=100, blank=True, null=True,verbose_name='客队')  # Field name made lowercase.
    #matchscore = models.CharField(db_column='MatchScore', max_length=20,verbose_name='比分', blank = True)  # Field name made lowercase.
    #winner = models.IntegerField(db_column='Winner',verbose_name='获胜者',choices=WINNER)  # Field name made lowercase.
    #statuscode = models.IntegerField(db_column='StatusCode',verbose_name='状态',choices=BASKETBALL_MATCH_STATUS)  # Field name made lowercase.
    #roundinfo = models.IntegerField(db_column='RoundInfo')  # Field name made lowercase.
    #isrecommend = models.BooleanField(db_column='IsRecommend',verbose_name='推荐')  # Field name made lowercase.
    #livebet = models.BooleanField(db_column='LiveBet',verbose_name='走地')  # Field name made lowercase.
    #generatedat = models.DateTimeField(db_column='GeneratedAt')  # Field name made lowercase.
    #createtime = models.DateTimeField(db_column='CreateTime',verbose_name='创建时间')  # Field name made lowercase.
    #weights = models.DecimalField(db_column='Weights', max_digits=18, decimal_places=2)  # Field name made lowercase.
    #uniquetournamentid = models.BigIntegerField(db_column='UniqueTournamentId')  # Field name made lowercase.
    #period1score = models.CharField(db_column='Period1Score', max_length=20,verbose_name='半场比分', blank = True)  # Field name made lowercase.
    #eventid = models.CharField(db_column='EventID', unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    #tournamenten = models.CharField(db_column='TournamentEN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    #team1en = models.CharField(db_column='Team1EN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    #team2en = models.CharField(db_column='Team2EN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    #homescore = models.IntegerField(db_column='HomeScore')  # Field name made lowercase.
    #awayscore = models.IntegerField(db_column='AwayScore')  # Field name made lowercase.
    #team1icon = models.CharField(db_column='Team1Icon', max_length=255, blank=True, null=True)  # Field name made lowercase.
    #team2icon = models.CharField(db_column='Team2Icon', max_length=255, blank=True, null=True)  # Field name made lowercase.
    #terminator = models.CharField(db_column='Terminator', max_length=20, blank=True, null=True)  # Field name made lowercase.
    #ishidden = models.BooleanField(db_column='IsHidden')  # Field name made lowercase.
    #marketstatus = models.IntegerField(db_column='MarketStatus',verbose_name='市场状态',choices=MATCH_MARKETSTATUS)  # Field name made lowercase.
    #satimestam = models.DateTimeField(db_column='SaTimestam')  # Field name made lowercase.
    #closelivebet = models.IntegerField(db_column='CloseLiveBet', blank=True, null=True)  # Field name made lowercase.
    #matchstatustype = models.CharField(db_column='MatchStatusType', max_length=50, blank = True)  # Field name made lowercase.
    #specialcategoryid = models.IntegerField(db_column='SpecialCategoryID')  # Field name made lowercase.
    #mainleagueid = models.IntegerField(db_column='MainLeagueID')  # Field name made lowercase.
    #mainhomeid = models.IntegerField(db_column='MainHomeID')  # Field name made lowercase.
    #mainawayid = models.IntegerField(db_column='MainAwayID')  # Field name made lowercase.
    #mainmatchid = models.IntegerField(db_column='MainMatchID')  # Field name made lowercase.
    #maineventid = models.CharField(db_column='MainEventID', max_length=100)  # Field name made lowercase.
    #settlestatus = models.IntegerField(db_column='SettleStatus', blank=True, null=True)  # Field name made lowercase.    
    #settletime = models.DateTimeField(db_column='SettleTime', blank=True, null=True)  # Field name made lowercase.
    #source = models.IntegerField(db_column='Source',choices=DATA_SOURCE)  # Field name made lowercase.
    #liveodds = models.BooleanField(db_column='LiveOdds',verbose_name='走地盘')  # Field name made lowercase.
    #q1score = models.CharField(db_column='Q1Score', max_length=20,blank=True,verbose_name='第一小节比分')  # Field name made lowercase.
    #q2score = models.CharField(db_column='Q2Score', max_length=20,blank=True,verbose_name='第二小节比分')  # Field name made lowercase.
    #q3score = models.CharField(db_column='Q3Score', max_length=20,blank=True,verbose_name='第三小节比分')  # Field name made lowercase.
    #q4score = models.CharField(db_column='Q4Score', max_length=20,blank=True,verbose_name='第四小节比分')  # Field name made lowercase.
    #overtimescore = models.CharField(db_column='OvertimeScore', max_length=20,blank=True,verbose_name='加时赛比分')  # Field name made lowercase.    
    
    #class Meta:
        #managed = False
        #db_table = 'TB_Matches_Basketball'
    
    #def __str__(self):
        #return '[%(matchid)s]%(home)s vs %(away)s' % {'matchid': self.matchid, 'home': self.team1zh,
                                                      #'away': self.team2zh, }    
        
#class TbTournamentBasketball(models.Model):
    #tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    #tournamentid = models.IntegerField(db_column='TournamentID', verbose_name='联赛ID',unique=True)  # Field name made lowercase.
    #tournamentname = models.CharField(db_column='TournamentName', max_length=200, verbose_name = '联赛名称')  # Field name made lowercase.
    #categoryid = models.IntegerField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    #createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True)  # Field name made lowercase.
    #uniquetournamentid = models.IntegerField(db_column='UniqueTournamentID', verbose_name='联赛ID')  # Field name made lowercase.
    #issubscribe = models.IntegerField(db_column='IsSubscribe', verbose_name='已订阅')  # Field name made lowercase.
    #sort = models.IntegerField(db_column='Sort', blank=True, null=True, verbose_name= '排序')  # Field name made lowercase.
    #typegroupswitch = models.CharField(db_column='TypeGroupSwitch', max_length=200, blank=True, null=True, verbose_name='已关闭玩法')  # Field name made lowercase.
    #closelivebet = models.IntegerField(db_column='CloseLiveBet', blank=True, null=True, verbose_name='关闭滚球')  # Field name made lowercase.
    #specialcategoryid = models.IntegerField(db_column='SpecialCategoryID')  # Field name made lowercase.
    #source = models.IntegerField(db_column='Source',choices=DATA_SOURCE)  # Field name made lowercase.
    #weight = models.DecimalField(db_column='Weight', max_digits=18, decimal_places=4,verbose_name='权重')  # Field name made lowercase.
     
    #class Meta:
        #managed = False
        #db_table = 'TB_Tournament_Basketball'
    
    #def __str__(self):
        #return self.tournamentname   

    
class TbTournamentLivebet(models.Model):
    tournamentid = models.IntegerField(db_column='TournamentID', primary_key=True)  # Field name made lowercase.
    tournamentname = models.CharField(db_column='TournamentName', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True)  # Field name made lowercase.
    uniquetournamentid = models.IntegerField(db_column='UniqueTournamentID', blank=True, null=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID', blank=True, null=True)  # Field name made lowercase.
    isfeedon = models.IntegerField(db_column='IsFeedOn', blank=True, null=True)  # Field name made lowercase.
    weights = models.FloatField(db_column='Weights', blank=True, null=True)  # Field name made lowercase.
    islivebet = models.IntegerField(db_column='IsLiveBet', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_Tournament_LiveBet'

class TbUserConst(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nickname = models.CharField(db_column='NickName', max_length=100, verbose_name = '昵称')  # Field name made lowercase.
    avatar = CusPictureField(db_column='Avatar', max_length=512, blank=True, null=True, verbose_name = '头像')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_User_Const'
        
    def __str__(self):
        return self.nickname
    
class TbUserRank(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    #userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    userid = models.ForeignKey(to= TbUserConst, db_constraint= False, db_column='UserId', verbose_name = '虚拟用户')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank= False, choices= RANK_TYPE, verbose_name= '榜单' )  # Field name made lowercase.
    period = models.IntegerField(db_column='Period', choices= RANK_PERIAD, verbose_name= '周期')  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled', verbose_name = '启用', default = 1)  # Field name made lowercase.
    parlayid = models.ForeignKey(to= TbParlayrules, db_constraint= False, default = 0, blank = True, db_column='ParlayId', verbose_name= '类别' )  # Field name made lowercase.
    #parlayid = models.IntegerField(db_column='ParlayId', verbose_name= '类别' )  # Field name made lowercase.
    value = CusDecimalField(db_column='Value', max_digits=18, decimal_places=4, verbose_name= '数值', digits = 2)  # Field name made lowercase.
    #value = models.DecimalField(db_column='Value', max_digits=18, decimal_places=4, verbose_name= '数值')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'TB_User_Rank'
  
class TbUserLog(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    bid = models.CharField(db_column='BId', max_length=64)  # Field name made lowercase.
    #accountid = models.IntegerField(db_column='AccountId')  # Field name made lowercase.
    account = models.ForeignKey(to=TbAccount,db_column='AccountId',verbose_name='账号',)
    ipaddress = models.CharField(db_column='IpAddress', max_length=16,verbose_name='IP地址')  # Field name made lowercase.
    operatetype = models.IntegerField(db_column='OperateType',choices=OPERATE_TYPE,verbose_name='操作类型')  # Field name made lowercase.
    deviceid = models.CharField(db_column='DeviceId', max_length=255, blank=True, null=True,verbose_name='设备ID')  # Field name made lowercase.
    terminal = models.IntegerField(db_column='Terminal',choices=TERMINAL_TYPE,verbose_name='终端')  # Field name made lowercase.
    area = models.CharField(db_column='Area', max_length=255, blank=True, null=True,verbose_name='区域')  # Field name made lowercase.
    arearemark = models.CharField(db_column='AreaRemark', max_length=255, blank=True, null=True,verbose_name = '区域标记')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='创建时间')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_User_Log'
        
class TbSporttypes(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID', unique=True,verbose_name='类型ID')  # Field name made lowercase.
    sportname = models.CharField(db_column='SportName', max_length=100,verbose_name='类型名')  # Field name made lowercase.
    sportnamezh = models.CharField(db_column='SportNameZH', max_length=100,verbose_name='类型中文名')  # Field name made lowercase.
    onlinetime = models.DateTimeField(db_column='OnlineTime', blank=True, null=True,verbose_name='上线时间')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status',verbose_name='状态')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort', blank=True, null=True,verbose_name='排序')  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled',verbose_name='启用')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True,auto_now_add=True, null=True,verbose_name='创建时间')  # Field name made lowercase.
    #updater = models.CharField(db_column='Updater', max_length=100, blank=True, null=True,verbose_name='更新人')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime', blank=True, null=True,auto_now=True,verbose_name='更新时间')  # Field name made lowercase.
    #updateuser = models.IntegerField(db_column='UpdateUser', blank=True, null=True)  # Field name made lowercase.
    updateuser = UpdateUserField(db_column='UpdateUser',verbose_name='更新人', blank=True, null=True)  # Field name made lowercase.
    #source = models.IntegerField(db_column='Source',choices=DATA_SOURCE)  # Field name made lowercase.
    #sportimg_s = models.CharField(db_column='SportImg_S', max_length=255, blank=True, null=True)  # Field name made lowercase.
    #sportimg_m = models.CharField(db_column='SportImg_M', max_length=255, blank=True, null=True)  # Field name made lowercase.
    #sportimg_l = models.CharField(db_column='SportImg_L', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sportimg_s = CusPictureField(db_column='SportImg_S', max_length=255, blank=True, null=True,verbose_name='小图')  # Field name made lowercase.
    sportimg_m = CusPictureField(db_column='SportImg_M', max_length=255, blank=True, null=True,verbose_name='中图')  # Field name made lowercase.
    sportimg_l = CusPictureField(db_column='SportImg_L', max_length=255, blank=True, null=True,verbose_name='大图')  # Field name ma
    new = models.BooleanField(db_column='New',verbose_name = '最新上线')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_SportTypes'

    def __str__(self):
        return self.sportnamezh


class TbTrendstatistics(models.Model):
    tid = models.BigAutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='时间')  # Field name made lowercase.
    betnum = models.BigIntegerField(db_column='BetNum',verbose_name='投注单数')  # Field name made lowercase.
    betamount = models.DecimalField(db_column='BetAmount', max_digits=18, decimal_places=4,verbose_name='投注金额')  # Field name made lowercase.
    finishbetamount = models.DecimalField(db_column='FinishBetAmount', max_digits=18, decimal_places=4,verbose_name='(已结算)投注金额')  # Field name made lowercase.
    turnover = models.DecimalField(db_column='Turnover', max_digits=18, decimal_places=4,verbose_name='流水')  # Field name made lowercase.
    betoutcome = models.DecimalField(db_column='BetOutCome', max_digits=18, decimal_places=4,verbose_name='派奖金额')  # Field name made lowercase.
    bonusamount = models.DecimalField(db_column='BonusAmount', max_digits=18, decimal_places=4,verbose_name='反水金额')  # Field name made lowercase.
    firstrechargeamount = models.DecimalField(db_column='FirstRechargeAmount', max_digits=18, decimal_places=4,verbose_name='首存金额')  # Field name made lowercase.
    secondrechargeamount = models.DecimalField(db_column='SecondRechargeAmount', max_digits=18, decimal_places=4,verbose_name='再存金额')  # Field name made lowercase.
    birthdayamount = models.DecimalField(db_column='BirthdayAmount', max_digits=18, decimal_places=4,verbose_name='生日礼金')  # Field name made lowercase.
    rescueamount = models.DecimalField(db_column='RescueAmount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    deductionamount = models.DecimalField(db_column='DeductionAmount', max_digits=18, decimal_places=4,verbose_name='')  # Field name made lowercase.
    ddditionamount = models.DecimalField(db_column='DdditionAmount', max_digits=18, decimal_places=4)  # Field name made lowercase.
    ebankamount = models.DecimalField(db_column='EbankAmount', max_digits=18, decimal_places=4,)  # Field name made lowercase.
    backendamount = models.DecimalField(db_column='BackendAmount', max_digits=18, decimal_places=4,verbose_name='礼金')  # Field name made lowercase.
    userprofit = models.DecimalField(db_column='UserProfit', max_digits=18, decimal_places=4,verbose_name='亏盈')  # Field name made lowercase.
    starttime = models.DateField(db_column='StartTime',verbose_name='时间',help_text='db 是 Datetime')  # Field name made lowercase.
    #starttime = models.DateTimeField(db_column='StartTime',verbose_name='时间')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.
    activityamount = models.DecimalField(db_column='ActivityAmount', max_digits=18, decimal_places=4,verbose_name='活动+调整')  # Field name made lowercase.
    rechargeamount = models.DecimalField(db_column='RechargeAmount', max_digits=18, decimal_places=4,verbose_name='充值金额')  # Field name made lowercase.
    withdrawamount = models.DecimalField(db_column='WithdrawAmount', max_digits=18, decimal_places=4,verbose_name='提现金额')  # Field name made lowercase.
    betusernum = models.IntegerField(db_column='BetUserNum',verbose_name='投注人数')  # Field name made lowercase.
    newusernum = models.IntegerField(db_column='NewUserNum',verbose_name='注册人数')  # Field name made lowercase.
    withdrawusernum = models.IntegerField(db_column='WithdrawUserNum',verbose_name='提现人数')  # Field name made lowercase.
    rechargeusernum = models.IntegerField(db_column='RechargeUserNum',verbose_name='充值人数')  # Field name made lowercase.
    loginusernum = models.IntegerField(db_column='LoginUserNum',verbose_name='登录用户数')  # Field name made lowercase.
    rechargeonsignindaynum = models.IntegerField(db_column='RechargeOnSignInDayNum',verbose_name='每日首冲')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_TrendStatistics'
 
 
class TbTodolist(models.Model):
    tid = models.BigAutoField(db_column='TID', primary_key=True)  # Field name made lowercase.
    category = models.IntegerField(db_column='Category',verbose_name='类别',choices=TODOLIST_CATEGORY)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=200,verbose_name='标题')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=1000,verbose_name='内容')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status',verbose_name='状态',default=0,choices=TODOLIST_STATUS)  # Field name made lowercase.
    rfid = models.CharField(db_column='RFID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime',verbose_name='创建时间',auto_now_add=True)  # Field name made lowercase.
    #operateuserno = models.IntegerField(db_column='OperateUserNo',verbose_name='操作人')  # Field name made lowercase.
    operateuser = UpdateUserField(db_column='OperateUserNo',verbose_name='操作人')  
    operatetime = models.DateTimeField(db_column='OperateTime', blank=True, null=True,auto_now=True,verbose_name='更新时间')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_ToDoList'    
    
    def __str__(self):
        if len(self.title)>10:
            return '%s...'%self.title[:10]
        else:
            return self.title
        
        
class TbMarketlistwithsport(models.Model):
    tid = models.AutoField(db_column='TID', primary_key=True)  # Field name made lowercase.
    #sportid = models.IntegerField(db_column='SportID',verbose_name='体育类型')  # Field name made lowercase.
    sport = models.ForeignKey(to=TbSporttypes,db_column='SportID',to_field='sportid',db_constraint=False,verbose_name='体育类型')
    #marketid = models.IntegerField(db_column='MarketID',verbose_name='玩法')  # Field name made lowercase.
    market = models.ForeignKey(to=TbMarkets,db_constraint=False,db_column='MarketID',verbose_name='玩法') 
    marketshowname = models.CharField(db_column='MarketShowName', max_length=200, blank=True, null=True,verbose_name='列表展示名')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort',verbose_name='排序')  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled',verbose_name='启用')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True,verbose_name='描述')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_MarketListWithSport'
        
class TbUserex(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True,verbose_name='账号')  # Field name made lowercase.
    extnumber = models.CharField(db_column='ExtNumber', max_length=50, blank=True, null=True,verbose_name='分机号')  # Field name made lowercase.
    
    usedpassword = models.CharField(db_column='UsedPassword', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    passwordexpiretime = models.DateTimeField(db_column='PasswordExpireTime', blank=True, null=True,verbose_name='密码过期')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'TB_UserEx'
    
    def __str__(self):
        return self.extnumber or ''
    
class TbTeammapping(models.Model):
    id = models.AutoField(db_column='ID',primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    source = models.IntegerField(db_column='Source')  # Field name made lowercase.
    sourceteamnameen = models.CharField(db_column='SourceTeamNameEn', max_length=200, blank=True, null=True)  # Field name made lowercase.
    sourceteamnamezh = models.CharField(db_column='SourceTeamNameZh', max_length=200, blank=True, null=True)  # Field name made lowercase.
    teamnameen = models.CharField(db_column='TeamNameEn', max_length=200, blank=True, null=True)  # Field name made lowercase.
    teamnamezh = models.CharField(db_column='TeamNameZh', max_length=200, blank=True, null=True)  # Field name made lowercase.
    teamid = models.IntegerField(db_column='TeamID', blank=True, null=True)  # Field name made lowercase.
    mappingkey = models.CharField(db_column='MappingKey', max_length=500, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'TB_TeamMapping'
        
        

class TbManualsettlemsg(models.Model):
    id = models.AutoField(db_column='ID',primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID', verbose_name='比赛ID')  # Field name made lowercase.
    settlemsg = models.TextField(db_column='SettleMsg', verbose_name='结算内容')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', verbose_name='状态',default=0,choices=SETTLEMSG_STATUS)  # Field 
    
    class Meta:
        managed = False
        db_table = 'TB_ManualSettleMsg'