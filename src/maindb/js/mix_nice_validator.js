var nice_validator={
    mounted:function(){
        var self=this
        var validator={}
        ex.each(this.heads,function(head){
            if(head.required){
                validator[head.name]='required'
            }
        })
        this.nice_validator =$(this.$el).find('.field-panel').validator({
            fields: validator,
        });
    },
}

window.mix_nice_validator=nice_validator