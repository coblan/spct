
//function para_encode(para_str){
//    return encodeURI(para_str).replace('+','%2B')
//}

export var old={

    /*两种调用方式
     var template1="我是{0}，今年{1}了";
     var template2="我是{name}，今年{age}了";
     var result1=template1.format("loogn",22);
     var result2=template2.format({name:"loogn",age:22});
     两个结果都是"我是loogn，今年22了"
     */
    template:function (string,args) {
        var result = string;
        if(args.length){
            for (var i = 0; i < args.length; i++) {
                if (args[i] != undefined) {
                    //var reg = new RegExp("({[" + i + "]})", "g");//这个在索引大于9时会有问题，谢谢何以笙箫的指出
                    var reg= new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, args[i]);
                }
            }
        }else{
            for (var key in args) {
                var value= args[key]
                if(value==undefined){
                    value=''
                }

                var reg = new RegExp("({" + key + "})", "g");
                result = result.replace(reg, value);

            }
        }
        return result;
    },
    /*
     ex.merge([{name:'dog',age:'18'}],[{name:'dog',label:'dog_label'}])
     >> [{name:'dog',age:'18',label:'dog_label'}]
     */
    merge:function (src1,src2) {
        var self=this
        var dst_list=JSON.parse(JSON.stringify(src1))
        this.each(src2,function (src_item) {
            var obj = self.findone(dst_list,{name:src_item.name})
            if(obj){
                self.assign(obj,src_item)
            }else{
                dst_list.push(src_item)
            }
        })
        return dst_list
    },
    product:function (src1,src2) {
        var out=[]
        for(var i=0;i<src1.length;i++){
            for(var j=0;j<src2.length;j++){
                out.push([src1[i],src2[j]])
            }
        }
        return out
    },
    copy:function (obj) {
        return JSON.parse(JSON.stringify(obj))
    },

    split:function (base_str,sep) {
        if(base_str==''){
            return []
        }else{
            return base_str.split(sep)
        }
    },


    append_css:function(styles_str){
        /*
         * @styles_str : css string or <style>css string</style>
         * */
        window._appended_css=window._appended_css || []
        if(ex.isin(styles_str,window._appended_css)){
            return
        }else{
            window._appended_css.push(styles_str)
        }
        var mt = /<style.*>([\s\S]*)<\/style>/im.exec(styles_str)
        if(mt){
            styles_str=mt[1]
        }
        var style = document.createElement('style');

        //这里最好给ie设置下面的属性
        /*if (isIE()) {
         style.type = “text/css”;
         style.media = “screen”
         }*/
        (document.getElementsByTagName('head')[0] || document.body).appendChild(style);
        if (style.styleSheet) { //for ie
            style.styleSheet.cssText = styles_str;
        } else {//for w3c
            style.appendChild(document.createTextNode(styles_str));
        }


        //function includeStyleElement(styles,styleId) {
        //
        //	if (document.getElementById(styleId)) {
        //		return
        //	}
        //	var style = document.createElement(“style”);
        //	style.id = styleId;
        //	//这里最好给ie设置下面的属性
        //	/*if (isIE()) {
        //	 style.type = “text/css”;
        //	 style.media = “screen”
        //	 }*/
        //	(document.getElementsByTagName(“head”)[0] || document.body).appendChild(style);
        //	if (style.styleSheet) { //for ie
        //		style.styleSheet.cssText = styles;
        //	} else {//for w3c
        //		style.appendChild(document.createTextNode(styles));
        //	}
        //}
        //var styles = “#div{background-color: #FF3300; color:#FFFFFF }”;
        //includeStyleElement(styles,”newstyle”);
    },

    is_fun:function (v) {
        return typeof v === "function"
    },

    show_msg:function(msg){
        alert(msg)
    },
    access : function(o, s) {
        s = s.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
        s = s.replace(/^\./, '');           // strip a leading dot
        var a = s.split('.');
        for (var i = 0, n = a.length; i < n; ++i) {
            var k = a[i];
            if (k in o) {
                o = o[k];
            } else {
                return;
            }
        }
        return o;
    },
    set:function(par,name,obj){
        name = name.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
        name = name.replace(/^\./, '');           // strip a leading dot
        var a = name.split('.');
        var o=par
        for (var i = 0; i < a.length-1; ++i) {
            var k = a[i];
            if (k in o) {
                o = o[k];
            } else {
                return null;
            }
        }
        o[a[a.length-1]]=obj
        return o;
    },
    tr:function(str){
        var gettext=window.gettext||function(x){return x}
        return gettext(str)
    },
    trList:function(strlist){
        // translate string list to a map object
        var gettext=window.gettext||function(x){return x}
        var map_obj={}
        ex.each(strlist,function(key){
            map_obj[key]=gettext(key)
        })
        return map_obj
    },
    unique: function(array){
        var res = [];
        var json = {};
        for(var i = 0; i < array.length; i++){
            if(!json[array[i]]){
                res.push(array[i]);
                json[array[i]] = 1;
            }
        }
        return res;
    },
    group_add:function(old_array,new_array,callback){
        var out_list=old_array.slice()
        var last_key=null
        var last_list= null
        ex.each(new_array,function(item){
            var key= callback(item)
            if(key!=last_key){
                var obj=ex.findone(out_list,function(old_item){
                    if(old_item.key==key){return true}
                    else {return false}
                })

                if(!obj){
                    last_list=  []
                    last_key=key
                    out_list.push({key:last_key,list:last_list})
                }else{
                    last_list=obj.list
                }
            }
            last_list.push(item)
        })
        return out_list
    }


}

//function parseSearch(queryString) {
//    var queryString = queryString || location.search
//    if(queryString.startsWith('?')){
//        var queryString=queryString.substring(1)
//    }
//    var params = {}
//    // Split into key/value pairs
//    var queries = queryString.split("&");
//    // Convert the array of strings into an object
//    for (var i = 0; i < queries.length; i++ ) {
//        var mt = /([^=]+?)=(.+)/.exec(queries[i])
//        params[mt[1]] = mt[2];
//    }
//    return params;
//}
//function searchfy(obj,pre){
//    var outstr=pre||''
//    for(x in obj){
//        if(obj[x]){
//            outstr+=x.toString()+'='+ obj[x].toString()+'&';
//        }
//
//    }
//    if(outstr.endsWith('&')){
//        return outstr.slice(0,-1)
//    }else{
//        return outstr
//    }
//
//}
//function update(dst_obj,src_obj) {
//    for(x in src_obj){
//        dst_obj[x]=src_obj[x]
//    }
//}




