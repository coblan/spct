
import * as win from './win.js'

export function enable_custom_history(){
    var his = new HistoryManager()

}

class HistoryManager{
    constructor(){
        this.add_history()
        this.listen_event()
    }
     add_history(){
        for(var i=0;i<3;i++){
            history.pushState({count:i},'')
        }
    }
     listen_event(){
        window.addEventListener('popstate', function (e) {

            if(mainView.history.length==1 && state_stack.length==0){
                win.info_quit()
            }

            var state= e.state
            if(state.count<1){
                add_history()
            }
            if(state_stack.length<=0){
                //注意：state_stack只能用来记录“非跨越f7.load”的状态。
                mainView.router.back()
            }else{
                var real_state= state_stack.pop()
                if(typeof(real_state) === 'function'){
                    real_state()
                }
            }
            hide_load()

        }, false);
    }
}






