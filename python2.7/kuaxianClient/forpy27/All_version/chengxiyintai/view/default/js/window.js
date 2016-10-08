//var location=""
window.onload=function(){
	Drag.init();
	var content = $(".win-content");
	content.height(content.height()-20);//减去窗口标题的高度，避免出现滚动条
	var wType = _window_.getWindowType();
	var url = _window_.getUrl();
	reBg();
	// $("#main-iframe").attr("src",_window_.getUrl());

}

// function loadSubPage(par){
// 	var url = _window_.getUrl();
// 	if(url.indexOf("?")!=-1){
// 		url = url.substring(0,url.indexOf("?"));
// 	}
// 	url+=par;
// 	loadPage(url);
// }
function setTitle(title){
	$(".win-title-text").text(title);		
}
function hiddenSkinBtn(){
	$(".win-skin").hide();
}
function clearBg(){
	$(".main").css("background-image","none");
}
function reBg(){
	$(".win-skin").show();
	if(window.localStorage.skin)
		$(".main").css("background-image","url('"+window.localStorage.skin+"')");
}
function skinItem(){
	var si = $("#skin-item");
	if(si.is(":hidden")){
		si.show();
		skinItems = _window_.getSkinItem();
		$("#skin-item").html(skinItems);
		$("#skin-item ul img").click(function(){
			$(".main").css("background","url('"+this.src+"')");
			window.localStorage.skin=$(this).attr("src");
			si.hide();
		});
	}else{
		si.hide();
	}
}
function windowClose(){
	_window_.quit();
	event.stopPropagation();
}

function windowMin(){
	_window_.minimize();
	event.stopPropagation(); 
}

var Drag = {
	mouseDown:function(e){
		// 修复drag
		if($(e.target).attr('class') == 'skin-imgs'){
			Drag.isDraging = null;
		}else{
			Drag.isDraging = 1;
			Drag.x = e.screenX;
			Drag.y = e.screenY;
			e.preventDefault();
		}
	},
	mouseUp:function(e){
		Drag.isDraging = null;
		e.preventDefault();
	},
	mouseMove:function(e){
		if(Drag.isDraging){
			var offsetX = e.screenX-Drag.x;
			var offsetY = e.screenY-Drag.y;
			_window_.moveTo(offsetX,offsetY)
			Drag.x = e.screenX;
			Drag.y = e.screenY;
		}
		e.preventDefault();
	},
	init:function(){
		//var title = $(".win-title")[0];
		//if(typeof title == "undefined") return;
		document.onmousedown = Drag.mouseDown;
		document.onmouseup = Drag.mouseUp;
		document.onmousemove = Drag.mouseMove;
	}
};

