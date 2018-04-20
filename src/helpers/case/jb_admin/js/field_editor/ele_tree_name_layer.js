var label_shower =  {
    props:['row','head'],
    methods:{
        handleCheckChange(data, checked, indeterminate) {
            console.log(data, checked, indeterminate);
            var ls =this.$refs.et.getCheckedKeys()
            ls =ex.filter(ls,function(itm){
                return itm!=undefined
            })
            this.row[this.head.name] = ls
        },
        handleNodeClick(data) {
            console.log(data);
        },
    },
    data:function(){
        return {
            selected:[1,2],
            data: [{
                label: '一级 1',
                children: [{
                    label: '二级 1-1',
                    children: [{
                        label: '三级 1-1-1',
                        pk:1
                    }]
                }]
            }, {
                label: '一级 2',
                children: [{
                    label: '二级 2-1',
                    children: [{
                        label: '三级 2-1-1',
                        pk:3
                    }]
                }, {
                    label: '二级 2-2',
                    children: [{
                        label: '三级 2-2-1'
                    }]
                }]
            }, {
                label: '一级 3',
                children: [{
                    label: '二级 3-1',
                    children: [{
                        label: '三级 3-1-1',
                        pk:2
                    }]
                }, {
                    label: '二级 3-2',
                    children: [{
                        label: '三级 3-2-1'
                    }]
                }]
            }],
            defaultProps: {
                children: 'children',
                label: 'label',
            }
        }
    },
    template:`<div>
        <el-tree ref="et" :data="head.options" :props="defaultProps"
             @node-click="handleNodeClick"
             show-checkbox
             @check-change="handleCheckChange"

             :default-checked-keys="row[head.name]"
             node-key="value"
    ></el-tree>
    </div>`,
    //default-expand-all
    computed:{
        label:function(){
            return this.row['_'+this.head.name+'_label']
        }
    }
}

Vue.component('com-field-ele-tree-name-layer',function(resolve,reject){
    ex.load_css('https://unpkg.com/element-ui/lib/theme-chalk/index.css')
    ex.load_js('https://unpkg.com/element-ui/lib/index.js',function(){
        resolve(label_shower)
    })
})