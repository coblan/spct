function cus_close(){
    window.opener=null;
    window.open('','_self');
    window.close();
}


var quit_ready=false
export function info_quit(){

    if(quit_ready){
        cus_close()
    }else{
        myApp.addNotification({
            title: 'warning',
            message: '再次点击退出应用程序!',
            hold:3000,
            closeIcon:false,
            additionalClass:'bottom_msg',
        });
        quit_ready=true

        setTimeout(function(){
            quit_ready=false
        },3000)
    }
}