var ajax_fields={
    props:['tab_head','par_row'],
    data:function(){
      return {
          heads:this.tab_head.heads,
          ops:this.tab_head.ops,
          errors:{},
          row:{},
      }
    },
    mixins:[mix_fields_data,mix_nice_validator],
    template:`<div>
    <!--<div style="margin: 5px 1em;">-->
        <!--<button type="button" class="btn btn-default" title="保存" @click="save()"><i class="fa fa-save"></i><span>保存</span></button>-->
    <!--</div>-->

    <span class="oprations">
            <component style="padding: 0.5em;" v-for="op in ops" :is="op.editor" :ref="'op_'+op.name" :head="op" @operation="on_operation(op.name)"></component>
    </span>

    <form class='field-panel msg-hide' id="form">
		<field  v-for='head in heads' :key="head.name" :head="head" :row='row'></field>
	</form></div>`,

    //created:function(){
    //    // find head from parent table
    //    var table_par = this.$parent
    //    while (true){
    //        if (table_par.heads){
    //            break
    //        }
    //        table_par = table_par.$parent
    //        if(!table_par){
    //            break
    //        }
    //    }
    //    this.table_par = table_par
    //},

    methods:{
        on_show:function(){
            if(! this.fetched){
                this.get_data()
                this.fetched = true
            }
        },
        data_getter:function(){
            var self=this
            var fun = get_data [self.tab_head.get_data.fun]
            var kws = self.tab_head.get_data.kws
            fun(self,function(row){
                //ex.assign(self.row,row)
                self.row = row
            },kws)

            //var self=this
            //cfg.show_load()
            //var dt = {fun:'get_row',model_name:this.model_name}
            //dt[this.relat_field] = this.par_row[this.relat_field]
            //var post_data=[dt]
            //$.post('/d/ajax',JSON.stringify(post_data),function(resp){
            //    self.row=resp.get_row
            //    cfg.hide_load()
            //})
         },
        after_save:function(new_row){
            if(this.tab_head.after_save){
                var fun = after_save[this.tab_head.after_save.fun]
                var kws = this.tab_head.after_save.kws
                // new_row ,old_row
                fun(this,new_row,kws)
            }
            this.row=new_row
        }
    }
        // data_getter  回调函数，获取数据,


}

Vue.component('com_ajax_fields',ajax_fields)

var get_data={
    get_row:function(self,callback,kws){
        //kws={model_name ,relat_field}
        var model_name = kws.model_name
        var relat_field = kws.relat_field
        var dt = {fun:'get_row',model_name:model_name}
        dt[relat_field] = self.par_row[relat_field]
        var post_data=[dt]
        cfg.show_load()
        $.post('/d/ajax',JSON.stringify(post_data),function(resp){
            cfg.hide_load()
            callback(resp.get_row)
        })
    }
}

var after_save={
    update_or_insert:function(self,new_row,kws){
        var old_row= self.row
        self.$emit('tab-event',{name:'update-or-insert',new_row:new_row,old_row:old_row})
    }
}