require('./scss/file_uploader.scss')

/*
* config={
*    accept:""
* }
* */

export var field_file_uploader={
    props:['name','row','kw'],
    template:`<div><com-file-uploader v-model="row[name]" :config="kw.config" :readonly="kw.readonly"></com-file-uploader></div>`
}

export var com_file_uploader = {
    props:['to','value','readonly','config'],
    data:function(){

        return {
            picstr: this.value,
            pictures:this.value ? this.value.split(';'):[],
            crt_pic:''
        }
    },

    template:`<div class="file-uploader">
    <div v-if="!readonly">
        <input v-if="cfg.multiple" v-show="!cfg.com_btn" class="pic-input" type="file" @change="upload_pictures($event)" :accept="cfg.accept" multiple="multiple">
        <input v-else v-show="!cfg.com_btn" class="pic-input" type="file" @change="upload_pictures($event)" :accept="cfg.accept">
    </div>


    <div class="wrap">
        <ul class="sortable">
            <li  v-for="pic in pictures" class="item" >
                <img v-if="is_image(pic)" :src="pic" alt="" @click="cfg.on_click(pic)"/>
                <div class="file-wrap" @click="cfg.on_click(pic)" v-else>
                    <span class="file-type" v-text="get_res_type(pic)"></span>
                    <!--<span v-text="get_res_basename(pic)"></span>-->
                </div>

                <span v-if="! readonly" v-show="cfg.multiple" class="remove-btn" title="remove image" @click="remove(pic)">
                    <!--<i class="fa fa-window-close" aria-hidden="true"></i>-->
                    <i class="fa fa-times" aria-hidden="true"></i>
                </span>

            </li>
        </ul>
    </div>


     <component v-if="cfg.com_btn && ! readonly" :is="cfg.com_btn" @click.native="browse()"></component>



    </div>`,
    mounted:function(){
        var self=this
        if(this.cfg.sortable){
            ex.load_js("/static/lib/sortable.min.js",function(){
                new Sortable($(self.$el).find('.sortable')[0],{
                    onSort: function (/**Event*/evt) {
                        self.ajust_order()
                    },
                });
            })
        }

    },
    computed:{
        res_url:function(){
            return this.to ? this.to: "/_face/upload"
        },
        cfg:function(){
            var def_config = {
                accept:'image/*',
                multiple:true,
                sortable:true,
                on_click:function(url){
                    window.open(
                        url,
                        '_blank' // <- This is what makes it open in a new window.
                    );
                }
            }
            if(this.config){
                if(! this.config.hasOwnProperty('multiple') || this.config.multiple){
                    def_config.com_btn='file-uploader-btn-plus'
                }
                ex.assign(def_config,this.config)
            }

            return def_config
        }

    },
    watch:{
        value:function(new_val,old_val){
            if(this.picstr != new_val){
                this.picstr=new_val
                this.pictures = this.value ? this.value.split(';'):[]
            }
            if(!this.picstr){
                $(this.$el).find('.pic-input').val("")
            }
        }
    },
    methods:{
        browse:function(){
          $(this.$el).find('input').click()
        },
        enter:function(pic){
            this.crt_pic= pic
        },
        out:function(){
            this.crt_pic=''
        },
        upload_pictures:function (event){
            var self=this
            var file_list = event.target.files
            if(file_list.length==0){
                return
            }
            var upload_url=this.res_url

            show_upload()

            fl.uploads(file_list,upload_url,function(resp){
                if(resp){
                    if(self.cfg.multiple){
                        self.add_value(resp)
                    }else{
                        self.set_value(resp)
                    }

                }
                hide_upload(300)
            })
        },
        set_value:function(value){
            //@value: [url1,url2]
            var val= value.join(';')
            this.$emit('input',val)
        },
        add_value:function(value){
            var self=this
            var real_add = ex.filter(value,function(item){
                return !ex.isin(item,self.pictures)
            })
            var real_list= self.pictures.concat(real_add)
            var val= real_list.join(';')
            self.$emit('input',val)
        },
        ajust_order:function (){
            var list = $(this.$el).find('ul.sortable img')
            var url_list=[]
            for(var i=0;i<list.length;i++){
                var ele=list[i]
                url_list.push($(ele).attr('src'))
            }
            var val=url_list.join(';')
            this.picstr=val
            this.$emit('input',val)
        },
        remove:function(pic){
            var pics =this.picstr.split(';')
            ex.remove(pics,function(item){return pic==item})
            var val= pics.join(';')
            this.$emit('input',val)
        },
        is_image:function(url){
            var type = this.get_res_type(url)
            return ex.isin(type.toLowerCase(),['jpg','png','webp','gif','jpeg','ico'])
        },
        get_res_type:function(url){
            var mt = /[^.]+$/.exec(url)
            if(mt.length>0){
                return mt[0]
            }else{
                return ""
            }
        },
        get_res_basename:function(url){
            var mt = /[^/]+$/.exec(url)
            if(mt.length>0){
                return mt[0]
            }else{
                return mt[0]
            }
        }
    }
}

var plus_btn={
    props:['accept'],
    template:`<div class="file-uploader-btn-plus">
        <div class="inn-btn"><span>+</span></div>
        <div style="text-align: center">添加文件</div>
    </div>`,
}
Vue.component('file-uploader-btn-plus',plus_btn)

Vue.component('com-file-uploader',com_file_uploader)
Vue.component('field-file-uploader',field_file_uploader)

