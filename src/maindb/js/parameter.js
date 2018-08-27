var parameter_form_logic={
    methods:{
        save:function(){
            var self=this
            layer.confirm('确认要保存修改吗？', {icon: 3, title:'提示'}, function(index){
                layer.close(index)

                ex.vueSuper(self,{fun:'save'})

            })
        }
    }
}

window.parameter_form_logic =parameter_form_logic

var parameter ={
    props:['row','head'],
        template:`<div style="position: relative">
            <component :is="head.subhead.editor" :head="head.subhead" :row="row"></component>
            <div style="position: absolute;left: 26em;top:0;width: 4em">
                <input type="checkbox" :id="'id_wrap_'+head.name" v-model='is_active'>
			    <label :for="'id_wrap_'+head.name"><span>激活</span></label>
			 </div>
			</div>`,

    computed:{
        is_active:{
            set:function(v){
                var self=this
                if(v){
                    if(! ex.isin(this.head.name,this.row.active_names)){
                        this.row.active_names.push(this.head.name)
                    }
                }else{
                    ex.remove(this.row.active_names,function(name){return name ==self.head.name})
                }
            },
            get:function(){
                return ex.isin(this.head.name,this.row.active_names)
            }
        }
    }


}

Vue.component('com-field-parameter',parameter)


var ping_lue={
    props:['row','head'],
    template:`<div style="position: relative">
               <input type="number" v-model="row.WithdrawIntervalMinutes" style="width: 6em">
               <span>分 </span>
               <input type="number" v-model="row.WithdrawIntervalCount" style="width: 4em">
               <span>次</span>
			</div>`,
}
Vue.component('com-field-pinglue',ping_lue)