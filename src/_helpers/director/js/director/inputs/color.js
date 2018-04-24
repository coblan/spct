var color={
    props:['value'],
    template: `<input type="text">`,
    methods:{
        init_and_listen:function(){
            var self = this
            Vue.nextTick(function(){
                $(self.$el).spectrum({
                    color: self.value,
                    showInitial: true,
                    showInput: true,
                    preferredFormat: "name",
                    change: function(color) {
                        self.src_color=color.toHexString()
                        self.$emit('input',self.src_color)
                    }
                });
            })
        }
    },
    watch:{
        value:function (value) {
            if(this.src_color !=value){
                this.init_and_listen()
            }
        }
    },
    mounted:function(){
        var self=this;
        ex.load_css('/static/lib/spectrum1.8.0.min.css')
        ex.load_js('/static/lib/spectrum1.8.0.min.js',function () {
            self.init_and_listen()
        })
    },
}

Vue.component('color',color)