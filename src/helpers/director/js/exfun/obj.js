export var obj_control={
    isEmpty:function(obj){
        for(var k in obj){
            if(/^[^_]/.exec(k)){
                return false
            }
        }
        return true
    }
}