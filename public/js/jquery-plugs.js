
 $(window).scroll(function(){
        if ($.browser.version!=='6.0'){
            if($(document).scrollTop() > 300)
                $("#go-top").slideDown("slow");
            else
                $("#go-top").slideUp("slow");
        }
    });

    $("#go-top").click(function(){
        var go = function(){
            var h = $(window).scrollTop();
            h -= Math.ceil(h * 15 / 100);
            if(h < 5) h = 0;
            $("html, body").scrollTop(h);
            if(h == 0) clearInterval(timer);
        };
        var timer = setInterval(go, 10);
        
    });
