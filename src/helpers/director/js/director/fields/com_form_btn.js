Vue.component('com-form-btn',{
    data:function(){
        return {
            can_add:can_add,
            can_del:can_del,
        }
    },
    props:['form_bus'],
    computed:{
        del_link:function(){
            return this.form_bus.del_row()
        }
    },
    //template:`<div style='overflow: hidden;'>
	//	<div class="btn-group" style='float: right;'>
	//		<button type="button" class="btn btn-default" @click='submit()' v-if='can_add'>保存</button>
	//		<a type="button" class="btn btn-default" v-if='can_del &&del_link' :href='del_link'>删除</a>
	//		<button type="button" class="btn btn-default" @click='cancel()' >取消</button>
	//	</div>
	//</div>`
    template:`<div style="min-height: 1.5em;">
    <div style="float: right;">
        <div class="btn-group">
            <button type="button" class="btn btn-success btn-sm" @click='form_bus.submit_return()' v-if='can_add'>保存并返回</button>
            <button type="button" class="btn btn-default btn-sm" @click='form_bus.submit()' v-if='can_add'>保存</button>
            <button type="button" class="btn btn-default btn-sm" @click='form_bus.goto_next()' >取消</button>
        </div>
        <!--<div class="btn-group" >-->
          <!--<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">-->
                <!--其他 <span class="caret"></span>-->
              <!--</button>-->
              <!--<ul class="dropdown-menu">-->
                <!--&lt;!&ndash;<li><a href="#" @click='form_bus.submit()' v-if='can_add'>保存</a></li>&ndash;&gt;-->
                <!--<li><a v-if='can_del &&del_link' :href='form_bus.del_row()'>删除</a></li>-->

                <!--&lt;!&ndash;<li role="separator" class="divider"></li>&ndash;&gt;-->
              <!--</ul>-->
        <!--</div>-->
    </div>

</div>`
})