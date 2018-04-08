

var depart_btn_panel={
    props:['crt_depart','depart_list'],
    template:`<div id="depart-btn" style="text-align: center;padding:0.3em 0;border-bottom: 1px solid #ffffff;">
        <div class="btn-group" role="group" aria-label="..." >
        <a type="button" :class="['btn btn-default',{'btn-info':crt_depart.pk==depart.pk}]" v-for="depart in depart_list" @click="depart_link(depart.pk)" v-text="depart.label">Left</a>
        </div>
    </div>`,
    methods:{
        depart_link:function(pk){
            ff.replace(ex.appendSearch({_depart:pk}))
        }
    }
}

Vue.component('depart-btn-panel',depart_btn_panel)



