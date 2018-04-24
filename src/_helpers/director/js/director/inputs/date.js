/**
 * Created by heyulin on 2017/1/24.
 *
 >->front/input.rst>
 =======
 inputs
 =======

 date
 ========
 ::

 <date v-model='variable'></date>  // 选择默认set=date ,即选择日期

 <date v-model='variable' set='month'></date> // 选择 set=month ,即选择月份

 <date v-model='variable' set='month' :config='{}'></date>  //  config 是自定义的配置对象，具体需要参加帮助文件

 datetime
 ===========
 ::

 <datetime v-model='variable' :config='{}'></datetime> // 选择日期和时间

 color
 ======

 forign-edit
 ============
 示例::

 <forign-edit :kw="person.emp_info" name="user" page_name="user" ></forign-edit>

 <-<
 */



var date_config_set={
    date:{
        language: "zh-CN",
        format: "yyyy-mm-dd",
        autoclose: true,
        todayHighlight: true,

    },
    month:{
        language: "zh-CN",
        format: "yyyy-mm",
        startView: "months",
        minViewMode: "months",
        autoclose: true,


    },
}

Vue.component('date',{
    //template:'<input type="text" class="form-control">',
    template:` <div class="input-group datetime-picker" style="width: 12em;">
                <input type="text" class="form-control input-sm" readonly :placeholder="placeholder"/>
                <div class="input-group-addon" >
                    <i v-if="! value" @click="click_input()" class="fa fa-calendar" aria-hidden="true"></i>
                    <i v-else @click="$emit('input','')" class="fa fa-calendar-times-o" aria-hidden="true"></i>
                </div>
                </div>`,
    props:['value','set','config','placeholder'],
    mounted:function () {
        var self=this
        if(!this.set){
            var def_conf=date_config_set.date
        }else{
            var def_conf=date_config_set[this.set]
        }
        if(this.config){
            ex.assign(def_conf,this.config)
        }
        self.input=$(this.$el).find('input')

        ex.load_css('/static/lib/bootstrap-datepicker1.6.4.min.css')

        ex.load_js('/static/lib/bootstrap-datepicker1.6.4.min.js',function(){
            ex.load_js('/static/lib/bootstrap-datepicker1.6.4.zh-CN.min.js',function(){
                self.input.datepicker(def_conf).on('changeDate', function(e) {
                    self.$emit('input',self.input.val())
                })
                // if has init value,then init it
                if(self.value){
                    self.input.datepicker('update',self.value)
                    self.input.val(self.value)
                }
            })
        })
    },
    methods:{
        click_input:function(){
            this.input.focus()
        }
    },
    watch:{
        value:function (n) {
            this.input.datepicker('update',n)
            this.input.val(n)

        }
    }
})


Vue.component('datetime',{
    //data:function(){
    //    return {
    //        input_value:'',
    //    }
    //},
    //template:'<input type="text" class="form-control">',
    template:`<span class="datetime-picker">
                <span class="cross" @click="$emit('input','')">X</span>
                <input type="text" readonly/>
                </span>`,
    props:['value','config'],
    mounted:function () {
        var self=this
        var def_conf={
            language: "zh-CN",
            format: "yyyy-mm-dd hh:ii",
            autoclose: true,
            todayHighlight: true,
        }
        if(self.config){
            ex.assign(def_conf,this.config)
        }
        self.input=$(this.$el).find('input')

        ex.load_css('/static/lib/smalot-bootstrap-datetimepicker2.4.3.min.css')
        ex.load_js('/static/lib/moment2.17.1.min.js')
        ex.load_js('/static/lib/smalot-bootstrap-datetimepicker2.4.3.min.js',function(){

            self.input.datetimepicker(def_conf).on('changeDate', function(e) {
                self.$emit('input',self.input.val())
            })

            // if has init value,then init it
            if(self.value){
                self.input.datepicker('update',self.value)
                self.input.val(self.value)
            }

        })
    },

    watch:{
        value:function (n) {
            this.input.val(n)
            this.input.val(n)
        },
        //input_value:function(n){
        //    this.$emit('input',n)
        //}
    }
})


