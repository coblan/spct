var com_select = {
    props:['head','search_args','config'],
    template:`<select v-model='search_args[head.name]' class="form-control input-sm" >
        <option :value="undefined" v-text='head.label'></option>
        <option :value="null" disabled >---</option>
        <option v-for='option in orderBy( head.options,"label")' :value="option.value" v-text='option.label'></option>
    </select>
    `,
    data:function(){
        var inn_cfg = {
            sort:true
        }
        ex.assign(inn_cfg,this.config)
        return {
            cfg:inn_cfg
        }
    },
    watch:{
        myvalue:function(v){
            this.$emit('input',v)
        }
    },
    methods:{
        orderBy:function (array,key) {
            if(! this.cfg.sort){
                return array
            }else{
                return  array.slice().sort(function (a,b) {
                    if(isChinese(a[key])&&isChinese(b[key])){
                        return a[key].localeCompare(b[key],'zh')
                    }else{
                        return compare(a[key],b[key])
                    }
                })
            }

        },
    }
}
Vue.component('com-select-filter',com_select)

function isChinese(temp){
    var re=/[^\u4E00-\u9FA5]/;
    if (re.test(temp[0])){return false  ;}
    return true ;
}
function compare(temp1, temp2) {
    if (temp1 < temp2) {
        return -1;
    } else if (temp1 == temp2) {
        return 0;
    } else {
        return 1;
    }
}
