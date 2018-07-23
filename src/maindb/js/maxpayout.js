var maxpayout={
    mounted:function(){
        this.heads_cach = this.fields_heads
    },
    computed:{
        fields_heads:function(){
            return this.heads
        }
    }
}

window.maxpayout_form_logic=maxpayout