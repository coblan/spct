




$.validator.config({
        rules: {
            two_valid_digit: [/^1$|^0$|^0\.[0-9]{0,2}$/, "请输入两位有效数字"],
        }
    }
)