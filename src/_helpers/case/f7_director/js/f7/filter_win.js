import {popup_page} from './popup.js'

export  function open(callback){
    var timestamp= Date.now()
    var uniq_id='uniq_'+timestamp

    var callback= callback || function(search_args){
            location=ex.appendSearch(search_args)
        }
    var filter_logic={
        el:'#'+uniq_id,
        data:{
            row_filters:row_filters,
            search_args:search_args,
            search_tip:search_tip,
        },
        mixins:[popup_page],
        methods:{
            selector:function(){
                return '.popup-filter'
            },
            assure:function(){
                this.search()
                this.close()
            },
            search:function () {
                var self=this
                //setTimeout(function(){  // popup关闭时，会有向下的滑动动画，如果向下滑动的动画卡顿，可以把这行加上
                    callback(self.search_args)
                //},100)
            },
            close:function(){
                ff.pop()
                this.close_()
                $('#'+uniq_id).remove()
            },

        },
    }
    var mount_str=`<div class="filter-block" id="${uniq_id}">
        <div class="popup popup-filter">
            <div class="content-block">
                <com-filter :row_filters="row_filters" :search_args="search_args" :search_tip='search_tip'></com-filter>
            </div>
        </div>
        </div>`

    $('body').append(mount_str)

    setTimeout(function(){
        var filter_win = new Vue(filter_logic)
        Vue.nextTick(function(){
            filter_win.open()
        })
    })


}


