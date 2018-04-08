var com_table_btn={
    data:function(){
        return {
            can_add:can_add,
            can_del:can_del,
        }
    },
    props:['add_new','del_item','table_bus'],
    template:`<div class='btn-group'>
            <slot></slot>
			<button type="button" class="btn btn-success btn-sm" @click='add_new()' v-if='can_add'>创建</button>
			<button type="button" class="btn btn-danger btn-sm" @click='del_item()' v-if='can_del' :disabled="table_bus.selected.length==0">删除</button>

		</div>`
}

Vue.component('com-table-btn',com_table_btn)