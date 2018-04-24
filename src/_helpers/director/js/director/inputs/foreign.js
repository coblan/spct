
var forignEdit={
    template:`<div class="forign-key-panel">
        <button v-if="has_pk()" @click="jump_edit(kw.row[name])" title="edit">
            <i class="fa fa-pencil-square-o" aria-hidden="true"></i></button>
        <button @click="jump_edit()" title="create new"><i class="fa fa-plus" aria-hidden="true"></i></button>
    </div>`,
    props:['kw','name','page_name'],
    methods:{
        jump_edit:function(pk){
            var name = this.name
            var kw=this.kw
            var page_name=this.page_name || this.name
            var options=ex.findone(kw.heads,{name:name}).options
            var row=kw.row
            var pk= pk || ''

            var url=ex.template('{engine_url}/{page_name}.edit?pk={pk}',{
                engine_url:engine_url,
                page_name:page_name,
                pk:pk
            })
            ln.openWin(url,function(resp){
                if(resp.del_rows){
                    ex.remove(options,function(option){
                        return ex.isin(option,resp.del_rows,function(op,del_row){
                            return op.value==del_row.pk
                        })
                    })
                }else if(resp.row){
                    if(pk){
                        var option =ex.findone(options,{value:pk})
                        option.label=resp.row._label
                    }else{
                        options.push({label:resp.row._label,value:resp.row.pk})
                        row[name]=resp.row.pk
                    }
                }
            })
        },
        has_pk:function(){
            if(this.kw.row[this.name]){
                return true
            }else{
                return false
            }
        }
    }
}

ex.append_css(`
<style type="text/css">
    .forign-key-panel{
        padding: 6px;
    }
</style>`)

Vue.component('forign-edit',forignEdit)