
$(document).ready(function () {

    //请求点赞状态,收藏状态
    var vid = $("#v_vid").text()
    var good_num = Number($('#good_num').text())
    var coll_num = Number($('#coll_num').text())
    var err_good = '', err_coll = '';

    $.ajax({
        url: "/ajax_vinfo",
        data: { "vid": vid },
        type: "post",
        async: false,
        success: function (err_code) {
            err_good = err_code['good']
            err_coll = err_code['coll']
            //查询出已点赞
            if (err_code['good'] == 'yes') {
                $("#good_img").attr("src", "../static/images/video/gooded.png");
                $("#good_img").attr("title", "取消点赞");

            } else {
                $("#good_img").attr("src", "../static/images/video/good.png");
                $("#good_img").attr("title", "喜欢就点赞吧");
            }

            //查询出已收藏
            if (err_code['coll'] == 'yes') {
                $("#coll_img").attr("src", "../static/images/video/colled.png");
                $("#coll_img").attr("title", "取消收藏");
            } else {
                $("#coll_img").attr("src", "../static/images/video/coll.png");
                $("#coll_img").attr("title", "喜欢就收藏吧");
            }
        }
    });

    $("#good_img").click(function () {

        //已点赞取消点赞
        if (err_good == 'yes') {
            var good_flag = confirm("确定取消点赞吗");
            if (good_flag == true) {
                $.ajax({
                    url: "/req_good_coll",
                    data: { 'vid': vid, 'req_stat': 'del_good' },
                    type: 'POST',
                    success: function (msg) {
                        alert(msg);
                        $("#good_img").attr("src", "../static/images/video/good.png");
                        $("#good_img").attr("title", "喜欢就点赞吧");
                    }
                })
            }
        }

        //查询出来未点赞(取消了点赞（存在记录），从未点赞（不存在记录）)，异步请求点赞
        if (err_good == 'no' || err_good == 'not_exist') {
            $.ajax({
                url: "/req_good_coll",
                data: { "vid": vid, "req_stat": "add_good", "log_exist": err_good },
                type: "POST",
                success: function (msg) {
                    alert(msg);
                    $("#good_img").attr("src", "../static/images/video/gooded.png");
                    $("#good_img").attr("title", "取消点赞");
                }
            });
        }

        //反复点赞，取消,需要更改err_good的值
        if (err_good == 'yes') {
            err_good = 'no';
            good_num = good_num - 1;
            $('#good_num').text(good_num);
        } else {
            err_good = 'yes';
            good_num = good_num + 1;
            $('#good_num').text(good_num);
        }
    });



    $("#coll_img").click(function () {

        //已收藏取消收藏
        if (err_coll == 'yes') {
            var coll_flag = confirm("是否取消收藏");
            if (coll_flag == true) {
                $.ajax({
                    url: "/req_good_coll",
                    data: { 'vid': vid, 'req_stat': 'del_coll' },
                    type: 'POST',
                    async: false,
                    success: function (msg) {
                        alert(msg);
                        $('#coll_num').text(coll_num - 1);
                        $("#coll_img").attr("src", "../static/images/video/coll.png");
                        $("#coll_img").attr("title", "喜欢就收藏吧");
                    }
                });
            } else {
                return;
            }

        }

        if (err_coll == 'no' || err_coll == 'not_exist') {
            $.ajax({
                url: "/req_good_coll",
                data: { 'vid': vid, 'req_stat': 'add_coll', 'log_exist': err_coll },
                type: "POST",
                async: false,
                success: function (msg) {
                    alert(msg);
                    $('#coll_num').text(coll_num + 1);
                    $("#coll_img").attr("src", "../static/images/video/colled.png");
                    $("#coll_img").attr("title", "取消收藏");
                }
            });
        }

        //在同一页面多次操作，需要更改err_coll的值(点击一次触发一次)
        if (err_coll == 'yes') {
            err_coll = 'no';
            coll_num = coll_num - 1;
            $('#coll_num').text(coll_num);
        } else {
            err_coll = 'yes';
            coll_num = coll_num + 1;
            $('#coll_num').text(coll_num);
        }

    });

});

$(document).ready(function () {


    //ajax请求是否订阅
    var up_name = $("#uname_a").text();
    var up_id = $("#u_id").text();
    $.ajax({
        url: "/req_subs_fans",
        data: { 'uid': up_id, 'type': 'getsub_stat' },
        type: 'get',
        success: function (err_code) {
            if (err_code == 'unlogin' || err_code == 'unsub') {
                $('#sub_hidden').attr('value', 'unsub');
            } else if (err_code == 'sub') {
                $('#sub').attr('src', '../static/images/video/subed.png');
                $('#sub').attr('title', '已订阅');
                $('#sub_hidden').attr('value', 'sub')
            } else if (err_code == 'usedsub') {
                $('#sub_hidden').attr('value', 'usedsub')
            } else {
                return;
            }
            console.log($('#sub_hidden').val());
        }
    });


    //点击订阅
    $('#sub').click(function () {
        var sub_stat = $('#sub_hidden').val();
        var req_type = '';
        //如果未订阅
        if (sub_stat == 'unsub' || sub_stat == 'usedsub') {
            req_type = 'reqsub';
            $.ajax({
                url: '/req_subs_fans',
                data: { 'uid': up_id, 'uname': up_name, 'sub_stat': sub_stat, 'type': req_type },
                type: 'get',
                success: function (msg) {
                    alert(msg);
                    $('#sub').attr('src', '../static/images/video/subed.png');
                }
            });
        }

        if (sub_stat == 'sub') {
            //取消订阅
            req_type = 'delsub';
            del_flag = confirm('确定取消订阅吗？');
            if (del_flag == true) {
                $.ajax({
                    url: '/req_subs_fans',
                    data: { 'uid': up_id, 'type': req_type },
                    type: 'get',
                    success: function (msg) {
                        alert(msg);
                        $('#sub').attr('src', '../static/images/video/sub.png');
                    }
                });
            } else {
                return;
            }

        }

        //操作完之后更改sub_stat的value
        if(sub_stat == 'unsub' || sub_stat == 'usedsub'){
            $('#sub_hidden').attr('value','sub');
        }else{
            $('#sub_hidden').attr('value','usedsub');
        }
    });

});