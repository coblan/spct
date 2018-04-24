var mix_v_table_adapter={

    mounted:function(){
        eventBus.$on('content_resize',this.resize)
    },
    computed:{
        columns:function(){
            var self=this
            var first_col={
                width: 60,
                titleAlign: 'center',
                columnAlign:'center',
                type: 'selection'
            }
            var cols=[first_col]
            var converted_heads =ex.map(this.heads,function(head){
                var col =ex.copy(head)
                var dc = {
                    field:head.name,
                    title:head.label,
                    isResize:true,
                }
                if (head.editor){
                    dc.componentName=head.editor
                }
                if(ex.isin(head.name,self.row_sort.sortable)){
                    dc.orderBy=''
                }
                ex.assign(col,dc)
                if(!col.width){
                    col.width=200
                }
                return col
            })
            cols = cols.concat(converted_heads)
            return cols
        }
    },
    methods:{
        resize:function(){
            var self=this
            $(self.$refs.vtable.$el).find('.v-table-rightview').css('width','100%')
            $(self.$refs.vtable.$el).find('.v-table-header').css('width','100%')
            $(self.$refs.vtable.$el).find('.v-table-body').css('width','100%')

            var tmid= setInterval(function(){
                self.$refs.vtable.resize()
            },50)
            setTimeout(function(){
                //self.$refs.vtable.resize()
                clearInterval(tmid)
            },600)

        },
        on_perpage_change:function(perpage){
            this.search_args._perpage=perpage
            this.search_args._page=1
            this.get_data()
        },
        sortChange(params){
            var self=this
            ex.each(this.row_sort.sortable,function(name){
                if(params[name]){
                    if(params[name]=='asc'){
                        self.search_args._sort=name
                    }else{
                        self.search_args._sort='-'+name
                    }
                    return 'break'
                }
            })
            this.get_data()
        },

    }
}
window.mix_v_table_adapter=mix_v_table_adapter