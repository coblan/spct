var multi_chosen={
    props:['value','options'],
    template:`<select  multiple="multiple" class="multi-chosen form-control">
    <option v-for="option in options" :value="option.value" v-text="option.label"></option>
</select>`,
    mounted:function(){
        var self=this
        ex.load_css('https://cdn.bootcss.com/chosen/1.8.2/chosen.min.css')
        ex.load_js('https://cdn.bootcss.com/chosen/1.8.2/chosen.jquery.min.js',function(){
            $(self.$el).chosen({
                search_contains:true
            }).change(function(event){
                self.$emit('input',$(this).val())
            });
            self.setValue(self.value)
        })
    },
    watch:{
        value:function(nv){
            this.setValue(nv)
        }
    },
    methods:{
        setValue:function(val){
            $(this.$el).val(val);
            $(this.$el).trigger("chosen:updated");
        }
    }
}

Vue.component('multi-chosen',multi_chosen)