export  var  maxpayout={
    watch:{
        normed_heads:function(){
            this.update_nice()
        }
    },
    computed:{
        normed_heads:function(){
            var  type_head=ex.findone(this.heads,{name:'limittype'})
            var crt_type = this.row.limittype
            var keywords = crt_type? type_head.keywords[crt_type]:[]
            var var_fields=type_head.var_fields
            var heads = ex.filter(this.heads,function(head){
                if(ex.isin(head.name,var_fields) && !ex.isin(head.name,keywords)){
                    head.required =false
                    return false
                }else{
                    if(ex.isin(head.name,var_fields)){
                        head.required =true
                    }

                    return true
                }
            })
            return heads
        }
    },


    methods:{

        //after_save:function(){
        //    var relationno_head=ex.findone(this.dict_heads,{name:'relationno'})
        //    if(relationno_head){
        //        var opt = ex.findone(relationno_head.options,{value:this.row.relationno})
        //        Vue.set(this.row,'_relationno_label',opt.label)
        //    }else {
        //        Vue.set(this.row,'_relationno_label','')
        //    }
        //}
    }
}

window.maxpayout_form_logic=maxpayout