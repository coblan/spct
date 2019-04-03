




$.validator.config({
        rules: {
            two_valid_digit: [/^1$|^0$|^0\.[0-9]{0,2}$/, "请输入两位有效数字"],
            key_unique:function(elem, param) {
                //return /^1[3458]\d{9}$/.test($(elem).val()) || '请检查手机号格式';
                var keys = param
                var value = $(elem).val()
                if(!value) return true
                var rows = JSON.parse(value)
                var dc={}
                ex.each(keys,key=>{dc[key]=[]})
                for(var i=0;i<rows.length;i++){
                    var row = rows[i]
                    for(var j=0;j<keys.length;j++){
                        var key = keys[j]
                        if(ex.isin(row[key],dc[key])){
                            return  key+"重复了"
                        }else{
                            dc[key].push(row[key])
                        }
                    }
                }
                return true
            },
            group_unique:function(elem, param) {
                var keys = param
                var value = $(elem).val()
                if(!value) return true
                var rows = JSON.parse(value)
                var ls=[]
                for(var i=0;i<rows.length;i++){
                    var row = rows[i]
                    var group_value = ''
                    ex.each(keys,key=>{
                        group_value+= row[key]
                    })
                    if(ex.isin(group_value,ls)){
                        return  group_value+"重复了"
                    }else{
                        ls.push(group_value)
                    }
                }
                return true
            },
        }
    }
)