pop_edit_ops=[
             {'name':'save','label':'确定','editor':'com-op-btn','action':'rt=scope.ps.vc.isValid()?scope.ps.vc.$emit("finish",scope.ps.vc.row):""'}
        ]


def head_109():
    def _fun(num):
        ls =[
        {'name':'home_14%s_1'%num,'label':'主队第%s局得分'%num,'editor':'com-field-number','required':True,'fv_rule':'主队上半场:integer(+0)'},
        {'name':'away_14%s_1'%num,'label':'客队第%s局得分'%num,'editor':'com-field-number','required':True,'fv_rule':'客队上半场:integer(+0)'},
        {'name':'has_overtime_14%s'%num,'label':'是否有加时','editor':'com-field-bool'},
        {'name':'home_14%s40_1'%num,'label':'主队第%s局加时得分'%num,'editor':'com-field-number','required':True,'fv_rule':'加时比分:integer(+0)','show':'scope.row.has_overtime_14%s'%num},
        {'name':'away_14%s40_1'%num,'label':'客队第%s局加时得分'%num,'editor':'com-field-number','required':True,'fv_rule':'加时比分:integer(+0)','show':'scope.row.has_overtime_14%s'%num},
        ]  
        return ls
    out_ls =[]
    for i in range(1,8):
        out_ls += _fun(i)
    return out_ls

def fields_group_109():
    def _fun(num):
        ls =[
            {'name':'huji','show':'scope.row.round_count>=%s'%num,'label':'第%s局'%num,'heads':['home_14%s_1'%num,'away_14%s_1'%num,'home_14%s40_1'%num,'away_14%s40_1'%num,'has_overtime_14%s'%num]},
        ]
        return ls
    
    out_ls =[]
    for i in range(1,8):
        out_ls += _fun(i)
    return out_ls
        

def head_lol_score():
    return { # 英雄联盟
            'heads': [
                {'name':'round_count','label':'局总数','editor':'com-field-select','required':True,'options':[
                    {'value':1,'label':'一局'},
                    {'value':2,'label':'两局'},
                    {'value':3,'label':'三局'},
                    {'value':4,'label':'四局'},
                    {'value':5,'label':'五局'},
                    ]},
                {'name':'home_141_1','label':'第一局胜者','editor':'com-field-select','required':True,'show':'scope.row.round_count >= 1','options':[
                    {'value':1,'label':'主队'},
                    {'value':0,'label':'客队'}
                    ]},
                {'name':'home_142_1','label':'第二局胜者','editor':'com-field-select','required':True,'show':'scope.row.round_count >= 2','options':[
                    {'value':1,'label':'主队'},
                    {'value':0,'label':'客队'}
                    ]},
                {'name':'home_143_1','label':'第三局胜者','editor':'com-field-select','required':True,'show':'scope.row.round_count >= 3','options':[
                    {'value':1,'label':'主队'},
                    {'value':0,'label':'客队'}
                    ]},
                {'name':'home_144_1','label':'第四局胜者','editor':'com-field-select','required':True,'show':'scope.row.round_count >= 4','options':[
                    {'value':1,'label':'主队'},
                    {'value':0,'label':'客队'}
                    ]},
                {'name':'home_145_1','label':'第五局胜者','editor':'com-field-select','required':True,'show':'scope.row.round_count >= 5','options':[
                    {'value':1,'label':'主队'},
                    {'value':0,'label':'客队'}
                    ]},
               
                ],
            'editor':'com-form-one', #'com-outcome-score',

            'ops_loc':'down',
            'ops':pop_edit_ops,
            'init_express':'ex.director_call("get_match_outcome_info",{matchid:scope.vc.ctx.par_row.matchid}).then(res=>ex.vueAssign(scope.row,res))'
            }
    

