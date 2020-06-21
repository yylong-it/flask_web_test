//用来更新用户的设置
$(document).ready(function () {

    //自动获取当前设置
    $.ajax({
        url:"/req_user_privacy?path=get_settings",
        type:'get',
        success:function(sets_msg){
            if(sets_msg == 'default')
                return;
            else{
                var sets = JSON.parse(sets_msg);
                if(sets.u_info == 1){
                    $("input[name='user_info'][value='show']").removeAttr('checked','checked');
                    $("input[name='user_info'][value='hide']").attr('checked','checked');
                }
                if(sets.u_comm == 1){
                    $("input[name='user_comm'][value='show']").removeAttr('checked','checked');
                    $("input[name='user_comm'][value='hide']").attr('checked','checked');
                }
                if(sets.u_good == 1){
                    $("input[name='user_good'][value='show']").removeAttr('checked','checked');
                    $("input[name='user_good'][value='hide']").attr('checked','checked');
                }
                if(sets.u_coll == 1){
                    $("input[name='user_coll'][value='show']").removeAttr('checked','checked');
                    $("input[name='user_coll'][value='hide']").attr('checked','checked');
                }
                if(sets.u_subs == 1){
                    $("input[name='user_subs'][value='show']").removeAttr('checked','checked');
                    $("input[name='user_subs'][value='hide']").attr('checked','checked');
                }
                if(sets.u_fans == 1){
                    $("input[name='user_fans'][value='show']").removeAttr('checked','checked');
                    $("input[name='user_fans'][value='hide']").attr('checked','checked');
                }
                if(sets.u_logs == 1){
                    $("input[name='user_logs'][value='show']").removeAttr('checked','checked');
                    $("input[name='user_logs'][value='hide']").attr('checked','checked');
                }
            }
        }
    });
    


    //个人信息的设置
    var old_info = $("input[name='user_info'][checked='checked']").val();
    console.log(old_info)
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

    //我的关注隐私设置
    var old_subs = $("input[name='user_subs']:checked").val();
    $("input[name='user_subs']").click(function () {
        var new_subs = $("input[name='user_subs']:checked").val();
        if (old_subs == new_subs) {
            $('#subs_msg').html("已是该选项");
        } else {
            console.log(new_subs);
            //异步请求更改设置
            $.ajax({
                url: '/req_user_privacy?path=u_subs',
                data: { 'new_subs': new_subs },
                type: "get",
                success: function (msg) {
                    $("#subs_msg").text(msg);
                    old_subs = new_subs;
                }
            });
        }
    });


    //我的粉丝隐私设置
    var old_fans = $("input[name='user_fans']:checked").val();
    $("input[name='user_fans']").click(function () {
        var new_fans = $("input[name='user_fans']:checked").val();
        if (old_fans == new_fans) {
            $('#fans_msg').html("已是该选项");
        } else {
            console.log(new_fans);
            //异步请求更改设置
            $.ajax({
                url: '/req_user_privacy?path=u_fans',
                data: { 'new_fans': new_fans },
                type: "get",
                success: function (msg) {
                    $("#fans_msg").text(msg);
                    old_fans = new_fans;
                }
            });
        }
    });


});