export var field_file_uploader={
    props:['row','head'],
    template:`<div class="com-field-app-pkg-uploader">
        <com-file-uploader-tmp v-if="has_merchant" :name='head.name' v-model="row[head.name]" :config="head.config" :readonly="head.readonly"></com-file-uploader-tmp>
    </div>`,
    data(){
        return {
            has_merchant:false
        }
    },
    mounted(){
        if(this.row.merchant){
            this.head.config.upload_url = ex.appendSearch(this.head.config.upload_url,{merchant:this.row.merchant})
            this.has_merchant= true
        }
    },
    computed:{
        url:function(){
            return this.row[this.head.name]
        },
        merchant(){
            return this.row.merchant
        }
    },
    watch:{
        merchant(){
            this.head.config.upload_url = ex.appendSearch(this.head.config.upload_url,{merchant:this.row.merchant})
            this.has_merchant= true
        },
        url:function(v){
            var mt =/([^\?]+)\?([^\?]+)/.exec(v)
            if(mt){
                var args = ex.parseSearch(mt[2])
                if(args.version_code){
                    this.row.versionid = args.version_code
                }
                if(args.version_name){
                    this.row.versionname = args.version_name
                }
                if(args.size){
                    this.row.size = args.size
                }
                if(args.md5){
                    this.row.md5 = args.md5
                }

                this.row[this.head.name] = mt[1]
            }
        }
    }
}

Vue.component('com-field-app-pkg-uploader',field_file_uploader)

var app_pkg={
    mounted:function(){
        //this.updateReadonly()
    },
    watch:{
        'row.terminal':function (){
            //this.updateReadonly()
        }
    },
    methods:{
        updateReadonly:function(){
            var self=this
            ex.each(self.heads,function(head){
                if(ex.isin(head.name,['versionid','versionname']) ){
                    // 2 == android
                    if(self.row.terminal==2){
                        head.readonly=true
                    }else{
                        head.readonly=false
                    }
                }
            })
        }
    }
}
window.app_pkg=app_pkg

