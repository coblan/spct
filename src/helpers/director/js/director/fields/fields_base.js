export var field_base={
    props: {
        head:{
            required:true
        },
        row:{
            required:true
        },
        //kw:{
        //    required:true
        //},
    },
    computed:{
        //row:function(){return this.kw.row},
        //errors:function() {
        //    if(!this.kw.errors){
        //        Vue.set(this.kw,'errors',{})
        //    }
        //    return this.kw.errors
        //},
        //head:function(){
        //    var heads = this.kw.heads
        //    for (var x=0;x<heads.length;x++) {
        //        var head = heads[x]
        //        if (head.name == this.name) {
        //            return head
        //        }
        //    }
        //
        //}
    },
    methods: {
        error_data: function (name) {
            if (this.errors[name]) {
                return this.errors[name]
            } else {
                return ''
            }
        }
    },
    components: {
        linetext: {
            props:['row','head'],
            template:`<div>
            			<span v-if='head.readonly' v-text='row[head.name]'></span>
            			<input v-else type="text" class="form-control input-sm" v-model="row[head.name]"
            		 	    :id="'id_'+head.name" :name="head.name"
                        	:placeholder="head.placeholder" :autofocus="head.autofocus" :maxlength='head.maxlength'>
                       </div>`,
        },
        number: {
            props:['row','head'],

            template: `<div><span v-if='head.readonly' v-text='row[head.name]'></span>
            		<input v-else type="number" class="form-control input-sm" v-model="row[head.name]" :id="'id_'+head.name"
            		    :name="head.name"
                        :placeholder="head.placeholder" :autofocus="head.autofocus"></div>`
        },
        password: {
            props:['row','head'],
            template: `<input type="password" :id="'id_'+head.name" class="form-control input-sm" v-model="row[head.name]" :placeholder="head.placeholder" :readonly='head.readonly'>`
        },
        blocktext: {
            props:['row','head'],
            //data:function(){
            //    return {
            //        org_height:0,
            //    }
            //},
            //mounted:function(){
            //    var self=this
            //    Vue.nextTick(function(){
            //        self.on_input()
            //    })
            //
            //},
            //methods:{
            //    on_input:function(){
            //        if(this.kw.readonly) return
            //        var textarea = $(this.$el).find('textarea')[0]
            //        if(this.org_height!=textarea.scrollHeight){
            //            $(textarea).height(textarea.scrollHeight-12)
            //            this.org_height=textarea.scrollHeight
            //        }
            //    }
            //},
            //computed:{
            //    value:function(){
            //        return this.row[this.name]
            //    }
            //},
            //watch:{
            //    value:function(v){
            //        var self=this
            //        Vue.nextTick(function(){
            //            self.on_input()
            //        })
            //    }
            //},
            template: `<div>
            <span v-if='head.readonly' v-text='row[head.name]'></span>
            <textarea v-else class="form-control input-sm" rows="3" :id="'id_'+head.name" v-model="row[head.name]" :placeholder="head.placeholder" :readonly='head.readonly'></textarea>
            </div>`
        },
        color:{
            props:['name','row','kw'],
            template: `<input type="text" v-model="row[name]" :id="'id_'+name" :readonly='kw.readonly'>`,
            methods:{
                init_and_listen:function(){
                    var self = this
                    Vue.nextTick(function(){
                        $(self.$el).spectrum({
                            color: self.row[self.name],
                            showInitial: true,
                            showInput: true,
                            preferredFormat: "name",
                            change: function(color) {
                                self.src_color=color.toHexString()
                                self.row[self.name] = color.toHexString();
                            }
                        });
                    })
                }
            },
            watch:{
                input_value:function (value) {
                    if(this.src_color !=value){
                        this.init_and_listen()
                    }
                }
            },
            computed:{
                input_value:function () {
                    return this.row[this.name]
                }
            },
            mounted:function(){
                var self=this;
                ex.load_css('/static/lib/spectrum1.8.0.min.css')
                ex.load_js('/static/lib/spectrum1.8.0.min.js',function () {
                    self.init_and_listen()
                })
            },
        },
        logo:{// absolate
            props:['name','row','kw'],
            template:`<logo-input :up_url="kw.up_url" :web_url.sync="row[name]" :id="'id_'+name"></logo-input>`
        },
        picture:{
            props:['row','head'],
            template:`<div class="picture">
            <input class="virtual_input" style="position:absolute;height: 0;width: 0;" type="text"  :name="head.name" v-model="row[head.name]">
            <img class="img-uploador" v-if='head.readonly' :src='row[head.name]'/>
			<img-uploador @select="on_uploader_click()" v-else :up_url="head.up_url" v-model="row[head.name]" :id="'id_'+head.name" :config="head.config"></img-uploador></div>`,
            methods:{
                on_uploader_click:function(){
                    $(this.$el).find('.virtual_input').focus()
                }
            }
        },
        sim_select:{
            props:['row','head'],
            data:function(){
                var inn_config={}
                if(this.head.config){
                    ex.assign(inn_config,this.head.config)
                }
                return {
                    model:this.row[this.head.name],
                    cfg:inn_config
                }
            },
            template:`<div>
            <span v-if='head.readonly' v-text='get_label(head.options,row[head.name])'></span>
            <select v-else v-model='row[head.name]'  :id="'id_'+head.name"  class="form-control input-sm">
            	<option v-for='opt in orderBy(head.options,"label")' :value='opt.value' v-text='opt.label'></option>
            </select>
            </div>`,
            mounted:function(){
                if(this.head.default && !this.row[this.head.name]){
                    Vue.set(this.row,this.head.name,this.head.default)
                    //this.row[this.name]=this.kw.default
                }
            },
            methods:{
                get_label:function(options,value){
                    var option = ex.findone(options,{value:value})
                    if(!option){
                        return '---'
                    }else{
                        return option.label
                    }
                },
                orderBy:function(array,key){
                    if(this.head.orgin_order || this.cfg.orgin_order){
                        return array
                    }else{
                        return order_by_key(array,key)
                    }

                }
            }
        },
        search_select:{
            props:['row','head'],
            data:function(){
                return {
                    model:this.row[this.head.name]
                }
            },
            template:`<div>
            <span v-if='head.readonly' v-text='get_label(head.options,row[head.name])'></span>
            <select v-else v-model='row[head.name]'  :id="'id_'+head.name"  class="selectpicker form-control" data-live-search="true">
            	<option v-for='opt in orderBy(head.options,"label")' :value='opt.value'
            	 :data-tokens="opt.label" v-text='opt.label'></option>
            </select>
            </div>`,
            mounted:function(){
                var self=this
                if(this.head.default && !this.row[this.head.name]){
                    Vue.set(this.row,this.head.name,this.head.default)
                }
                ex.load_css("/static/lib/bootstrap-select.min.css")
                ex.load_js("/static/lib/bootstrap-select.min.js",function(){
                    $(self.$el).find('.selectpicker').selectpicker()
                })
            },
            methods:{
                get_label:function(options,value){
                    var option = ex.findone(options,{value:value})
                    if(!option){
                        return '---'
                    }else{
                        return option.label
                    }
                },
                orderBy:function(array,key){
                    return order_by_key(array,key)
                }
            }
        },

        check_select:{
            props:['row','head'],
            computed:{
                selected:{
                    get:function(){
                        var data=this.row[this.head.name]
                        if(data){
                            return data.split(',')
                        }else{
                            return []
                        }

                    },
                    set:function(v){
                        this.row[this.head.name]=v.join(',')
                    }

                }
            },
            template:`<div>
                <ul>
                <li v-for='option in head.options' v-if="option.value"><input type="checkbox" :value="option.value" v-model="selected"/><span v-text="option.label"></span></li>
                </ul>
            </div>`,
        },
        field_multi_chosen:{
            props:['row','head'],
            template:`<div>
	        	<ul v-if='head.readonly'><li v-for='value in row[head.name]' v-text='get_label(value)'></li></ul>
	        	<multi-chosen v-else v-model='row[head.name]' :id="'id_'+head.name" :options='head.options'></multi-chosen>
	        	</div>`,
            methods:{
                get_label:function (value) {
                    for(var i =0;i<this.head.options.length;i++){
                        if(this.head.options[i].value==value){
                            return this.head.options[i].label
                        }
                    }
                }
            }
        },

        tow_col:{
            props:['row','head'],
            template:`<div>
	        	<ul v-if='head.readonly'><li v-for='value in row[head.name]' v-text='get_label(value)'></li></ul>
	        	<tow-col-sel v-else v-model='row[head.name]' :id="'id_'+head.name" :choices='head.options' :size='head.size' ></tow-col-sel>
	        	</div>`,
            methods:{
                get_label:function (value) {
                    for(var i =0;i<this.head.options.length;i++){
                        if(this.head.options[i].value==value){
                            return this.head.options[i].label
                        }
                    }
                }
            }
        },
        bool:{
            props:['row','head'],
            template:`<div class="checkbox">
	        <input type="checkbox" :id="'id_'+head.name" v-model='row[head.name]' :disabled="head.readonly">
			 <label :for="'id_'+head.name"><span v-text='head.label'></span></label>
					  </div>`
        },
        date: {
            props:['name','row','kw'],
            template:`<div><span v-if='kw.readonly' v-text='row[name]'></span>
                                <date v-else v-model="row[name]" :id="'id_'+name"
                                    :placeholder="kw.placeholder"></date>
                               </div>`,
        },
        datetime:{
            props:['name','row','kw'],
            template:`<div><span v-if='kw.readonly' v-text='row[name]'></span>
            			<datetime  v-model="row[name]" :id="'id_'+name"
                        	:placeholder="kw.placeholder"></datetime>
                       </div>`,
        },
        richtext:{
            props:['name','row','kw'],
            template:`<div><span v-if='kw.readonly' v-text='row[name]'></span>
            			<ckeditor  v-model="row[name]" :id="'id_'+name"></ckeditor>
                       </div>`,
        },

    }

}


