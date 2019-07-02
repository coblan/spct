




$.validator.config({
        rules: {
            two_valid_digit: [/^1$|^0$|^0\.[0-9]{0,2}$/, "请输入两位有效数字"],

            depend_check:function(elem, param) {
                var depend_value = $(`[name=${param}]`).prop('checked')
                var value = $(elem).prop('checked')

                if(value && !depend_value ){
                    return false
                }else{
                    return true
                }
            },
        }
    }
)