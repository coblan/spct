

export class DepartSelect{
    constructor(back_url,root){
        this.back_url=back_url
        this.root=root || {pk:null,name:'公司'}
    }
    select(callback){
        ff.load_vue_com({
            url:"/static/organize/organize.pack.js",
            name:'depart_select',
            label:'选择部门',
            com_html:`<com-depart-browser :url="url" :root="root"></com-depart-browser>`,
            data:{
                url:this.back_url,
                root:this.root
            },
            callback:function(depart){
                callback(depart)
            }
        })
    }
}

var depart={
    props:['url','root'],
    data:function(){
        return {
            parents:[this.root],
            items:[],

            checked:[],
            clip:[],
            depart_back_call:back_ops(this.url)
        }
    },
    computed:{
        par:function(){
            return this.parents[this.parents.length-1]
        } ,
        //root:function(){
        //    return this.parents[0]
        //}
    },
    mounted:function(){
        this.dir_data(this.par)
    },
    methods:{
        dir_data:function(item){
            var self=this
            this.checked=[]
            this.depart_back_call([{fun:'dir_data',root:this.root,par:item}],function(resp){
                self.parents=resp.dir_data.parents
                self.items=resp.dir_data.items
            })
        },

        choice_me:function(item){
            this.$parent.callback(item)
            mainView.router.back()
        }
    },
    template:`
        <div class="scroll-wraper">
            <lay-tree-head :items="parents" @item_click="dir_data($event)"></lay-tree-head>
            <ul style="margin-left: 1em;font-size:1.1em;list-style:none;">
                <li v-for="item in items" style="padding: 0.4em;">
                    <span v-text="item._label" @click="dir_data(item)"></span>
                    <button style="float: right;margin-right: 1.5em;" @click="choice_me(item)">选择</button>
                </li>
            </ul>
        </div>
    `

}

Vue.component('com-depart-browser',depart)

//<ul style="margin-top: 0.3em;font-size: 1.3em;">
//    <li v-for="par in parents" @click="dir_data(par)" style="display: inline-block;">
//    <span v-text="par._label"></span>
//    <span style="display: inline-block;padding-left: 0.3em;padding-right: 0.3em;">
//    <i class="fa fa-angle-right" aria-hidden="true"></i>
//    </span>
//    </li>
//    </ul>