var com_table={
    props: {
        has_check: {},
        heads: {},
        rows: {
            default: function () {
                return []
            }
        },
        map: {},
        row_sort: {
            default: function () {
                return {sort_str: '', sortable: []}
            }
        },
        value: {}
    } ,
    computed:{
        selected:{
            get:function(){
                return this.value
            },
            set:function(v){
                this.$emit('input',v)
            }
        }
    },
    watchs:{
        selected:function(v){
            this.$emit('input',v)
        }
    },
    methods:{
        m_map:function(name,row){
            if(this.map){
                return this.map(name,row)
            }else{
                return row[name]
            }
        },
        is_sorted:function (sort_str,name) {
            var ls=sort_str.split(',')
            var norm_ls=this.filter_minus(ls)
            return ex.isin(name,norm_ls)
        },
        filter_minus:function (array) {
            return ex.map(array,function (v) {
                if(v.startsWith('-')){
                    return v.slice(1)
                }else{
                    return v
                }
            })
        },
        is_sortable:function(name){
            return ex.isin(name,this.row_sort.sortable)
        },
        toggle:function (sort_str,name) {
            if(sort_str == name){
                return '-'+name
            }else {
                return name
            }
            //var ls=ex.split(sort_str,',')
            //var norm_ls=this.filter_minus(ls)
            //var idx = norm_ls.indexOf(name)
            //if(idx!=-1){
            //    ls[idx]=ls[idx].startsWith('-')?name:'-'+name
            //}else{
            //    ls.push(name)
            //}
            //return ls.join(',')
        },
        toggle_all:function(e){
            var checked = e.currentTarget.checked
            if(checked){
                this.selected=ex.map(this.rows,function(row){return row.pk})
            }else{
                this.selected=[]
            }
        }

    },
    template:`	<table data-toggle="table">
		<thead>
			<tr >
				<th style='width:50px' v-if='has_check'>
					<input type="checkbox" name="test" value="" @click="toggle_all($event)"/>
				</th>
				<th v-for='head in heads' :class='["td_"+head.name,{"selected":is_sorted(row_sort.sort_str ,head.name )}]'>
					<div v-if='is_sortable(head.name)'  class='clickable' style="white-space: nowrap;"
						@click='row_sort.sort_str = toggle( row_sort.sort_str,head.name)'>
						    <span v-text='head.label'></span>
						    <div style="font-size: 0.7em;display: inline-block;margin: 0 0.2em;">
                                <i :class='["fa fa-caret-up sortmark",{"sort-col":row_sort.sort_str==head.name}]' style="position: relative;top: 0.7em;"></i><br>
                                <i :class='["fa fa-caret-down sortmark",{"sort-col":row_sort.sort_str=="-"+head.name}]' class="fa fa-caret-down"></i>
						    </div>
					</div>
					<span v-else v-text='head.label'></span>
					<!--<sort-mark class='sort-mark' v-model='row_sort.sort_str' :name='head.name'></sort-mark>-->
				</th>
			</tr>
		</thead>
		<tbody>
			<tr v-for='row in rows'>
				<td v-if='has_check'>
					<input type="checkbox" name="test" :value="row" v-model='selected'/>
				</td>
				<td v-for='head in heads' :class='"td_"+head.name'>
				    <component v-if="head.type" :is="head.type" :name="head.name" :row="row"></component>
					<span v-else v-html='m_map(head.name,row)'></span>
				</td>
			</tr>
		</tbody>
	</table>`
}

Vue.component('com-table',com_table)