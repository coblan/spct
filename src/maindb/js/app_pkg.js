export var field_file_uploader={
    props:['row','head'],
    template:`<div><com-file-uploader-tmp v-model="row[head.name]" :config="head.config" :readonly="head.readonly"></com-file-uploader-tmp></div>`,
    computed:{
        url:function(){
            return this.row[this.head.name]
        }
    },
    watch:{
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
        this.updateReadonly()
    },
    watch:{
        'row.terminal':function (){
            this.updateReadonly()
        }
    },
    methods:{
        updateReadonly:function(){
            var self=this
            ex.each(self.heads,function(head){
                if(ex.isin(head.name,['versionid','versionname']) ){
                    if(self.row.terminal==1){
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