def head_all_333(label1,label2,round_number):
    dc = {
            'heads':[
                 {'name':'content','label':label1+label2,'editor':'com-field-table-list','fv_rule':'group_unique(Specifiers_1, Specifiers)','fv_msg':'%s+%s 不能重复'%(label1,label2),
                  'table_heads':[
                    {'name':'Specifiers_1','label':label1,'editor':'com-table-pop-fields-local'},
                    {'name':'Specifiers','label':label2,'editor':'com-table-span', 'width': 80, },
                    {'name':'OutcomeId','label':'主/客队','editor':'com-table-mapper', 'width': 80,
                      'options':[
                         {'value':4,'label':'主队'},
                         {'value':5,'label':'客队'}
                         ], 
                     }, 
                    
                      ],
                 'fields_heads':[
                     {'name':'Specifiers_1','label':label1,'editor':'com-field-number','required':True,'fv_rule':'integer(+);range(1~%s)'%round_number},
                     {'name':'Specifiers','label':label2,'editor':'com-field-number','required':True,'fv_rule':'integer(+)'}, 
                    {'name':'OutcomeId','label':'主队','editor':'com-field-select', 'required':True,
                     'options':[
                         {'value':4,'label':'主队'},
                         {'value':5,'label':'客队'}
                         ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         }
    return dc


outcome_header = {
    'panel_map':{
        -19:{
            'heads':[
                 {'name':'set_count','label':'总盘数','editor':'com-field-select','options':[
                    {'value':i,'label':'%s盘'%i}
                    for i in range(1,51)
                    ]},
            ]+[ {'name':'home_%s_1'%i,'label':'主队第%s盘得分'%i,'editor':'com-field-number','required':True,'show':'scope.row.set_count >= %s'%i,'fv_rule':'integer(+0)'}
                    for i in range(1,51)]
            +[{'name':'away_%s_1'%i,'label':'客队第%s盘得分'%i,'editor':'com-field-number','required':True,'show':'scope.row.set_count >= %s'%i,'fv_rule':'integer(+0)'}
               for i in range(1,51)],
            'table_grid':[['set_count'],
                          ]+[['home_%s_1'%i,'away_%s_1'%i]
                             for i in range(1,51)
                              ],
            'fields_group':[
                {'name':'huji','label':'基本控制','heads':['set_count']},
                {'name':'huji','label':'比分','heads':['home_%s_1'%i for i in range(1,51)]+ ['away_%s_1'%i for i in range(1,51)]},
            ],
            
            'editor':'com-form-one', 
            'ops_loc':'down',
            'ops':pop_edit_ops,
            'init_express':'ex.director_call("get_match_outcome_info",{matchid:scope.vc.ctx.par_row.matchid}).then(res=>ex.vueAssign(scope.row,res))'

        },
        -5:{ # 网球分数
            'heads':[
                {'name':'set_count','label':'总盘数','editor':'com-field-select','options':[
                    {'value':1,'label':'一盘'},
                    {'value':2,'label':'二盘'},
                    {'value':3,'label':'三盘'},
                    {'value':4,'label':'四盘'},
                    {'value':5,'label':'五盘'}
                    ]},
                {'name':'home_8_1','label':'主队第一盘得分','editor':'com-field-number','required':True,'show':'scope.row.set_count >= 1','fv_rule':'integer(+0)'},
                {'name':'away_8_1','label':'客队第一盘得分','editor':'com-field-number','required':True,'show':'scope.row.set_count >= 1','fv_rule':'integer(+0)'},
                {'name':'home_9_1','label':'主队第二盘得分','editor':'com-field-number','required':True,'show':'scope.row.set_count >= 2','fv_rule':'integer(+0)'},
                {'name':'away_9_1','label':'客队第二盘得分','editor':'com-field-number','required':True,'show':'scope.row.set_count >= 2','fv_rule':'integer(+0)'},
                {'name':'home_10_1','label':'主队第三盘得分','editor':'com-field-number','required':True,'show':'scope.row.set_count >= 3','fv_rule':'integer(+0)'},
                {'name':'away_10_1','label':'客队第三盘得分','editor':'com-field-number','required':True,'show':'scope.row.set_count >= 3','fv_rule':'integer(+0)'},
                {'name':'home_11_1','label':'主队第四盘得分','editor':'com-field-number','required':True,'show':'scope.row.set_count >= 4','fv_rule':'integer(+0)'},
                {'name':'away_11_1','label':'客队第四盘得分','editor':'com-field-number','required':True,'show':'scope.row.set_count >= 4 ','fv_rule':'integer(+0)'},
                {'name':'home_12_1','label':'主队第五盘得分','editor':'com-field-number','required':True,'show':'scope.row.set_count >= 5','fv_rule':'integer(+0)'},
                {'name':'away_12_1','label':'客队第五盘得分','editor':'com-field-number','required':True,'show':'scope.row.set_count >= 5','fv_rule':'integer(+0)'},
                    
            ],
            'editor':'com-form-one', 
            
            'table_grid':[['set_count'],
                          ['home_8_1','away_8_1'],
                          ['home_9_1','away_9_1'],
                          ['home_10_1','away_10_1'],
                          ['home_11_1','away_11_1'],
                          ['home_12_1','away_12_1'],
                          ],
            'fields_group':[
                {'name':'huji','label':'基本控制','heads':['set_count']},
                {'name':'huji','label':'比分','heads':['home_8_1','away_8_1','home_9_1','away_9_1','home_10_1','away_10_1','home_11_1','away_11_1','home_12_1','away_12_1']},
                #{'name':'huji','label':'角球','heads':['home_6_5','away_6_5','home_7_5','away_7_5','home_40_5','away_40_5']},
            ],
            
            'ops_loc':'down',
            'ops':pop_edit_ops,
            'init_express':'ex.director_call("get_match_outcome_info",{matchid:scope.vc.ctx.par_row.matchid}).then(res=>ex.vueAssign(scope.row,res))'
        },
        -3:{
            'heads':[
                {'name':'home_6_1','label':'主队上半场得分','editor':'com-field-number','required':True,'fv_rule':'主队上半场:integer(+0)'},
                {'name':'away_6_1','label':'客队上半场得分','editor':'com-field-number','required':True,'fv_rule':'客队上半场:integer(+0)'},
                {'name':'home_100_1','label':'主队全场得分','editor':'com-field-number','required':True,'show':'scope.row.has_100_1','fv_rule':'integer(+0);match(gte, home_6_1)'},
                {'name':'away_100_1','label':'客队全场得分','editor':'com-field-number','required':True,'show':'scope.row.has_100_1','fv_rule':'integer(+0);match(gte, away_6_1)'},
                {'name':'home_40_1','label':'主队加时赛得分','editor':'com-field-number','required':True,'show':'scope.row.has_overtime','fv_rule':'integer(+0)'},
                {'name':'away_40_1','label':'客队加时赛得分','editor':'com-field-number','required':True,'show':'scope.row.has_overtime','fv_rule':'integer(+0)'},
                 
                {'name':'has_6_1','label':'上半场','editor':'com-field-bool','readonly':True},
                {'name':'has_100_1','label':'全场','editor':'com-field-bool'},
                {'name':'has_overtime','label':'加时赛','editor':'com-field-bool','fv_rule':'depend_check(has_finish)','fv_msg':'必须勾选比赛结束!'},
                {'name':'has_finish','label':'比赛结束','editor':'com-field-bool','fv_rule':'depend_check(has_100_1)','fv_msg':'必须勾选全场!'}
    
            ],
            'editor':'com-form-one', 
            
            'table_grid':[['has_finish'],
                        ['has_6_1','has_100_1','has_overtime'],
                          ['home_6_1','away_6_1'],
                          ['home_100_1','away_100_1'],
                          ['home_40_1','away_40_1'],
                          ],
            'ops_loc':'down',
            'ops':pop_edit_ops,
            'init_express':'if(ex.isEmpty(scope.row)){ ex.director_call("get_match_outcome_info",{matchid:scope.vc.ctx.par_row.matchid}).then(res=>ex.vueAssign(scope.row,res)) }'
        },
        -2:{ # 篮球分数
            'heads':[
                {'name':'home_13_1','label':'主队第一节得分','editor':'com-field-number','required':True,'fv_rule':'integer(+0)','show':'scope.row.has_13_1',},
                {'name':'away_13_1','label':'客队第一节得分','editor':'com-field-number','required':True,'fv_rule':'integer(+0)','show':'scope.row.has_13_1',},
                {'name':'home_14_1','label':'主队第二节得分','editor':'com-field-number','required':True,'fv_rule':'integer(+0)','show':'scope.row.has_14_1',},
                {'name':'away_14_1','label':'客队第二节得分','editor':'com-field-number','required':True,'fv_rule':'integer(+0)','show':'scope.row.has_14_1'},
                {'name':'home_15_1','label':'主队第三节得分','editor':'com-field-number','required':True,'fv_rule':'integer(+0)','show':'scope.row.has_15_1'},
                {'name':'away_15_1','label':'客队第三节得分','editor':'com-field-number','required':True,'fv_rule':'integer(+0)','show':'scope.row.has_15_1'},
                {'name':'home_16_1','label':'主队第四节得分','editor':'com-field-number','required':True,'fv_rule':'integer(+0)','show':'scope.row.has_16_1'},
                {'name':'away_16_1','label':'客队第四节得分','editor':'com-field-number','required':True,'fv_rule':'integer(+0)','show':'scope.row.has_16_1'},
                {'name':'home_40_1','label':'主队加时赛得分','editor':'com-field-number','required':True,'show':'scope.row.has_40_1','fv_rule':'integer(+0)'},
                {'name':'away_40_1','label':'客队加时赛得分','editor':'com-field-number','required':True,'show':'scope.row.has_40_1','fv_rule':'integer(+0)'},
                
                {'name':'has_13_1','label':'第一节','editor':'com-field-bool',},
                {'name':'has_14_1','label':'第二节','editor':'com-field-bool','fv_rule':'depend_check(has_13_1)','fv_msg':'必须勾选第一节!'},
                {'name':'has_15_1','label':'第三节','editor':'com-field-bool','fv_rule':'depend_check(has_14_1)','fv_msg':'必须勾选第二节!'},
                {'name':'has_16_1','label':'第四节','editor':'com-field-bool','fv_rule':'depend_check(has_15_1)','fv_msg':'必须勾选第三节!'},
                {'name':'has_40_1','label':'加时赛','editor':'com-field-bool','fv_rule':'depend_check(has_16_1);depend_check(has_100_1)','fv_msg':'必须勾选第四节和比赛结束!'},
                {'name':'has_100_1','label':'比赛结束','editor':'com-field-bool','fv_rule':'depend_check(has_16_1)','fv_msg':'必须勾选第四节!'}
               
                
            ],
            'editor':'com-form-one', 
            'table_grid':[
                ['has_100_1'],
                ['has_13_1','has_14_1','has_15_1','has_16_1','has_40_1'],
                          ['home_13_1','away_13_1'],
                          ['home_14_1','away_14_1'],
                          ['home_15_1','away_15_1'],
                          ['home_16_1','away_16_1'],
                          ['home_40_1','away_40_1'],
                          ],
            'fields_group':[
                {'name':'huji','label':'基本控制','heads':['has_100_1','has_13_1','has_14_1','has_15_1','has_16_1','has_40_1']},
                {'name':'huji','label':'比分','heads':['home_13_1','away_13_1','home_14_1','away_14_1','home_15_1','away_15_1','home_16_1','away_16_1','home_40_1','away_40_1']},
    
            ],
            'ops_loc':'down',
            'ops':pop_edit_ops,
            'init_express':'if(ex.isEmpty(scope.row)){ex.director_call("get_match_outcome_info",{matchid:scope.vc.ctx.par_row.matchid}).then(res=>{ex.vueAssign(scope.row,res);}) }'
           },
        -1:{ # 足球分数
            'heads': [ 
                {'name':'home_6_1','label':'主队上半场得分','editor':'com-field-number','required':True,'fv_rule':'主队上半场:integer(+0)'},
                {'name':'away_6_1','label':'客队上半场得分','editor':'com-field-number','required':True,'fv_rule':'客队上半场:integer(+0)'},
                {'name':'home_100_1','label':'主队全场得分','editor':'com-field-number','required':True,'show':'scope.row.has_half2','fv_rule':'integer(+0);match(gte, home_6_1)'},
                {'name':'away_100_1','label':'客队全场得分','editor':'com-field-number','required':True,'show':'scope.row.has_half2','fv_rule':'integer(+0);match(gte, away_6_1)'},
                {'name':'home_40_1','label':'主队加时赛得分','editor':'com-field-number','required':True,'show':'scope.row.has_overtime','fv_rule':'integer(+0)'},
                {'name':'away_40_1','label':'客队加时赛得分','editor':'com-field-number','required':True,'show':'scope.row.has_overtime','fv_rule':'integer(+0)'},
                {'name':'home_50_1','label':'主队点球大战得分','editor':'com-field-number','required':True,'show':'scope.row.has_penalty','fv_rule':'integer(+0)'},
                {'name':'away_50_1','label':'客队点球大战得分','editor':'com-field-number','required':True,'show':'scope.row.has_penalty','fv_rule':'integer(+0)'},
                
                {'name':'home_6_5','label':'主队上半场角球','editor':'com-field-number','required':True,'fv_rule':'主队上半场:integer(+0)',},
                {'name':'away_6_5','label':'客队上半场角球','editor':'com-field-number','required':True,'fv_rule':'客队上半场:integer(+0)',},
                {'name':'home_100_5','label':'主队全场角球','editor':'com-field-number','required':True,'show':'scope.row.has_half2','fv_rule':'integer(+0);match(gte, home_6_5)'},
                {'name':'away_100_5','label':'客队全场角球','editor':'com-field-number','required':True,'show':'scope.row.has_half2','fv_rule':'integer(+0);match(gte, away_6_5)'},
                {'name':'home_40_5','label':'主队加时赛角球','editor':'com-field-number','required':True,'show':'scope.row.has_overtime','fv_rule':'integer(+0)'},
                {'name':'away_40_5','label':'客队加时赛角球','editor':'com-field-number','required':True,'show':'scope.row.has_overtime','fv_rule':'integer(+0)'},
                
                {'name':'has_half1','label':'上半场','editor':'com-field-bool','readonly':True},
                {'name':'has_half2','label':'全场','editor':'com-field-bool'},
                {'name':'has_overtime','label':'加时赛','editor':'com-field-bool','fv_rule':'depend_check(has_half2);depend_check(has_100_1)','fv_msg':'必须选择全场和比赛结束!'},
                {'name':'has_penalty','label':'点球大战','editor':'com-field-bool','fv_rule':'depend_check(has_half2);depend_check(has_100_1)','fv_msg':'必须选择全场和比赛结束!'},
                {'name':'has_100_1','label':'比赛结束','editor':'com-field-bool','fv_rule':'depend_check(has_half2);','fv_msg':'必须勾选全场!'}
                ],
            'editor':'com-form-one', #'com-outcome-score',
     
            'table_grid':[
                ['has_100_1'],
                ['has_half1','has_half2','has_overtime','has_penalty'],
                          ['home_6_1','away_6_1'],
                          ['home_100_1','away_100_1'],
                          ['home_40_1','away_40_1'],
                          ['home_50_1','away_50_1'],
                          ['home_6_5','away_6_5'],
                          ['home_100_5','away_100_5'],
                          ['home_40_5','away_40_5'],
                          ],
            'fields_group':[
                    {'name':'huji','label':'基本控制','heads':['has_100_1','has_half1','has_half2','has_overtime','has_penalty']},
                    {'name':'huji','label':'比分','heads':['home_6_1','away_6_1','home_100_1','away_100_1','home_40_1','away_40_1','home_50_1','away_50_1']},
                    {'name':'huji','label':'角球','heads':['home_6_5','away_6_5','home_100_5','away_100_5','home_40_5','away_40_5']},
                ],

            'ops_loc':'down',
            'ops':pop_edit_ops,
            'init_express':'if(!scope.row.has_half1){ex.director_call("get_match_outcome_info",{matchid:scope.vc.ctx.par_row.matchid}).then(res=>ex.vueAssign(scope.row,res))}'
            },
            -109:{ # 反恐精英 分数
            'heads': [ 
                {'name':'round_count','label':'局总数','editor':'com-field-select','required':True,'options':[
                    {'value':1,'label':'一局'},
                    {'value':2,'label':'两局'},
                    {'value':3,'label':'三局'},
                    {'value':4,'label':'四局'},
                    {'value':5,'label':'五局'},
                    {'value':6,'label':'六局'},
                    {'value':7,'label':'七局'},
                    ]},
                ] + head_109(),
            'editor':'com-form-one', #'com-outcome-score',
            
            'table_grid':[['round_count'],
                          ['has_overtime_14%s'%num for num in range(1,8)],
                          ['home_14%s_1'%num for num in range(1,8)]+['away_14%s_1'%num for num in range(1,8)]   ,
                          ['home_14%s40_1'%num for num in range(1,8)] + ['away_14%s40_1'%num for num in range(1,8)],
                          ],
            'fields_group':[
                {'name':'basice','label':'基本控制','heads':['round_count']},
            ] + fields_group_109(),
            
            'ops_loc':'down',
            'ops':pop_edit_ops,
            'init_express':'ex.director_call("get_match_outcome_info",{matchid:scope.vc.ctx.par_row.matchid}).then(res=>ex.vueAssign(scope.row,res))'
            },
         -110:head_lol_score(),
         -111:head_lol_score(),
         
         291:{
            'heads':[
                 {'name':'content','label':'谁先得X分','editor':'com-field-table-list','fv_rule':'key_unique(Specifiers)','fv_msg':'分数不能重复',
                  'table_heads':[
                      {'name':'Specifiers','label':'分数','editor':'com-table-pop-fields-local', 'width': 200,}, 
                      {'name':'OutcomeId','label':'主队/客队','editor':'com-table-mapper', 'width': 200,
                       'options':[
                         {'value':4,'label':'主队'},
                         {'value':5,'label':'客队'},
                         ]}, 
                      ],
                 'fields_heads':[
                     {'name':'Specifiers','label':'分数','editor':'com-field-number','required':True,'fv_rule':'integer(+0)' }, 
                     {'name':'OutcomeId','label':'主队/客队','editor':'com-field-select', 'required':True,'options':[
                         {'value':4,'label':'主队'},
                         {'value':5,'label':'客队'},
                         ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         174:{
            'heads':[
                 {'name':'content','label':'上半场谁发X角球','editor':'com-field-table-list','fv_rule':'key_unique(Specifiers)','fv_msg':'角球个数不能重复',
                  'table_heads':[
                      {'name':'Specifiers','label':'角球个数','editor':'com-table-pop-fields-local', 'width': 200,}, 
                      {'name':'OutcomeId','label':'主队/客队','editor':'com-table-mapper', 'width': 200,
                       'options':[
                         {'value':6,'label':'主队'},
                         {'value':7,'label':'都不'},
                         {'value':8,'label':'客队'},
                         ]}, 
                      #{'name':'order','label':'','editor':'com-table-change-order'}
                      ],
                 'fields_heads':[
                     {'name':'Specifiers','label':'角球个数','editor':'com-field-number', 'required':True}, 
                     {'name':'OutcomeId','label':'主队/客队','editor':'com-field-select', 'required':True,'options':[
                         {'value':6,'label':'主队'},
                         {'value':7,'label':'都不'},
                         {'value':8,'label':'客队'},
                         ]}, 
                 ]}
            ],
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         163:{
            'heads':[
                 {'name':'content','label':'常规时间第X角球','editor':'com-field-table-list','fv_rule':'key_unique(Specifiers)','fv_msg':'角球个数不能重复',
                  'table_heads':[
                      {'name':'Specifiers','label':'角球个数','editor':'com-table-pop-fields-local', 'width': 200,}, 
                      {'name':'OutcomeId','label':'主队/客队','editor':'com-table-mapper', 'width': 200,
                       'options':[
                         {'value':6,'label':'主队'},
                         {'value':7,'label':'都不'},
                         {'value':8,'label':'客队'},
                         ]}, 
                      ],
                 'fields_heads':[
                     {'name':'Specifiers','label':'角球个数','editor':'com-field-number', 'required':True}, 
                     {'name':'OutcomeId','label':'主队/客队','editor':'com-field-select', 'required':True,'options':[
                         {'value':6,'label':'主队'},
                         {'value':7,'label':'都不'},
                         {'value':8,'label':'客队'},
                         ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
             
         },
         8:{
           'heads':[
                 {'name':'content','label':'常规时间谁先进第X球','editor':'com-field-table-list','fv_rule':'key_unique(Specifiers)','fv_msg':'个数不能重复',
                  'table_heads':[
                      {'name':'Specifiers','label':'个数','editor':'com-table-pop-fields-local', 'width': 200,}, 
                      {'name':'OutcomeId','label':'主队/客队','editor':'com-table-mapper', 'width': 200,
                       'options':[
                         {'value':6,'label':'主队'},
                         {'value':7,'label':'都不'},
                         {'value':8,'label':'客队'},
                         ]}, 
                      ],
                 'fields_heads':[
                     {'name':'Specifiers','label':'个数','editor':'com-field-number', 'required':True}, 
                     {'name':'OutcomeId','label':'主队/客队','editor':'com-field-select', 'required':True,'options':[
                         {'value':6,'label':'主队'},
                         {'value':7,'label':'都不'},
                         {'value':8,'label':'客队'},
                         ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         9:{
           'heads':[
                 {'name':'OutcomeId','label':'谁进最后一个球','editor':'com-field-select',  
                  'options':[
                         {'value':6,'label':'主队'},
                         {'value':7,'label':'都不'},
                         {'value':8,'label':'客队'},
                         ]
                  }
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         100:{
            'heads':[
                 {'name':'content','label':'15分钟','editor':'com-field-table-list','fv_rule':'key_unique(OutcomeId)','fv_msg':'时间段不能重复',
                  'table_heads':[
                      {'name':'Specifiers','label':'个数','editor':'com-table-pop-fields-local', 'width': 200,}, 
                      {'name':'OutcomeId','label':'时间段','editor':'com-table-mapper', 'width': 200,
                       'options':[
                           {'value':584,'label':'1-15'},
                           {'value':586,'label':'16-30'},
                           {'value':588,'label':'31-45'},
                           {'value':590,'label':'46-60'},
                           {'value':592,'label':'61-75'},
                           {'value':594,'label':'76-90'},
                           {'value':596,'label':'默认'},
                         ]}, 
                      ],
                 'fields_heads':[
                     {'name':'Specifiers','label':'个数','editor':'com-field-number', 'required':True}, 
                     {'name':'OutcomeId','label':'时间段','editor':'com-field-select', 'required':True,'options':[
                         {'value':584,'label':'1-15'},
                         {'value':586,'label':'16-30'},
                         {'value':588,'label':'31-45'},
                         {'value':590,'label':'46-60'},
                         {'value':592,'label':'61-75'},
                         {'value':594,'label':'76-90'},
                         {'value':596,'label':'默认'},
                         ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         101:{
            'heads':[
                 {'name':'content','label':'10分钟','editor':'com-field-table-list','fv_rule':'key_unique(Specifiers)','fv_msg':'个数不能重复',
                  'table_heads':[
                      {'name':'Specifiers','label':'个数','editor':'com-table-pop-fields-local', 'width': 200,}, 
                      {'name':'OutcomeId','label':'时间段','editor':'com-table-mapper', 'width': 200,
                       'options':[
                           {'value':598,'label':"1-10"},
                           {'value':600,'label':"11-20"},
                           {'value':602,'label':"21-30"},
                           {'value':604,'label':"31-40"},
                           {'value':606,'label':"41-50"},
                           {'value':608,'label':"51-60"},
                           {'value':610,'label':"61-70"},
                           {'value':612,'label':"71-80"},
                           {'value':614,'label':"81-90"},
                           {'value':616,'label':"默认"},
                         ], }
                      ],
                 'fields_heads':[
                     {'name':'Specifiers','label':'个数','editor':'com-field-number','fv_rule':'integer(+0)', 'required':True}, 
                     {'name':'OutcomeId','label':'时间段','editor':'com-field-select', 'required':True,'options':[
                           {'value':598,'label':"1-10"},
                           {'value':600,'label':"11-20"},
                           {'value':602,'label':"21-30"},
                           {'value':604,'label':"31-40"},
                           {'value':606,'label':"41-50"},
                           {'value':608,'label':"51-60"},
                           {'value':610,'label':"61-70"},
                           {'value':612,'label':"71-80"},
                           {'value':614,'label':"81-90"},
                           {'value':616,'label':"默认"},
                         ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         102:{
            'heads':[
                 {'name':'content','label':'15分钟1X2','editor':'com-field-table-list','fv_rule':'key_unique(Specifiers)','fv_msg':'时间段不能重复',
                  'table_heads':[
                    
                      {'name':'Specifiers','label':'时间段','editor':'com-table-pop-fields-local', 'inn_editor':'com-table-mapper', 'width': 200,
                       'options':[
                           {'value':'from=1|to=15' ,'label':'1-15' },
                           {'value':'from=16|to=30','label':'16-30'},
                           {'value':'from=31|to=45','label':'31-45'},
                           {'value':'from=46|to=60','label':'46-60'},
                           {'value':'from=61|to=75','label':'61-75'},
                           {'value':'from=76|to=90','label':'76-90'},
                         ], },
                        {'name':'OutcomeId','label':'胜平负','editor':'com-table-mapper', 'width': 200,
                         'options':[
                              {'value':1 ,'label':'主赢' },
                              {'value':2,'label':'平局'},
                              {'value':3,'label':'客赢'},
                             ]}, 
                      ],
                 'fields_heads':[
                     {'name':'Specifiers','label':'时间段','editor':'com-field-select', 'required':True,'options':[
                            {'value':'from=1|to=15' ,'label':'1-15' },
                           {'value':'from=16|to=30','label':'16-30'},
                           {'value':'from=31|to=45','label':'31-45'},
                           {'value':'from=46|to=60','label':'46-60'},
                           {'value':'from=61|to=75','label':'61-75'},
                           {'value':'from=76|to=90','label':'76-90'},
                         ]}, 
                    {'name':'OutcomeId','label':'胜平负','editor':'com-field-select', 'required':True,
                      'options':[
                              {'value':1 ,'label':'主赢' },
                              {'value':2,'label':'平局'},
                              {'value':3,'label':'客赢'},
                             ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         103:{
            'heads':[
                 {'name':'content','label':'15分钟进球','editor':'com-field-table-list','fv_rule':'group_unique(Specifiers_1, Specifiers)','fv_msg':'第几粒球+时间段 不能重复',
                  'table_heads':[
                    {'name':'Specifiers_1','label':'第几粒球','editor':'com-table-pop-fields-local'},
                    {'name':'Specifiers','label':'时间段','editor':'com-table-mapper', 'width': 200,
                       'options':[
                           {'value':'|from=1|to=15','label':'1-15'},
                           {'value':'|from=16|to=30','label':'16-30'},
                           {'value':'|from=31|to=45','label':'31-45'},
                           {'value':'|from=46|to=60','label':'46-60'},
                           {'value':'|from=61|to=75','label':'61-75'},
                           {'value':'|from=76|to=90','label':'76-90'},
                         ], },
                    {'name':'OutcomeId','label':'胜平负','editor':'com-table-mapper', 'width': 200,
                     'options':[
                          {'value':6,'label':'主赢' },
                          {'value':7,'label':'平局'},
                          {'value':8,'label':'客赢'},
                         ]}, 
                      ],
                 'fields_heads':[
                     {'name':'Specifiers_1','label':'第几粒球','editor':'com-field-number','fv_rule':'integer(+)','required':True},
                     {'name':'Specifiers','label':'时间段','editor':'com-field-select', 'required':True,'options':[
                           {'value':'|from=1|to=15','label':'1-15'},
                           {'value':'|from=16|to=30','label':'16-30'},
                           {'value':'|from=31|to=45','label':'31-45'},
                           {'value':'|from=46|to=60','label':'46-60'},
                           {'value':'|from=61|to=75','label':'61-75'},
                           {'value':'|from=76|to=90','label':'76-90'},
                         ]}, 
                    {'name':'OutcomeId','label':'胜平负','editor':'com-field-select', 'required':True,
                      'options':[
                               {'value':6,'label':'主赢' },
                               {'value':7,'label':'平局'},
                               {'value':8,'label':'客赢'},
                             ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         104:{
            'heads':[
                 {'name':'content','label':'15分钟大小','editor':'com-field-table-list','fv_rule':'group_unique(Specifiers_1, Specifiers)','fv_msg':'盘口+时间段 不能重复',
                  'table_heads':[
                    {'name':'Specifiers_1','label':'盘口','editor':'com-table-pop-fields-local'},
                    {'name':'Specifiers','label':'时间段','editor':'com-table-mapper', 'width': 80,
                       'options':[
                           {'value':'|from=1|to=15','label':'1-15'},
                           {'value':'|from=16|to=30','label':'16-30'},
                           {'value':'|from=31|to=45','label':'31-45'},
                           {'value':'|from=46|to=60','label':'46-60'},
                           {'value':'|from=61|to=75','label':'61-75'},
                           {'value':'|from=76|to=90','label':'76-90'},
                         ], },
                    {'name':'OutcomeId','label':'主队','editor':'com-table-span', 'width': 80,}, 
                    {'name':'OutcomeId_1','label':'客队','editor':'com-table-span', 'width': 80,}, 
                    
                      ],
                 'fields_heads':[
                     {'name':'Specifiers_1','label':'盘口','editor':'com-field-number','required':True},
                     {'name':'Specifiers','label':'时间段','editor':'com-field-select','required':True, 'options':[
                           {'value':'|from=1|to=15','label':'1-15'},
                           {'value':'|from=16|to=30','label':'16-30'},
                           {'value':'|from=31|to=45','label':'31-45'},
                           {'value':'|from=46|to=60','label':'46-60'},
                           {'value':'|from=61|to=75','label':'61-75'},
                           {'value':'|from=76|to=90','label':'76-90'},
                         ]}, 
                    {'name':'OutcomeId','label':'主队','editor':'com-field-number', 'required':True}, 
                    {'name':'OutcomeId_1','label':'客队','editor':'com-field-number', 'required':True}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         105:{
            'heads':[
                 {'name':'content','label':'10分钟1X2','editor':'com-field-table-list','fv_rule':'key_unique(Specifiers)','fv_msg':'时间段不能重复',
                  'table_heads':[
                    
                      {'name':'Specifiers','label':'时间段','editor':'com-table-pop-fields-local','inn_editor':'com-table-mapper', 'width': 200,
                       'options':[
                           {'value':"from=1|to=10",'label':"1-10"},
                           {'value':"from=11|to=20",'label':"11-20"},
                           {'value':"from=21|to=30",'label':"21-30"},
                           {'value':"from=31|to=40",'label':"31-40"},
                           {'value':"from=41|to=50",'label':"41-50"},
                           {'value':"from=51|to=60",'label':"51-60"},
                           {'value':"from=61|to=70",'label':"61-70"},
                           {'value':"from=71|to=80",'label':"71-80"},
                           {'value':"from=81|to=90",'label':"81-90"},
                         ], },
                        {'name':'OutcomeId','label':'胜平负','editor':'com-table-mapper', 'width': 200,
                         'options':[
                              {'value':1 ,'label':'主赢' },
                              {'value':2,'label':'平局'},
                              {'value':3,'label':'客赢'},
                             ]}, 
                      ],
                 'fields_heads':[
                     {'name':'Specifiers','label':'时间段','editor':'com-field-select', 'required':True,'options':[
                         {'value':"from=1|to=10",'label':"1-10"},
                           {'value':"from=11|to=20",'label':"11-20"},
                           {'value':"from=21|to=30",'label':"21-30"},
                           {'value':"from=31|to=40",'label':"31-40"},
                           {'value':"from=41|to=50",'label':"41-50"},
                           {'value':"from=51|to=60",'label':"51-60"},
                           {'value':"from=61|to=70",'label':"61-70"},
                           {'value':"from=71|to=80",'label':"71-80"},
                           {'value':"from=81|to=90",'label':"81-90"},
                         ]}, 
                    {'name':'OutcomeId','label':'胜平负','editor':'com-field-select', 'required':True,
                      'options':[
                              {'value':1 ,'label':'主赢' },
                              {'value':2,'label':'平局'},
                              {'value':3,'label':'客赢'},
                             ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         106:{
            'heads':[
                 {'name':'content','label':'10分钟进球','editor':'com-field-table-list','fv_rule':'group_unique(Specifiers_1, Specifiers)','fv_msg':'第几粒球+时间段不能重复',
                  'table_heads':[
                    {'name':'Specifiers_1','label':'第几粒球','editor':'com-table-pop-fields-local'},
                    {'name':'Specifiers','label':'时间段','editor':'com-table-mapper', 'width': 200,
                       'options':[
                           {'value':"|from=1|to=10",'label':"1-10"},
                           {'value':"|from=11|to=20",'label':"11-20"},
                           {'value':"|from=21|to=30",'label':"21-30"},
                           {'value':"|from=31|to=40",'label':"31-40"},
                           {'value':"|from=41|to=50",'label':"41-50"},
                           {'value':"|from=51|to=60",'label':"51-60"},
                           {'value':"|from=61|to=70",'label':"61-70"},
                           {'value':"|from=71|to=80",'label':"71-80"},
                           {'value':"|from=81|to=90",'label':"81-90"},
                         ], },
                    {'name':'OutcomeId','label':'胜平负','editor':'com-table-mapper', 'width': 200,
                     'options':[
                          {'value':6,'label':'主赢' },
                          {'value':7,'label':'平局'},
                          {'value':8,'label':'客赢'},
                         ]}, 
                      ],
                 'fields_heads':[
                     {'name':'Specifiers_1','label':'第几粒球','editor':'com-field-number','fv_rule':'integer(+)','required':True},
                     {'name':'Specifiers','label':'时间段','editor':'com-field-select','required':True, 'options':[
                         {'value':"|from=1|to=10",'label':"1-10"},
                           {'value':"|from=11|to=20",'label':"11-20"},
                           {'value':"|from=21|to=30",'label':"21-30"},
                           {'value':"|from=31|to=40",'label':"31-40"},
                           {'value':"|from=41|to=50",'label':"41-50"},
                           {'value':"|from=51|to=60",'label':"51-60"},
                           {'value':"|from=61|to=70",'label':"61-70"},
                           {'value':"|from=71|to=80",'label':"71-80"},
                           {'value':"|from=81|to=90",'label':"81-90"},
                         ]}, 
                    {'name':'OutcomeId','label':'胜平负','editor':'com-field-select', 'required':True,
                      'options':[
                               {'value':6,'label':'主赢' },
                               {'value':7,'label':'平局'},
                               {'value':8,'label':'客赢'},
                             ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         107:{
            'heads':[
                 {'name':'content','label':'10分钟大小','editor':'com-field-table-list','fv_rule':'group_unique(Specifiers_1, Specifiers)','fv_msg':'盘口+时间段不能重复',
                  'table_heads':[
                    {'name':'Specifiers_1','label':'盘口','editor':'com-table-pop-fields-local'},
                    {'name':'Specifiers','label':'时间段','editor':'com-table-mapper', 'width': 80,
                       'options':[
                           {'value':"|from=1|to=10",'label':"1-10"},
                           {'value':"|from=11|to=20",'label':"11-20"},
                           {'value':"|from=21|to=30",'label':"21-30"},
                           {'value':"|from=31|to=40",'label':"31-40"},
                           {'value':"|from=41|to=50",'label':"41-50"},
                           {'value':"|from=51|to=60",'label':"51-60"},
                           {'value':"|from=61|to=70",'label':"61-70"},
                           {'value':"|from=71|to=80",'label':"71-80"},
                           {'value':"|from=81|to=90",'label':"81-90"},
                         ], },
                    {'name':'OutcomeId','label':'主队','editor':'com-table-span', 'width': 80,}, 
                    {'name':'OutcomeId_1','label':'客队','editor':'com-table-span', 'width': 80,}, 
                    
                      ],
                 'fields_heads':[
                     {'name':'Specifiers_1','label':'盘口','editor':'com-field-number','required':True},
                     {'name':'Specifiers','label':'时间段','editor':'com-field-select','required':True, 'options':[
                         {'value':"|from=1|to=10",'label':"1-10"},
                           {'value':"|from=11|to=20",'label':"11-20"},
                           {'value':"|from=21|to=30",'label':"21-30"},
                           {'value':"|from=31|to=40",'label':"31-40"},
                           {'value':"|from=41|to=50",'label':"41-50"},
                           {'value':"|from=51|to=60",'label':"51-60"},
                           {'value':"|from=61|to=70",'label':"61-70"},
                           {'value':"|from=71|to=80",'label':"71-80"},
                           {'value':"|from=81|to=90",'label':"81-90"},
                         ]}, 
                    {'name':'OutcomeId','label':'主队','editor':'com-field-number', 'required':True}, 
                    {'name':'OutcomeId_1','label':'客队','editor':'com-field-number', 'required':True}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         108:{
            'heads':[
                 {'name':'content','label':'5分钟1X2','editor':'com-field-table-list','fv_rule':'key_unique(Specifiers)','fv_msg':'时间段不能重复',
                  'table_heads':[
                    
                      {'name':'Specifiers','label':'时间段','editor':'com-table-pop-fields-local','inn_editor':'com-table-mapper', 'width': 200,
                       'options':[
                           {'value':"from=1|to=5", 'label':"1-5"},
                           {'value':"from=6|to=10",'label':"6-10"},
                           {'value':"from=11|to=15",'label':"11-15"},
                           {'value':"from=16|to=20",'label':"16-20"},
                           {'value':"from=21|to=25",'label':"21-25"},
                           {'value':"from=26|to=30",'label':"26-30"},
                           {'value':"from=31|to=35",'label':"31-35"},
                           {'value':"from=36|to=40",'label':"36-40"},
                           {'value':"from=41|to=45",'label':"41-45"},
                           {'value':"from=46|to=50",'label':"46-50"},
                           {'value':"from=51|to=55",'label':"51-55"},
                           {'value':"from=56|to=60",'label':"56-60"},
                           {'value':"from=61|to=65",'label':"61-65"},
                           {'value':"from=66|to=70",'label':"66-70"},
                           {'value':"from=71|to=75",'label':"71-75"},
                           {'value':"from=76|to=80",'label':"76-80"},
                           {'value':"from=81|to=85",'label':"81-85"},
                           {'value':"from=86|to=90",'label':"86-90"},
               
                         ], },
                        {'name':'OutcomeId','label':'胜平负','editor':'com-table-mapper', 'width': 200,
                         'options':[
                              {'value':1 ,'label':'主赢' },
                              {'value':2,'label':'平局'},
                              {'value':3,'label':'客赢'},
                             ]}, 
                      ],
                 'fields_heads':[
                     {'name':'Specifiers','label':'时间段','editor':'com-field-select', 'required':True,'options':[
                         {'value':"from=1|to=5", 'label':"1-5"},
                           {'value':"from=6|to=10",'label':"6-10"},
                           {'value':"from=11|to=15",'label':"11-15"},
                           {'value':"from=16|to=20",'label':"16-20"},
                           {'value':"from=21|to=25",'label':"21-25"},
                           {'value':"from=26|to=30",'label':"26-30"},
                           {'value':"from=31|to=35",'label':"31-35"},
                           {'value':"from=36|to=40",'label':"36-40"},
                           {'value':"from=41|to=45",'label':"41-45"},
                           {'value':"from=46|to=50",'label':"46-50"},
                           {'value':"from=51|to=55",'label':"51-55"},
                           {'value':"from=56|to=60",'label':"56-60"},
                           {'value':"from=61|to=65",'label':"61-65"},
                           {'value':"from=66|to=70",'label':"66-70"},
                           {'value':"from=71|to=75",'label':"71-75"},
                           {'value':"from=76|to=80",'label':"76-80"},
                           {'value':"from=81|to=85",'label':"81-85"},
                           {'value':"from=86|to=90",'label':"86-90"},
                         ]}, 
                    {'name':'OutcomeId','label':'胜平负','editor':'com-field-select', 'required':True,
                      'options':[
                              {'value':1 ,'label':'主赢' },
                              {'value':2,'label':'平局'},
                              {'value':3,'label':'客赢'},
                             ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         109:{
            'heads':[
                 {'name':'content','label':'5分钟进球','editor':'com-field-table-list','fv_rule':'group_unique(Specifiers_1, Specifiers)','fv_msg':'第几粒球+时间段不能重复',
                  'table_heads':[
                    {'name':'Specifiers_1','label':'第几粒球','editor':'com-table-pop-fields-local'},
                    {'name':'Specifiers','label':'时间段','editor':'com-table-mapper', 'width': 200,
                       'options':[
                           {'value':"|from=1|to=5", 'label':"1-5"},
                           {'value':"|from=6|to=10",'label':"6-10"},
                           {'value':"|from=11|to=15",'label':"11-15"},
                           {'value':"|from=16|to=20",'label':"16-20"},
                           {'value':"|from=21|to=25",'label':"21-25"},
                           {'value':"|from=26|to=30",'label':"26-30"},
                           {'value':"|from=31|to=35",'label':"31-35"},
                           {'value':"|from=36|to=40",'label':"36-40"},
                           {'value':"|from=41|to=45",'label':"41-45"},
                           {'value':"|from=46|to=50",'label':"46-50"},
                           {'value':"|from=51|to=55",'label':"51-55"},
                           {'value':"|from=56|to=60",'label':"56-60"},
                           {'value':"|from=61|to=65",'label':"61-65"},
                           {'value':"|from=66|to=70",'label':"66-70"},
                           {'value':"|from=71|to=75",'label':"71-75"},
                           {'value':"|from=76|to=80",'label':"76-80"},
                           {'value':"|from=81|to=85",'label':"81-85"},
                           {'value':"|from=86|to=90",'label':"86-90"},
                         ], },
                    {'name':'OutcomeId','label':'胜平负','editor':'com-table-mapper', 'width': 200,
                     'options':[
                          {'value':6,'label':'主赢' },
                          {'value':7,'label':'平局'},
                          {'value':8,'label':'客赢'},
                         ]}, 
                      ],
                 'fields_heads':[
                     {'name':'Specifiers_1','label':'第几粒球','editor':'com-field-number','required':True},
                     {'name':'Specifiers','label':'时间段','editor':'com-field-select', 'required':True,'options':[
                         {'value':"|from=1|to=5", 'label':"1-5"},
                           {'value':"|from=6|to=10",'label':"6-10"},
                           {'value':"|from=11|to=15",'label':"11-15"},
                           {'value':"|from=16|to=20",'label':"16-20"},
                           {'value':"|from=21|to=25",'label':"21-25"},
                           {'value':"|from=26|to=30",'label':"26-30"},
                           {'value':"|from=31|to=35",'label':"31-35"},
                           {'value':"|from=36|to=40",'label':"36-40"},
                           {'value':"|from=41|to=45",'label':"41-45"},
                           {'value':"|from=46|to=50",'label':"46-50"},
                           {'value':"|from=51|to=55",'label':"51-55"},
                           {'value':"|from=56|to=60",'label':"56-60"},
                           {'value':"|from=61|to=65",'label':"61-65"},
                           {'value':"|from=66|to=70",'label':"66-70"},
                           {'value':"|from=71|to=75",'label':"71-75"},
                           {'value':"|from=76|to=80",'label':"76-80"},
                           {'value':"|from=81|to=85",'label':"81-85"},
                           {'value':"|from=86|to=90",'label':"86-90"},
                         ]}, 
                    {'name':'OutcomeId','label':'胜平负','editor':'com-field-select', 'required':True,
                      'options':[
                               {'value':6,'label':'主赢' },
                               {'value':7,'label':'平局'},
                               {'value':8,'label':'客赢'},
                             ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         110:{
            'heads':[
                 {'name':'content','label':'5分钟大小','editor':'com-field-table-list','fv_rule':'group_unique(Specifiers_1, Specifiers)','fv_msg':'盘口+时间段不能重复',
                  'table_heads':[
                    {'name':'Specifiers_1','label':'盘口','editor':'com-table-pop-fields-local'},
                    {'name':'Specifiers','label':'时间段','editor':'com-table-mapper', 'width': 80,
                       'options':[
                            {'value':"|from=1|to=5", 'label':"1-5"},
                           {'value':"|from=6|to=10",'label':"6-10"},
                           {'value':"|from=11|to=15",'label':"11-15"},
                           {'value':"|from=16|to=20",'label':"16-20"},
                           {'value':"|from=21|to=25",'label':"21-25"},
                           {'value':"|from=26|to=30",'label':"26-30"},
                           {'value':"|from=31|to=35",'label':"31-35"},
                           {'value':"|from=36|to=40",'label':"36-40"},
                           {'value':"|from=41|to=45",'label':"41-45"},
                           {'value':"|from=46|to=50",'label':"46-50"},
                           {'value':"|from=51|to=55",'label':"51-55"},
                           {'value':"|from=56|to=60",'label':"56-60"},
                           {'value':"|from=61|to=65",'label':"61-65"},
                           {'value':"|from=66|to=70",'label':"66-70"},
                           {'value':"|from=71|to=75",'label':"71-75"},
                           {'value':"|from=76|to=80",'label':"76-80"},
                           {'value':"|from=81|to=85",'label':"81-85"},
                           {'value':"|from=86|to=90",'label':"86-90"},
                         ], },
                    {'name':'OutcomeId','label':'主队','editor':'com-table-span', 'width': 80,}, 
                    {'name':'OutcomeId_1','label':'客队','editor':'com-table-span', 'width': 80,}, 
                    
                      ],
                 'fields_heads':[
                     {'name':'Specifiers_1','label':'盘口','editor':'com-field-number','required':True},
                     {'name':'Specifiers','label':'时间段','editor':'com-field-select','required':True, 'options':[
                          {'value':"|from=1|to=5", 'label':"1-5"},
                           {'value':"|from=6|to=10",'label':"6-10"},
                           {'value':"|from=11|to=15",'label':"11-15"},
                           {'value':"|from=16|to=20",'label':"16-20"},
                           {'value':"|from=21|to=25",'label':"21-25"},
                           {'value':"|from=26|to=30",'label':"26-30"},
                           {'value':"|from=31|to=35",'label':"31-35"},
                           {'value':"|from=36|to=40",'label':"36-40"},
                           {'value':"|from=41|to=45",'label':"41-45"},
                           {'value':"|from=46|to=50",'label':"46-50"},
                           {'value':"|from=51|to=55",'label':"51-55"},
                           {'value':"|from=56|to=60",'label':"56-60"},
                           {'value':"|from=61|to=65",'label':"61-65"},
                           {'value':"|from=66|to=70",'label':"66-70"},
                           {'value':"|from=71|to=75",'label':"71-75"},
                           {'value':"|from=76|to=80",'label':"76-80"},
                           {'value':"|from=81|to=85",'label':"81-85"},
                           {'value':"|from=86|to=90",'label':"86-90"},
                         ]}, 
                    {'name':'OutcomeId','label':'主队','editor':'com-field-number', 'required':True}, 
                    {'name':'OutcomeId_1','label':'客队','editor':'com-field-number', 'required':True}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         333:head_all_333('第几局', '第几杀', 7),
         396:head_all_333('第几局', '第几保护', 5),
         397:head_all_333('第几局', '第几个塔', 5), 
         398:head_all_333('第几局', '第几个兵营', 5),
         556:head_all_333('第几局', '第几个小龙', 5), 
         557:head_all_333('第几局', '第几个男爵',5),
         558:head_all_333('第几局', '第几个水晶',5),
         206:{
            'heads':[
                 {'name':'content','label':'第几盘是否有抢7','editor':'com-field-table-list','fv_rule':'group_unique( Specifiers)','fv_msg':'盘数不能重复',
                  'table_heads':[
                    {'name':'Specifiers','label':'第几盘','editor':'com-table-pop-fields-local'},
                    {'name':'OutcomeId','label':'是否抢7','editor':'com-table-mapper','options':[
                        {'value':74,'label':'是' },
                        {'value':76,'label':'否'},
                        ]},
                      ],
                 'fields_heads':[
                    {'name':'Specifiers','label':'第几盘','editor':'com-field-number','fv_rule':'integer(+0)','required':True},
                    {'name':'OutcomeId','label':'是否抢7','editor':'com-field-select', 'required':True,
                      'options':[
                               {'value':74,'label':'是' },
                               {'value':76,'label':'否'},
                             ]}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         195:{
             'heads':[
                 {'name':'OutcomeId','label':'是否抢7','editor':'com-field-select','options':[
                       {'value':74,'label':'是' },
                        {'value':76,'label':'否'},
                 ]}
             ],
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
         555:{
            'heads':[
                 {'name':'content','label':'第几局击杀让分','editor':'com-field-table-list','fv_rule':'group_unique(Specifiers_1, Specifiers)','fv_msg':'盘口+时间段 不能重复',
                  'table_heads':[
                    {'name':'Specifiers','label':'第几盘','editor':'com-table-pop-fields-local'},
                    {'name':'Specifiers_1','label':'盘口','editor':'com-table-span'},
                    {'name':'OutcomeId','label':'主队','editor':'com-table-span', 'width': 80,}, 
                    {'name':'OutcomeId_1','label':'客队','editor':'com-table-span', 'width': 80,}, 
                      ],
                 'fields_heads':[
                    {'name':'Specifiers','label':'第几局','editor':'com-field-number','fv_rule':'integer(+0)','required':True},
                    {'name':'Specifiers_1','label':'盘口','editor':'com-field-number','required':True},
                    {'name':'OutcomeId','label':'主队','editor':'com-field-number', 'required':True}, 
                    {'name':'OutcomeId_1','label':'客队','editor':'com-field-number', 'required':True}, 
                 ]}
            ],
            
            'editor':'com-form-one',
            'ops_loc':'down',
            'ops':pop_edit_ops,
         },
 
    }
}





        
        
     