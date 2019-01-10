if(window.jb_app){
    // android
}
else if (window.webkit &&window.webkit.messageHandlers && window.webkit.messageHandlers.get){
    // ios
    window.jb_app={
        get:function(key,url){
            var get_data= {key:key,url:url}
            window.webkit.messageHandlers.get.postMessage(get_data)
        },
        post:function(key,url,data){
            var post_data= {key:key,url:url,data:data}
            window.webkit.messageHandlers.post.postMessage(post_data)
        }
    }
}else{
    window.jb_app={
        get:function(key,url,mock_data){
            var rt_data= mock_data || {data:'顺利GET'}
            rt_data.key = key
            jb_js.dispatch(rt_data)
        },
        post:function(key,url,data,mock_data){
            var rt_data= mock_data || {data:'顺利POST'}
            rt_data.key = key
            jb_js.dispatch(rt_data)
        }
    }
}

var jb_js={
    get:function(url,callback,mock_data){
        var fun_key = _uuid()

        jb_js['_fun_'+fun_key]=callback
        window.jb_app.get(fun_key,url,mock_data)
    },
    post:function(url,data,callback,mock_data){
        var fun_key = _uuid()

        jb_js['_fun_'+fun_key]=callback
        window.jb_app.post(fun_key,url,data,mock_data)
    },
    dispatch:function(resp){
        //var resp= JSON.parse(resp_str)
        //cfg.showMsg('进入dispatch')

        var key = resp.key
        jb_js['_fun_'+key](resp)
        delete jb_js['_fun_'+key]
    }
}

window.jb_js=jb_js


function _uuid() {
    var d = Date.now();
    if (typeof performance !== 'undefined' && typeof performance.now === 'function'){
        d += performance.now(); //use high-precision timer if available
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
}