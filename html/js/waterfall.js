_config = {
    skip: 0,
    max: 20,
    timeout: 500,
    containerId: 'container',
    boxClass: 'box',
    loadingId: 'loading',
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
    var img = '<img src="{0}" alt="{1}" width="{2}" height="{3}">'.format(
        photo.thumb.url, photo.ori.url, photo.thumb.width, photo.thumb.height
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
        $('#' + _config.containerId).append($(box)).masonry('appended', $(box), true);
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
                _config.skip += _config.max;
                $(window).bind('scroll', scroll);
            }, _config.timeout);
        },
        complete: function(){
            $("#" + _config.loadingId).show();
            return;
        }
    });

}

// 初始化操作
function init() {
    var $container = $("#" + _config.containerId).masonry({
        itemSelector : '.' + _config.boxClass,
        gutterWidth : 20,
        isAnimated: true,
    });
    $(window).bind('scroll', scroll);
}


$(document).ready(function(){
    init();
    ajaxLoad();
});
