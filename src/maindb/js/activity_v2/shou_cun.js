require('./scss/shou_cun.scss')

Vue.component('com-shouchun',{
    template:`<div class="com-shouchun">

    <!--<button @click="update_data()">获取</button>-->

    <table>
    <tr v-for="row in rows">
        <td v-for="head in heads"  :class="head.scls">
            <div   v-if="row[head.name]" v-text="head.top_label"></div>
            <div v-text="row[head.name]"></div>
        </td>
        <td class="mybtn-col">
            <div :class="['mybtn',{disabled:!row.submitable}]" @click="submit(row)"><span class="center-vh" style="white-space: nowrap" v-text="action_label(row)"></span></div>
        </td>
    </tr>
    </table>
    </div>`,
    data:function(){
        return {
            heads:[
                {name:'label',scls:'big-col',top_label:''},
                {name:'chargeTime',scls:'data-col',top_label:'存款'},
                {name:'amount',scls:'data-col',top_label:'存入'},
                {name:'bonus',scls:'data-col green',top_label:'可得红利'},

            ],
            rows:[]
        }
    },
    /*
     "chargeTime": "2019-01-09T11:34:28.207Z",
     "amount": 0,
     "bonus": 0,
     "Done": true
    * */
    mounted:function(){
        var self=this
        //setTimeout(function(){
            self.update_data()
        //},5000)
    },
    methods:{
        action_label:function(row){
            var dc ={
                0:'参加活动',
                1:'已参加',
                2:'已发放',
                3:'已过期'
            }
            return dc[row.state]
        },
        update_data:function(){
            //cfg.showMsg('开始更新数据')
            var mock_data={
                data:[
                    {chargeTime:'04-21 22:30',amount:50,bonus:50,state:1},
                    {chargeTime:'2019-01-22 22:30:30',amount:'100000',bonus:'1239999',state:0},
                ]
            }
            var dec_rows=[
                {label:'首存',action:'',submitable:false},
                {label:'再存',action:'',submitable:false},
            ]
            var self=this
            cfg.show_load()

            jb_js.get('/activity/charge/list?activityId='+activity.pk,function(resp){
                cfg.hide_load()
                //cfg.showMsg('首存数据:'+JSON.stringify(resp))
                self.rows = resp.data

                var last_done=true
                for(var i=0;i<self.rows.length;i++){
                    var row = self.rows[i]
                    ex.vueAssign(row,dec_rows[i])
                    row.Type=i+1
                    if(row.state != 0){
                        last_done=true
                    }else if(last_done){
                        row.submitable=true
                        last_done=false
                    }
                }

                //cfg.showMsg('追踪数据:'+JSON.stringify(self.rows))

            },mock_data)
        },
        submit:function(row){
            if(!row.submitable){
                return
            }
            var mock_data={success:1}
            var post_data={
                ActivityId:activity.pk,
                Type:row.Type,
            }
            var self=this
            jb_js.post('/activity/charge/do',post_data,function(resp){

                if(resp.success ){
                    cfg.showMsg('参加成功！')
                    self.update_data()
                }else{
                    cfg.showError(resp.error_description)
                }

            },mock_data)
        }
    }
})