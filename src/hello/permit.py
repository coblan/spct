from helpers.director.base_data import permit_dc
from django.utils.translation import ugettext as _

permit = [
    {'name': 'xxx', 'label': '市场',
     'children': [
         {'name': 'xbb', 'label': '广告', 'value': 'TbBanner',}, 
         {'name': 'xbb', 'label': 'APP版本', 'value': 'TbAppversion',}, 
         {'name': 'xbb', 'label': '公告', 'value': 'TbNotice',}, 
         {'name': 'xbb', 'label': '帮助管理', 'value': 'TbQa',}, 
         {'name': 'xbb', 'label': '活动管理', 'value': 'TbActivity',}, 
         {'name': 'xbb', 'label': 'APP资源管理', 'value': 'TbAppresource',}, 
         ]
     }, 
    {'name': 'xxx', 'label': '会员管理',
     'children': [
         {'label': '会员管理', 'value': 'TbAccount',}, 
         {'label': '登录日志', 'value': 'TbLoginlog',}, 
         {'label': '账目记录', 'value': 'TbBalancelog', }, 
         {'label': 'TbTicketmaster', 'value': 'TbTicketmaster',}
         ],
     }, 
    {'label': '金流管理',
     'children': [
         #{'label': '账目记录', 'value': 'TbBalancelog', }, 
         {'label': '金流渠道', 'value': 'TbChannel',}, 
         {'label': '金流日志', 'value': 'TbChargeflow',}
         ],
    }, 
    {'label': '比赛管理', 'value': 'TbMatches',}, 
    {'label': _('RC Control'),
     'children': [
         {'label': _('TbBlackuserlist'), 'value': 'TbBlackuserlist',}, 
         {'label': _('TbBlackuserlistLog'), 'value': 'TbBlackuserlistLog',}, 
         {'label': _('Blackiplist'), 'value': 'Blackiplist',}, 
         {'label': _('Blackiprangelist'), 'value': 'Blackiprangelist',}, 
         {'label': _('Whiteiplist'), 'value': 'Whiteiplist',}, 
         {'label': _('Whiteuserlist'), 'value': 'Whiteuserlist',}
         ],}, 
    {'label': _('User'),
     'children': [
        {'label': '查看用户', 'value': 'User.read',}, 
         {'label': '编辑用户', 'value': 'User.write',}, 
         {'label': _('Group'), 'value': 'Group',}
         ],
     }
    
    
]

permit_dc['__root__'] = permit