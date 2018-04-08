window.cfg={
    showMsg:function(msg){
        alert(msg)
    },
    tr:{
        'picture_size_excceed':'图片尺寸不能超过{maxsize}'
    },
    show_load:function(){
        this._loader_index = layer.load(1)
    },
    hide_load:function(delay){
        layer.close(this._loader_index)
        if(delay){
            layer.msg('操作成功',{time:delay})
        }
    }
}