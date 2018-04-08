Vue.component('sort-mark',{
    props:['value','name'],
    data:function () {
        return {
            index:-1,
            sort_str:this.value,
        }
    },
    //mixins:[table_fun],
    template:`<span class='sort-mark'>
			<span v-if='index>0' v-text='index'></span>
			<img v-if='status=="up"' src='http://res.enjoyst.com/image/up_01.png'
					 @click='sort_str=toggle(sort_str,name);$emit("input",sort_str)'/>
			<img v-if='status=="down"' src='http://res.enjoyst.com/image/down_01.png'
					 @click='sort_str=toggle(sort_str,name);$emit("input",sort_str)'/>
			<img v-if='status!="no_sort"' src='http://res.enjoyst.com/image/cross.png'
					@click='sort_str=remove_sort(sort_str,name);$emit("input",sort_str)'/>
			</span>
	`,
    computed:{
        status:function () {
            var sorted=this.value.split(',')
            for(var x=0;x<sorted.length;x++){
                var org_name=sorted[x]
                if(org_name.startsWith('-')){
                    var name=org_name.slice(1)
                    var minus='up'
                }else{
                    var name=org_name
                    var minus='down'
                }
                if(name==this.name){
                    this.index=x+1
                    return minus
                }
            }
            return 'no_sort'
        }
    },
    methods:{
        remove_sort:function (sort_str,name) {
            var ls=ex.split(sort_str,',')
            ls=ex.filter(ls,function (v) {
                return v!='-'+name && v!=name
            })
            return ls.join(',')
        },
        toggle:function (sort_str,name) {
            var ls=ex.split(sort_str,',')
            var norm_ls=this.filter_minus(ls)
            var idx = norm_ls.indexOf(name)
            if(idx!=-1){
                ls[idx]=ls[idx].startsWith('-')?name:'-'+name
            }else{
                ls.push(name)
            }
            return ls.join(',')
        },
    }
    //methods:{

    //	get_status:function () {
    //		var sorted=this.sort_str.split(',')
    //		for(var x=0;x<sorted.length;x++){
    //			var org_name=sorted[x]
    //			if(org_name.startsWith('-')){
    //				var name=org_name.slice(1)
    //				var minus='up'
    //			}else{
    //				var name=org_name
    //				var minus='down'
    //			}
    //			if(name==this.name){
    //				this.index=x+1
    //				return minus
    //			}
    //		}
    //		return 'no_sort'
    //	}
    //}

})