export  var  maxpayout={
    computed:{
        dict_heads:function(){
            var  this_head=ex.findone(this.heads,{name:'relationno'})
            if(this.row.limittype == 11 ){
                var heads =ex.filter(this.heads,function(head){
                    if(head.name =='accountid'|| head.name == 'relationno'){
                        return false
                    }else{
                        return true
                    }
                })
            } else if(ex.isin(this.row.limittype,[12,13]) ){
                var heads =ex.filter(this.heads,function(head){
                        if(head.name=='accountid'){
                            return false
                        }else{
                            return true
                        }
                })
            }
            else if(this.row.limittype == 21) {
                var heads =ex.filter(this.heads,function(head){
                    if(head.name=='relationno'){
                        return false
                    }else{
                        return true
                    }
                })
            }else{
                var heads=this.heads
            }

            if(ex.isin(this.row.limittype,[12,22])){
                var options=this_head.oddstype_options
            }else{
                var options=this_head.user_options
            }

            var relationno_head=ex.findone(heads,{name:'relationno'})
            if(relationno_head){
                relationno_head.editor='sim_select'
                Vue.set(relationno_head,'options',options)
            }
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