

export var table_fun={
    data:function(){

        if(table_fun_config.detail_link){
            heads.push({name:'_detail_link',label:''})
        }

        return {
            heads:heads,
            rows:rows,
            row_filters:row_filters,
            row_sort:row_sort,
            row_pages:row_pages,
            search_tip:search_tip,
            selected:[],
            del_info:[],
            menu:menu,

            can_add:can_add,
            can_del:can_del,
            can_edit:can_edit,

            search_args:ex.parseSearch(),
            ex:ex,
            help_url:help_url,
            page_label:page_label,
        }
    },
    watch:{
        'row_sort.sort_str':function (v) {
            this.search_args._sort=v
            this.search()
        }
    },
    methods:{
        goto:function(url){
            location=url
        },
        search:function () {
            location=ex.appendSearch(this.search_args)
            //location =ex.template('{path}{search}',{path:location.pathname,
            //    search: encodeURI(ex.searchfy(this.search_args,'?')) })
        },
        //rt_win:function(row){
        //    ln.rtWin(row)
        //},
        filter_minus:function (array) {
            // 移到 com-table 中去了
            return ex.map(array,function (v) {
                if(v.startsWith('-')){
                    return v.slice(1)
                }else{
                    return v
                }
            })
        },
        is_sorted:function (sort_str,name) {
            // 该函数被移到 com-table 中去了。
            var ls=sort_str.split(',')
            var norm_ls=this.filter_minus(ls)
            return ex.isin(name,norm_ls)
        },
        // 移到sort_mark
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
        //remove_sort:function (sort_str,name) {
        // 移到sort_mark.js 去了
        //    var ls=ex.split(sort_str,',')
        //    ls=ex.filter(ls,function (v) {
        //        return v!='-'+name && v!=name
        //    })
        //    return ls.join(',')
        //},
        map:function(name,row){
            if(name==this.heads[0].name && !table_fun_config.detail_link){
                return ex.template('<a href="{edit}?pk={pk}&next={next}">{text}</a>',
                    {
                        text: row[name],
                        edit: page_name + '.edit',
                        pk: row.pk,
                        next:encodeURIComponent(ex.appendSearch(location.pathname,search_args))
                    })
            }
            if(name=='_detail_link') {
                return ex.template('<a href="{edit}?pk={pk}&next={next}">{text}</a>',
                    {
                        text: table_fun_config.detail_link,
                        edit: page_name + '.edit',
                        pk: row.pk,
                        next:encodeURIComponent(ex.appendSearch(location.pathname,search_args))
                    })
            }
            if(row[name]===true){
                return '<img src="//res.enjoyst.com/true.png" width="15px" />'
            }else if(row[name]===false){
                return '<img src="//res.enjoyst.com/false.png" width="15px" />'
            }else{
                return row[name]
            }
        },
        form_link:function(name,row){
            return ex.template('<a href="{edit}?pk={pk}&next={next}">{value}</a>',
                {	edit:page_name+'.edit',
                    pk:row.pk,
                    next:encodeURIComponent(location.href),
                    value:row[name]
                })
        },

        del_item:function () {
            if (this.selected.length==0){
                return
            }
            var del_obj={}
            for(var j=0;j<this.selected.length;j++){
                var pk = this.selected[j]
                for(var i=0;i<this.rows.length;i++){
                    if(this.rows[i].pk.toString()==pk){
                        if(!del_obj[this.rows[i]._class]){
                            del_obj[this.rows[i]._class]=[]
                        }
                        del_obj[this.rows[i]._class].push(pk)
                    }
                }
            }
            var out_str=''
            for(var key in del_obj){
                out_str += (key+':'+ del_obj[key].join(':')+',')
            }
            location=ex.template("{engine_url}/del_rows?rows={rows}&next={next}",{engine_url:engine_url,
                rows:encodeURI(out_str),
                next:encodeURIComponent(location.href)})
        },
        goto_page:function (page) {
            this.search_args._page=page
            this.search()
        },
        add_new:function () {
            var  url = ex.template('{engine_url}/{page}.edit/?next={next}',{
                engine_url:engine_url,
                page:page_name,
                next:encodeURIComponent(ex.appendSearch(location.pathname,search_args))
            })
            location = url
        },
    },

}

window.table_fun = table_fun