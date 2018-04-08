var ajax_fields={
    props:['kw'],
    data:function(){
      return {
          heads:this.kw,
          errors:{},
          row:{},
          //fields_kw:{
          //    heads:this.kw,
          //    errors:{},
          //    row:{}
          //}
      }
    },
    mixins:[mix_fields_data,mix_nice_validator],
    template:`<div>
    <div style="margin: 5px 1em;">
        <button type="button" class="btn btn-default" title="保存" @click="save()"><i class="fa fa-save"></i><span>保存</span></button>
    </div>

    <form class='field-panel msg-hide' id="form">
		<field  v-for='head in heads' :key="head.name" :head="head" :row='row'></field>
	</form></div>`,

        // data_getter  回调函数，获取数据,


}

Vue.component('com_ajax_fields',ajax_fields)