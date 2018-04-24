/**
 * Created by heyulin on 2017/1/24.
 *
>->front/input.rst>
=======
inputs
=======


color
======

forign-edit
============
示例::

    <forign-edit :kw="person.emp_info" name="user" page_name="user" ></forign-edit>

<-<
 */



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

ex.append_css(
    `<style type="text/css" media="screen">
    /*.datetime-picker{*/
        /*position: relative;*/
        /*display: inline-block;*/
    /*}*/
    .datetime-picker input[readonly]{
        background-color: white;
    }
	/*.datetime-picker .cross{*/
	    /*display: none;*/
	/*}*/
	/*.datetime-picker:hover .cross{*/
	    /*display: inline-block;*/
	    /*position: absolute;*/
	    /*right: 8px;*/
	    /*top:3px;*/
	    /*cursor: pointer;*/

	/*}*/
</style>
 `
)

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

var check_box={
    model: {
        prop: 'checked',
        event: 'change',
    },
    props:['value','checked'],
    methods:{
        on_click:function(){
            $(this.$el).find('input').click()
            this.$emit('change',this.checked)
        },
    },
    data:function(){
        var checked = this.checked || []
        return {
            inn_checked:checked,
        }
    },
    watch:{
        inn_checked:function(v){
            this.$emit('change',v)
        },
        checked:function(v){
            this.inn_checked=v
        }
    },
    computed:{
        is_checked:function(){
            if(this.value){
                return this.inn_checked.indexOf(this.value)!=-1
            }else{
                return this.inn_checked
            }
        }
    },
    template:` <span class="com-checkbox" @click="on_click()">
                <input type="checkbox" :value="value" v-model='inn_checked' style="display: none"/>
                  <i class="fa fa-check-circle" aria-hidden="true" v-if='is_checked' style="color: #009926"></i>
                  <i class="fa fa-circle-thin" aria-hidden="true" v-else></i>
              </span>`
}
Vue.component('com-check-box',check_box)