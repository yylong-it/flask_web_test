//用来更新用户的设置
$(document).ready(function () {

    //个人信息的设置
    var old_info = $("input[name='user_info']:checked").val();
    $("input[name='user_info']").click(function () {
        var new_info = $("input[name='user_info']:checked").val();
        if (old_info == new_info) {
            $('#info_msg').html("已是该选项");
        } else {
            console.log(new_info);
            //异步请求更改设置
            $.ajax({
                url: '/req_user_privacy?path=u_info',
                data: { 'new_info': new_info },
                type: "get",
                success: function (msg) {
                    $("#info_msg").text(msg);
                    old_info = new_info;
                }
            });
        }
    });

    //我的评论隐私设置
    var old_comm = $("input[name='user_comm']:checked").val();
    $("input[name='user_comm']").click(function () {
        var new_comm = $("input[name='user_comm']:checked").val();
        if (old_comm == new_comm) {
            $('#comm_msg').html("已是该选项");
        } else {
            console.log(new_comm);
            //异步请求更改设置
            $.ajax({
                url: '/req_user_privacy?path=u_comm',
                data: { 'new_comm': new_comm },
                type: "get",
                success: function (msg) {
                    $("#comm_msg").text(msg);
                    old_comm = new_comm;
                }
            });
        }
    });

    //我的点赞隐私设置
    var old_good = $("input[name='user_good']:checked").val();
    $("input[name='user_good']").click(function () {
        var new_good = $("input[name='user_good']:checked").val();
        if (old_good == new_good) {
            $('#good_msg').html("已是该选项");
        } else {
            console.log(new_good);
            //异步请求更改设置
            $.ajax({
                url: '/req_user_privacy?path=u_good',
                data: { 'new_good': new_good },
                type: "get",
                success: function (msg) {
                    $("#good_msg").text(msg);
                    old_good = new_good;
                }
            });
        }
    });


    //我的收藏隐私设置
    var old_coll = $("input[name='user_coll']:checked").val();
    $("input[name='user_coll']").click(function () {
        var new_coll = $("input[name='user_coll']:checked").val();
        if (old_coll == new_coll) {
            $('#coll_msg').html("已是该选项");
        } else {
            console.log(new_coll);
            //异步请求更改设置
            $.ajax({
                url: '/req_user_privacy?path=u_coll',
                data: { 'new_coll': new_coll },
                type: "get",
                success: function (msg) {
                    $("#coll_msg").text(msg);
                    old_coll = new_coll;
                }
            });
        }
    });


});