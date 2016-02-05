_config = {
    skip: 0,
    max: 20,
    timeout: 500,
    containerId: 'container',
    boxClass: 'box',
    loadingId: 'loading',
    imgDivId: 'big_img',
    coverId: 'cover',
    init: false,
}

// 实现类似 Python 的 format 操作
String.prototype.format = function(args) {
    var result = this;
    if (arguments.length < 1) {
        return result;
    }

    var data = arguments;
    if (arguments.length == 1 && typeof(args) == "object") {
        data = args;
    }
    for (var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replace("{" + key + "}", value);
        }
    }
    return result;
}

// 滚动事件
function scroll() {
    var document_scroll_top = $(document).scrollTop();
    var scroll_total = document_scroll_top + $(window).height();
    // 距离底部还剩 20px 的时候加载
    if (scroll_total >= $(document).height() - 20) {
        ajaxLoad();
        // 先解除绑定, 读取成功后重新绑定
        $(window).unbind('scroll', scroll);
    }
}

// 新建一个 box
function newBox(photo) {
    var box = document.createElement('div');
    var img = '<img class="thumb" src="{0}" alt="{1}" width="{2}" height="{3}" ori_width="{4}" ori_height="{5}">'.format(
        photo.thumb.url, photo.ori.url, photo.thumb.width, photo.thumb.height, photo.ori.width, photo.ori.height
    );
    box.setAttribute('class', _config.boxClass);
    $(box).append(img);
    return box;
}

// 解析拿到的数据
function parseData(data) {
    var ret_photos = [];
    photos = data.data.photos;
    for (var i = 0; i < photos.length; i++) {
        photo = photos[i];
        // 添加新的 box 到容器中
        var box = newBox(photo);
        if (_config.init) {
            $('#' + _config.containerId).append($(box)).masonry('appended', $(box), true);
        } else {
            $('#' + _config.containerId).append($(box));
        }
    }
}

// 异步读取
function ajaxLoad() {
    var url = 'http://4gun.net/api/v1/tumblr?uid=test&os=ios&max={0}&skip={1}'.format(
        _config.max, _config.skip)

    $.ajax({
        type: 'GET',
        data: {},
        url: url,
        dataType: 'json',
        beforeSend: function(){
            $("#" + _config.loadingId).show();
            return;
        },
        success: function(data){
            setTimeout(function() {
                parseData(data);
                initWaterfall();
                _config.skip += _config.max;
                $(window).bind('scroll', scroll);
            }, _config.timeout);
        },
        complete: function(){
            $("#" + _config.loadingId).hide();
            return;
        }
    });

}

// 初始化操作
function initWaterfall() {
    if (! _config.init) {
        var $container = $("#" + _config.containerId).masonry({
            itemSelector : '.' + _config.boxClass,
            gutterWidth : 20,
            isAnimated: true,
            isFitWidth: true,
        });
        _config.init = true;
    }
}

// 显示浮层
function showCover(url, img_width, img_height) {
    $(window).unbind('scroll', scroll);
    var screen_width = $(window).width();
    var screen_height = $(window).height();

    // 浮层的大小
    var cover = $('#' + _config.coverId);
    cover.css('width', $(document).width());
    cover.css('height', $(document).height());

    // 添加图片
    var img_div = $("#" + _config.imgDivId);
    var img = img_div.find('img');
    img.attr('src', url);

    // 调整大图的展现大小
    if (img_height > screen_height) {
        img_width = (screen_height / img_height) * img_width;
        img_height = screen_height;
    }
    if (img_width > screen_width) {
        img_height = (screen_width / img_width) * img_height;
        img_width = screen_width;
    }
    img_width *= 0.95;
    img_height *= 0.95;
    img.attr('width', img_width);
    img.attr('height', img_height);

    // 放在屏幕正中央
    img_div.css('left', Math.floor((screen_width - img_width) / 2));
    img_div.css('top', Math.floor((screen_height - img_height) / 2) + $(document).scrollTop());
    img_div.hide();
    cover.fadeIn(150, function(){
        img_div.fadeIn(300, function(){});
    });
}

// 隐藏浮层
function hideCover() {
    $('#' + _config.coverId).fadeOut(300, function(){
        $(window).bind('scroll', scroll);
    });

}

// 点击图片事件
function listenClick() {
    $("div").delegate("img", "click", function() {
        if (typeof $(this).attr('alt') != 'undefined') {
            var ori_img = $(this).attr('alt');
            var ori_width = $(this).attr('ori_width');
            var ori_height = $(this).attr('ori_height');
            showCover(ori_img, ori_width, ori_height);
        }
    });
}

$(document).ready(function(){
    hideCover();
    ajaxLoad();
    listenClick();
}).click(function(e) {
    e = e || window.event;
    if (e.target != $('#big_img')[0] && e.target == $('#mask')[0]) {
        hideCover();
    }
});
