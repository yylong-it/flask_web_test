$(document).ready(function () {

    //校验用户名的格式合法性
    function check_uname_legal(uname) {
        var err_msg = "格式合法";
        if (uname.length < 3 || uname.length > 6) {
            err_msg = "长度为3-6个字符";
            return err_msg;
        } else {
            if (!uname.match(/^[\u4E00-\u9FA5a-zA-Z0-9]{3,6}$/)) {
                err_msg = "只能由汉字，数字，字母组成";
                return err_msg;
            }
        }
        return err_msg;
    }

    // jQuery ajax添加用户名重复性校验
    $('#regist_name').keyup(function () {
        var reg_name = $('#regist_name').val();

        //先做格式校验,格式校验通过在ajax重复性校验
        if (check_uname_legal(reg_name) == "格式合法") {

            $.ajax({
                url: '/uname_repeat_verify',
                data: { 'reg_name': reg_name },
                type: 'post',
                success: function (msg) {
                    $('#ver_uname_msg').text(msg);

                    if (msg == "验证通过") {
                        $('#ver_uname_msg').css("color", "green");

                        if ($('#sub').attr("disabled") == "disabled") {
                            $('#sub').removeAttr("disabled");
                        }
                    } else {
                        $('#ver_uname_msg').css("color", "red");
                        $('#sub').attr("disabled", true)
                    }
                }
            });
        } else {
            $('#ver_uname_msg').css("color", "red");
            $('#ver_uname_msg').text(check_uname_legal(reg_name));
        }
    });

    //校验密码的格式，并返回密码强度判断
    $("#regist_pass").keyup(function () {
        var reg_pass = $("#regist_pass").val();

        var pass_strong = "";

        //判断长度
        if (reg_pass.match(/[^a-zA-Z0-9]/)) {
            pass_strong = "密码只能由数字，大小写字母组成";
            $("#pass_msg").css({ "color": "red", "font-size": "楷体" });
            console.log("字符不合法");
        } else {
            if (reg_pass.length < 6 || reg_pass.length > 12) {
                pass_strong = "密码长度为6-12";
                $("#pass_msg").css({ "color": "red", "font-size": "楷体" });
                console.log("长度不合法");
            } else {
                //强度判断
                if (reg_pass.match(/(^[a-z]+$)|(^[0-9]+$)|(^[A-Z]+$)/g)) {
                    pass_strong = "密码强度过低";
                    $("#pass_msg").css({ "color": "#FF1717", "font-size": "楷体" });
                    console.log([pass_strong, reg_pass]);
                } else if (reg_pass.match(/(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])/)) {
                    pass_strong = "密码强度很高";
                    $("#pass_msg").css({ "color": "#00FF00", "font-size": "楷体" });
                    console.log([pass_strong, reg_pass]);
                } else {
                    pass_strong = "密码强度中等";
                    $("#pass_msg").css({ "color": "#FFFF35", "font-size": "楷体" });
                    console.log([pass_strong, reg_pass]);
                }
            }
        }

        $("#pass_msg").text(pass_strong);
    });
});