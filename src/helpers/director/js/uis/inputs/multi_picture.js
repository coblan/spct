require('./scss/multi_picture.scss')

export var com_multi_picture = {
    props:['to','value'],
    data:function(){
        return {
            picstr: this.value,
            pictures:this.value ? this.value.split(';'):[],
            crt_pic:''
        }
    },
    template:`<div class="com_multi_picture">

    <input class="pic-input" type="file" @change="upload_pictures(event)" accept="image/*" multiple="multiple">

     <ul class="sortable">
        <li  v-for="pic in pictures" class="item" >
            <img :src="pic" alt=""/>
            <!--<span class="remove-btn" title="remove image" @click="remove(pic)">-->
                <!--<i class="fa fa-window-close" aria-hidden="true"></i>-->
            <!--</span>-->

        </li>
    </ul>

    </div>`,
    mounted:function(){
        var self=this
        ex.load_js("/static/lib/sortable.min.js",function(){
            new Sortable($(self.$el).find('.sortable')[0],{
                onSort: function (/**Event*/evt) {
                    self.ajust_order()
                },
            });
        })
    },
    computed:{
        res_url:function(){
              return this.to ? this.to: "/res/upload"
          },

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
            fl.uploads(file_list,upload_url,function(resp){
                if(resp){
                    var val= resp.join(';')
                    self.$emit('input',val)
                }
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
}


}