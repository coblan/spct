
 export var ff={
     // 子iframe页面调用该对象方法，

    app:parent.myApp,
    push:function(obj){
        parent.state_stack.push(obj)
    },
    pop:function(){
        parent.state_stack.pop()
    },
    back:function(callback){
        // 在子frame中调用该函数，会向上一个frame注入“修改代码”。
        if(callback){
            var last_win= $(parent.mainView.activePage.fromPage.container).find('.iframe_wraper')[0].contentWindow
            callback(last_win)
        }
        parent.mainView.router.back()

        //parent.back(callback)
    },
    load:function(url,name,callback){
        // 利用iframe来加载页面。@url是地址，@name framework7页面名字
        var name=name.replace(/\./g,'_')
        parent.show_load()
        parent.load_iframe(url,name,callback)
    },
     load_vue_com:function(kw){
         parent.load_vue_com(kw)
     },
    replace:function(url){
        parent.show_load()
        parent.replace_iframe(url)
    },
    pop_menu:function(buttons){
        parent.pop_menu(buttons)
    },
    show_load:function(){
        parent.show_load()
    },
    hide_load:function(time){
        parent.hide_load(time)
    },
    init_page:function(str){
        ff.hide_load(200)
        var str= str || page_label
        //parent.init_page()
        parent.set_title(str)
    },
    show_nav:function(){
        parent.show_nav()
    },
    hide_nav:function(){
        parent.hide_nav()
    },
    add_nav:function(str){
        parent.add_nav(str)
    },
    alert:function(str){
        // 警告框
        parent.myApp.alert(str)
    },
    confirm:function(info,callback){
        // 弹出框，确认框
        parent.myApp.confirm(info, callback);
    },
    open_image:function(str){
        // 弹出框，显示图片
        var myPhotoBrowser = parent.myApp.photoBrowser({
            zoom: 400,
            photos: [str]
        });
        myPhotoBrowser.open(); // open photo browser
        ff.push(function(){
            myPhotoBrowser.close()
        })
    }

}

 // 当页面不在framework7的iframe内时，自动切换为下面的函数。例如，单独开发某个页面时。
if(!parent.myApp){
  ff={
        app:{
            actions:function(){
            }
        },
        push:function(obj){
        },
        pop:function(){
        },
        back:function(callback){
        },
        load:function(url,name){
            location=url
        },
        replace:function(url){
            location=url
        },
        pop_menu:function(buttons){
        },
        show_load:function(){
        },
        hide_load:function(time){
        },
        init_page:function(){
        },
        show_nav:function(){
        },
        hide_nav:function(){
        },
        add_nav:function(str){
        },
        alert:function(str){
            alert(str)
        },
        confirm:function(info,callback){
            confirm(info, callback);
        },
        open_image:function(str){
            alert(str)
        }
    }
}


// 下面这个类好像没有用过。初衷应该大概是：把wrap.html中的函数出去出来，放在该类中。
export  class F7Manager{
    constructor(app,mainView){
        this.app=app;
        this.mainView=mainView
        this.state_stack=[]
        this.load_timer=null
    }
    load_iframe (url,name){
        this.show_load()
        var html = this.get_template()
        html=ex.template(html,{name:name,url:url})
        this.mainView.router.loadContent(html)
        if(this.mainView.history.length>2){
            this.mainView.showNavbar()
        }else{
            // 在第二个页面，先隐藏住navbar，500毫秒后，再显示。
            this.mainView.hideNavbar()
            setTimeout(()=>{
                this.mainView.showNavbar()
            },200)
        }
        setTimeout(()=>{
            $('.pages .page').last().find('.page-content.iframe_content iframe').attr('src',url)
        },300)
    }
    get_template(){
        return `
        <div class="navbar">
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
                <div class="page-content iframe_content ">
                    <div style="height: 100vh;width: 5vw;position: fixed;z-index: 9000;background: rgba(0,0,0,0);top:0;left: 0;"></div>
                    <iframe class="iframe_wraper"  frameborder="0" width="100%" height="100%"></iframe>
                </div>
            </div>
        </div>`
    }
    set_title(title){
        $('.navbar .navbar-inner:last-child .center').html(title)
    }
    on_pop_menu(callback){
        $('.view .navbar .navbar-inner:last-child .pop-menu').css('visibility','visible')
        if(callback){
            $('.view .navbar .navbar-inner').last().find('.pop-menu')[0].onclick=callback
        }
    }
    back(callback){
        // 当form页面修改item数据后，返回回table页面时，需要更新table中对应item的数据
        if(callback){
            var last_win= $(this.mainView.activePage.fromPage.container).find('.iframe_wraper')[0].contentWindow
            callback(last_win)
        }
        this.mainView.router.back()
    }
    call_iframe(callback_name){
        var args=Array.prototype.slice.call(arguments)
        $('.page-on-center .iframe_wraper')[0].contentWindow[callback_name].apply(this,args.slice(1,args.length))
    }
     add_nav(str){
        $('.view .navbar .navbar-inner').last().after(str)
    }
     remove_nav(){
        $('.view .navbar .navbar-inner').last().remove()
    }

    mount_history(){

        this._add_history()
        window.addEventListener('popstate',  (e)=> {
            var state= e.state
            if(state.count<1){
                this._add_history()
            }
            if(this.state_stack.length<=0){
                this.mainView.router.back()
            }else{
                var real_state= this.state_stack.pop()
                if(typeof(real_state) === 'function'){
                    real_state()
                }
            }
            this.hide_load()
        }, false);
    }
    _add_history(){
        for(var i=0;i<3;i++){
            history.pushState({count:i},'')
        }
    }

     show_load(timeout){
        var timeout= timeout || 10*1000
        $('.general-loader').removeClass('hide')

        if(this.load_timer){
            clearTimeout(this.load_timer)
        }
         this.load_timer =setTimeout(function(){
            this.app.alert('请检查网络问题', '加载超时');
             this.hide_load()
        },timeout)
    }

     hide_load(time){
        if(this.load_timer){
            clearTimeout(this.load_timer)
            this.load_timer=null
        }
        var time= time || 20
        setTimeout(function(){
            $('.general-loader').addClass('hide')
        },time)
    }
}
