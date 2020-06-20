
$(document).ready(function(){


    //为每个分类添加聚焦失去焦点的方法

    $('#index_a').focus(function(){

        $("#index_img").attr("src","../static/images/index/first_paged.png");
    });

    $("#game_a").focus(function(){

        $("#game_img").attr("src","../static/images/index/gamed.png");
    });

    $("#food_a").focus(function(){
        
        $("#food_img").attr("src","../static/images/index/fooded.png");
    });

    $("#tech_a").focus(function(){

        $("#tech_img").attr("src","../static/images/index/technologyed.png");
    });

    $("#life_a").focus(function(){

        $("#life_img").attr("src","../static/images/index/lifed.png");
    });

    $("#rec_a").focus(function(){

        $("#rec_img").attr("src","../static/images/index/recreationed.png");
    });

    $(".a_sort").blur(function(){

        $("#index_img").attr("src","../static/images/index/first_page.png");    
    });

    $("#game_a").blur(function(){

        $("#game_img").attr("src","../static/images/index/game.png");
    });

    $("#food_a").blur(function(){

        $("#food_img").attr("src","../static/images/index/food.png");
    });

    $("#tech_a").blur(function(){

        $("#tech_img").attr("src","../static/images/index/technology.png");
    });

    $("#life_a").blur(function(){

        $("#life_img").attr("src","../static/images/index/life.png");
    });

    $("#rec_a").blur(function(){

        $("#rec_img").attr("src","../static/images/index/recreation.png");
    });
});
