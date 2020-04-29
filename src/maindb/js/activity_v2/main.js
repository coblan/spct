import * as shou_cun from  './shou_cun.js'
import * as network from  './network.js'

cfg.showMsg = (msg,title)=>{
    //vant.Dialog.alert({
    //    title: title ||  '信息提示',
    //    message: msg,
    //})
    return MINT.MessageBox.alert(msg)
}
cfg.showError = (msg,title)=>{
    //vant.Dialog.alert({
    //    title: title ||  '错误提示',
    //    message: msg,
    //})
    return MINT.MessageBox.alert(msg)
}