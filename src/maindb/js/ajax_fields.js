var ajax_fields={
    props:['tab_head','par_row'],
    data:function(){
      return {
          heads:this.tab_head.fields_heads,
          ops:this.tab_head.fields_ops,
          relat_field:this.tab_head.relat_field,
          model_name:this.tab_head.model_name,
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


    methods:{
        on_show:function(){
            if(! this.fetched){
                this.get_data()
                this.fetched = true
            }
        },
        data_getter:function(){
            var self=this
            cfg.show_load()
            var dt = {fun:'get_row',model_name:this.model_name}
            dt[this.relat_field] = this.par_row[this.relat_field]
            var post_data=[dt]
            $.post('/d/ajax',JSON.stringify(post_data),function(resp){
                self.row=resp.get_row
                cfg.hide_load()
            })
         }
    }
        // data_getter  回调函数，获取数据,


}

Vue.component('com_ajax_fields',ajax_fields)