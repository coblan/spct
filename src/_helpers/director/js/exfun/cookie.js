/*
setCookie('name', 1111, 5);
setCookie('name1', 22222, 5);

console.log(getCookie('name'));
console.log(getAllCookie());

delCookie('name1');
clearCookie('undefined')    //清除未定义的名的cookie
*/
/*set cookie*/
export var cookie={
    setCookie:function (name, value, Days){
        if(Days == null || Days == ''){
            Days = 300;
        }
        var exp  = new Date();
        exp.setTime(exp.getTime() + Days*24*60*60*1000);
        document.cookie = name + "="+ escape (value) + "; path=/;expires=" + exp.toGMTString();
        //document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
    },

    /*get cookie*/
    getCookie:function (name) {
        var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
        if(arr=document.cookie.match(reg))
            return unescape(arr[2]);
        else
            return null;
    },

    /*get all cookie*/
    getAllCookie:function (){
        return document.cookie;
    },

    /* clear cookie*/
    clearCookie:function (name){
        setCookie(name, '', -1);
    },

    /* del cookie*/
    delCookie:function (name){
        var exp = new Date();
        exp.setTime(exp.getTime() - 1);
        var cval=getCookie(name);
        if(cval!=null)
            document.cookie= name + "="+cval+"; path=/;expires="+exp.toGMTString();
    }
}
