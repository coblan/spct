require('./scss/multi_picture.scss')

/*
* config={
*    accept:""
* }
* */

export var field_file_uploader={
    props:['name','row','kw'],
    template:`<div><com-file-uploader v-model="row[name]" :config="kw.config"></com-file-uploader></div>`
}

export var com_file_uploader = {
    props:['to','value','config'],
    data:function(){

        return {
            picstr: this.value,
            pictures:this.value ? this.value.split(';'):[],
            crt_pic:''
        }
    },

    template:`<div class="com_multi_picture">

    <input v-if="cpt_config.multiple" class="pic-input" type="file" @change="upload_pictures($event)" :accept="cpt_config.accept" multiple="multiple">
    <input v-else class="pic-input" type="file" @change="upload_pictures($event)" :accept="cpt_config.accept">

     <ul class="sortable">
        <li  v-for="pic in pictures" class="item" >
            <img v-if="is_image(pic)" :src="pic" alt=""/>
            <div v-else style="width: 5em;text-align: center;padding:1em 0;word-wrap: break-word;">
                <span v-text="get_res_type(pic)" style="font-size: 300%;font-weight: 700;"></span>
                <span v-text="get_res_basename(pic)"></span>
            </div>
            <!--<span class="remove-btn" title="remove image" @click="remove(pic)">-->
                <!--<i class="fa fa-window-close" aria-hidden="true"></i>-->
            <!--</span>-->

        </li>
    </ul>

    </div>`,
    mounted:function(){
        var self=this
        if(this.cpt_config.sortable){
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
        cpt_config:function(){
            var def_config = {
                accept:'image/*',
                multiple:true,
                sortable:true,
            }
            if(this.config){
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
                    var val= resp.join(';')
                    self.$emit('input',val)
                }
                hide_upload(300)
            })
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
        //remove:function(pic){
        //    var pics =this.picstr.split(';')
        //    ex.remove(pics,function(item){return pic==item})
        //    var val= pics.join(';')
        //    this.$emit('input',val)
        //}
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

