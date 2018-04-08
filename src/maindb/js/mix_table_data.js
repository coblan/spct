var mix_table_data={
    methods: {
        search:function(){
            this.search_args._page=1
            this.get_data()
        },
        get_data: function () {
            this.data_getter(this)
        },
        get_page: function (page_number) {
            this.search_args._page = page_number
            this.get_data()
        },
        get_search_args: function () {
            return this.search_args
        },
        data_getter:function(){
            // 默认的 data_getter
            var self=this
            //var loader = layer.load(2);
            cfg.show_load()
            $.get(ex.appendSearch(this.search_args),function(resp){
                self.rows = resp.rows
                self.row_pages = resp.row_pages
                cfg.hide_load()
            })
        },
        clear: function () {
            this.rows = []
            this.row_pages = {}
        },

        del_selected:function(){
            var self=this
            layer.confirm('真的删除吗?', {icon: 3, title:'确认'}, function(index) {
                layer.close(index);
                var ss = layer.load(2);
                var post_data = [{fun: 'del_rows', rows: self.selected}]
                $.post('/d/ajax', JSON.stringify(post_data), function (resp) {
                    layer.close(ss)
                    ex.each(self.selected,function(item){
                        ex.remove(self.rows,item )
                    })
                    self.selected=[]
                    layer.msg('删除成功',{time:2000})
                })
            })
        },

        //del_item: function () {
        //    if (this.selected.length == 0) {
        //        return
        //    }
        //    var del_obj = {}
        //    for (var j = 0; j < this.selected.length; j++) {
        //        var pk = this.selected[j]
        //        for (var i = 0; i < this.rows.length; i++) {
        //            if (this.rows[i].pk.toString() == pk) {
        //                if (!del_obj[this.rows[i]._class]) {
        //                    del_obj[this.rows[i]._class] = []
        //                }
        //                del_obj[this.rows[i]._class].push(pk)
        //            }
        //        }
        //    }
        //    var out_str = ''
        //    for (var key in del_obj) {
        //        out_str += (key + ':' + del_obj[key].join(':') + ',')
        //    }
        //    location = ex.template("{engine_url}/del_rows?rows={rows}&next={next}", {
        //        engine_url: engine_url,
        //        rows: encodeURI(out_str),
        //        next: encodeURIComponent(location.href)
        //    })
        //},
        //goto_page: function (page) {
        //    this.search_args._page = page
        //    this.get_data()
        //},
        //add_new: function () {
        //    var url = ex.template('{engine_url}/{page}.edit/?next={next}', {
        //        engine_url: engine_url,
        //        page: page_name,
        //        next: encodeURIComponent(ex.appendSearch(location.pathname, search_args))
        //    })
        //    location = url
        //},
    }
}

window.mix_table_data = mix_table_data