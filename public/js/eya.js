
//咿呀网全局使用功能 
//2012.7.14



$().ready(function(){
    //固定在顶部
    var _defautlTop = $("#navigator").offset().top;
    var _defautlLeft = $("#navigator").offset().left;
    var _position = $("#navigator").css('position');
    var _top = $("#navigator").css('top');
    var _left = $("#navigator").css('left');
    var _zIndex = $("#navigator").css('z-index');
    $(window).scroll(function(){
        if($(this).scrollTop() > _defautlTop){
            if($.browser.msie && $.browser.version=="6.0"){
                $("#navigator").css({'position':'absolute','top':eval(document.documentElement.scrollTop),'left':_defautlLeft,'z-index':99999});
                $("html,body").css({'background-image':'url(about:blank)','background-attachment':'fixed'});
            }else{
                $("#navigator").css({'position':'fixed','top':0,'left':_defautlLeft,'z-index':99999});
            }
        }else{
            $("#navigator").css({'position':_position,'top':_top,'left':_left,'z-index':_zIndex});
        }
    });
	
	//加入收藏
	$(".setfavorite").click(function(){
		var start = 1;
		$.post('/auth/favoritecounts',{'start':start},function(){},'json');	
		var ctrl = (navigator.userAgent.toLowerCase()).indexOf('mac') != -1 ? 'Command/Cmd': 'CTRL'; 
		if (document.all) { 
			window.external.addFavorite('http://www.eya.cc', 'e雅网-发现你最想要的东西'); 
		} else if (window.sidebar) { 
			window.sidebar.addPanel('e雅网-发现你最想要的东西', 'http://www.eya.cc', ""); 
		} else { 
			//您的浏览器不支持自动加收藏 请按ctrl+d加入收藏
			alert('您的浏览器不支持自动加收藏，请按 ctrl+d 加入收藏'); 
		}	
			return false; 
	});
	//淘宝好店铺收藏设置
	$(".shopfavorite").click(function(){
		var start = 1;
		$.post('/auth/favoritecounts',{'start':start},function(){},'json');	
		var ctrl = (navigator.userAgent.toLowerCase()).indexOf('mac') != -1 ? 'Command/Cmd': 'CTRL'; 
		if (document.all) { 
			window.external.addFavorite('http://eya.cc', '淘宝好店铺导航'); 
		} else if (window.sidebar) { 
			window.sidebar.addPanel('淘宝好店铺导航', 'http://eya.cc', ""); 
		} else { 
			//您的浏览器不支持自动加收藏 请按ctrl+d加入收藏
			alert('您的浏览器不支持自动加收藏，请按 ctrl+d 加入收藏'); 
		}	
			return false; 
	});
	
	//宝贝搜索
	$("a[class=tgsearch]").live('click',function(){
		slideTg();								   
	});
	$("#btnfilter").click(function(){
		var q = $("#q").val();
		gurl = 'q='+q;
		submitfilter(gurl);
		
	});
	$("html").die().live("keydown",function(event){
		var q = $("#q").val();
		gurl = 'q='+q;
		if(event.keyCode==13){     
			submitfilter(gurl);
        }
    }); 
	function submitfilter(url){
		setTimeout(function(){  
		   window.location.href = '/search/?' + url; 
		},0); 	
	}
	function slideTg(){
		$("#fosearch").slideToggle(300);
		$("#q").focus().select();
	}
	$('.pro').hover(function(){
		$(this).addClass('proh'); 
			},function(){
		$(this).removeClass('proh'); 
		}
	);
	//评论
	$("a[class=entercomment]").live('click',function(){
	    var csrf = $("#csrf").val();
		var content = $("#content").val();
		var face = $("#faceurl").attr("src");
		var message = $("#message").val();
		if(content != "写评论" && content !=""){
			$.post('/addcomment/',{'content':content,'face':face,'message':message,'csrfmiddlewaretoken':csrf},function(required){
				if(required.successful){
					 var str = $('<ul class="clearfix"><li style="margin-top:3px;"><img src="'+face+'" /></li><li style="margin-left:8px;"><p>刚刚</p><p>'+content+'</p></li></ul>');
					 $("#commentslist").append(str);
					 $("#content").val("");
				}
			},'json');	
		}
	});

	//自定义设置
	$("a[class=custom-b]").live('click',function(){
		var customset = 1;
		var csrf = $("#csrf").val();
		$.post('/custom/',{'customset':customset,'csrfmiddlewaretoken':csrf},function(required){
				if(required.successful){
					 $("#custom-tip").show();
					 window.setTimeout("window.location.reload();",1000); 
				}
		},'json');	
	});
	$("a[class=custom-s]").live('click',function(){
		var customset = 0;
		var csrf = $("#csrf").val();										 
		$.post('/custom/',{'customset':customset,'csrfmiddlewaretoken':csrf},function(required){
				if(required.successful){
					 $("#custom-tip").show();
					 window.setTimeout("window.location.reload();",1000); 
				}
		},'json');	
	});
});
