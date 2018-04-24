import * as myhistory from './myhistory.js'



var iframe_html=`
    <div class="navbar">
    <!-- Top Navbar-->
        <div class="navbar-inner">
            <div class="left"><a href="#" class="back link"> <i class="icon icon-back"></i><span>返回</span></a></div>
            <div class="center"><span style="color: #999999">加载...</span></div>
            <div class="right pop-menu" style="visibility: hidden;">
                <!-- Right link contains only icon - additional "icon-only" class-->
                <a href="#" class="link icon-only"> <i class="icon icon-bars"></i></a>
            </div>
        </div>
    </div>
    <div class="pages">
        <!-- Page, data-page contains page name-->
        <div data-page="{name}" class="page page-cus">
            <!-- Scrollable page content-->
            <div class="page-content iframe_content ">
                <div style="height: 100vh;width: 5vw;position: fixed;z-index: 9000;background: rgba(0,0,0,0);top:0;left: 0;"></div>
                <iframe class="iframe_wraper"  frameborder="0" width="100%" height="100%"></iframe>
            </div>
        </div>
    </div>`

function load_iframe(url,name,callback){
    show_load()
    var html = iframe_html

    html=ex.template(html,{name:name,url:url})
    mainView.router.loadContent(html)

    if(mainView.history.length>2){
        mainView.showNavbar()
    }else{
        // 在第二个页面，先隐藏住navbar，500毫秒后，再显示。
        mainView.hideNavbar()
        setTimeout(function(){
            mainView.showNavbar()
        },200)
    }
    setTimeout(function(){
        var last_iframe= $('.pages .page').last().find('.page-content.iframe_content iframe')
        last_iframe.attr('src',url)

        last_iframe.on('load',function(){
            hide_load(200)
            if(callback){
                // 把该回调传给 子frame ，子frame可以利用 window.ret 调用该回调。
                this.contentWindow.ret=function(node){return callback(node)}
            }
        })

    },300)

}


var input_vue_com_html=`
    <div class="navbar">
      <!-- Top Navbar-->
        <div class="navbar-inner">
            <div class="left"><a href="#" class="back link"> <i class="icon icon-back"></i><span>返回</span></a></div>
            <div class="center"><span style="color: #999999">加载...</span></div>
            <div class="right pop-menu" style="visibility: hidden;">
                <!-- Right link contains only icon - additional "icon-only" class-->
                <a href="#" class="link icon-only"> <i class="icon icon-bars"></i></a>
            </div>
        </div>
    </div>
    <div class="pages">
        <!-- Page, data-page contains page name-->
        <div data-page="{name}" class="page page-cus">
            <!-- Scrollable page content-->

            <div class="page-content vue_content">
                {com_html}
            </div>
        </div>
    </div>`

function load_vue_com(kw){
    /*
     kw={
     url:url string,
     com_html:html string,
     data:{},
     name:string,
     label:string,
     callback:function,
     }

     callback的使用方法：

     #在parent页面触发vue_com页面，
     load_vue_com({other:xxx,  callback:function(com_resp){
     dosomething(com_resp)
     }

     #在vue_com页面中，在返回parent页面时，要调用注册的回调函数。
     methods:{
     back:function(){
     this.$parent.callback(my_resp)
     mainView.router.back()
     }
     }

     * */

    var html = input_vue_com_html

    html=ex.template(html,{name:kw.name,com_html:kw.com_html})
    mainView.router.loadContent(html)

    if(mainView.history.length>2){
        mainView.showNavbar()
    }else{
        // 在第二个页面，先隐藏住navbar，500毫秒后，再显示。
        mainView.hideNavbar()
        setTimeout(function(){
            mainView.showNavbar()
        },200)
    }

    setTimeout(function(){
        ex.load_js(kw.url,function(){
            var el= $('.pages .page').last().find('.vue_content')[0]
            new Vue({
                el:el,
                data:kw.data,
                methods:{
                    callback:kw.callback
                }
            })
            set_title(kw.label)
        })
    },50)
}

function set_title(title){
    // 设置当前子页面的标题
    $('.navbar .navbar-inner:last-child .center').html(title)
}

function init_page(){
    window.state_stack=[]
    myhistory.enable_custom_history()
}

window.load_iframe=load_iframe
window.load_vue_com=load_vue_com
window.set_title=set_title
window.init_page=init_page