function dispatch() {
    var keyword = $("#search-keyword").val();
    if (keyword != "") {
        var url = 'https://www.google.com/search?q=site:git-share.com/t%20' + keyword;
        window.open(url, "_black");
        return false;
    }
    return false;
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function userInfo() {
    var uid = getCookie("uid");
    if(uid) {
        var userinfo = localStorage.getItem("userinfo");
        if (userinfo) {
            var payload = JSON.parse(userinfo);
            var avatar = payload.avatar;
            var github = payload.github;
            var nickname = payload.nickname;
            $("#login-nav").addClass("hidden");
            $("#userinfo").text(nickname);
            $('.basic-info img').attr('src', avatar);
            $("#name").append("<a href='/settings'>" + nickname + "</a>");
            if (github) {
                $("#github").text(github)
            } else {
                $("#github").append("<a href='/settings'>设置Github地址!</a>")
            }


        } else {
            $.getJSON("/api/user/" + parseInt(uid), null, function (data) {
                localStorage.setItem("userinfo", JSON.stringify(data));
                location.reload();
            })
        }
    }else{
            // $("#userinfo-nav").addClass("hidden");
            // $("#show-login").removeClass("hidden");
            // $("#user-basic-info").addClass("hidden");
            var pathname = location.pathname;
            window.location = '/signin?next=' + pathname;
    }
}

function getTime(timestamp) {
    var now = Date.parse(new Date()) / 1000;
    var seconds = now - timestamp;
    var dt;
    if (seconds < 60) {
        dt = seconds + "秒前"
    } else if (seconds < 3600) {
        dt = Math.round(seconds / 60) + "分钟前"
    } else if (seconds < 86400) {
        dt = Math.round(seconds / 3600) + "小时前"
    } else {
        dt = Math.round(seconds / 86400) + "天前"
    }
    return dt
}


function getNotification(status) {
    var uid  = getCookie("uid");
    if (!uid) {
        window.location = "/";
    }
    if (status == 0) {
        //未读消息
        $.getJSON("/api/message", {page: 1, status: 1}, listNotification)
    } else {
        //已读消息
        $.getJSON("/api/message", {page: 1, status: 2}, listNotification)
    }
}

function listNotification(data) {
    var notification = data.notification;
    $(".message-body ul li").each(function () {
        this.remove()
    });

    for (var nf of notification) {
        var desc = nf.desc;
        var from = nf.from;
        var id = nf.id;
        var status = nf.status;
        var time = getTime(nf.time);
        var title = nf.title;
        var to = nf.to;
        var url = nf.url;
        var uid = from.uid;
        var nickname = from.nickname;
        $(".message-body ul").append('<li class="li-cell"> \
                        <div class="li-head"> \
                            <span><a href="' + url + '">' + title + '</a>中<a href="/user/' + uid + '">' + nickname + '</a>回复了您:</span> \
                            <span data-id="' + id + '" onclick="deleteNotification(this)">删除</span> \
                            <span data-id="' + id + '" onclick="modifyNotification(this)">已读</span> \
                            <span>' + time + '</span> \
                        </div> \
                        <div class="li-body">' + marked(desc) + '</div> \
                    </li>')
    }
}
function modifyNotification(e) {
    var mid = $(e).attr('data-id');
    var uid = getCookie("uid");
    if (!uid) {
        window.location = "/";
    }
    $.ajax({
        url: '/api/message/' + mid,
        data: {status: 2},
        type: 'put',
        dataType: 'json',
        success: function (data) {
            if (data.code == 403) {
                window.location = "/signin";
            } else {
                if (data.code != 0) {
                    alert(data.message);
                } else {
                    getNotification(0);
                }
            }
        }
    })
}

function deleteNotification(e) {
    var mid = $(e).attr('data-id');
    var uid = getCookie("uid");
    if (!uid) {
        window.location = "/";
    }
    $.ajax({
        url: '/api/message/' + mid,
        data: {status: 3},
        type: 'delete',
        dataType: 'json',
        success: function (data) {
            if (data.code == 403) {
                window.location = "/signin";
            } else {
                if (data.code != 0) {
                    alert(data.message);
                } else {
                    getNotification(1);
                }
            }
        }
    })

}
function linkPub() {
    window.location = '/git-pub';
}

function getHotArticle() {
    $.getJSON("/api/hot/article", null, listHotArticle);
}

function listHotArticle(data) {
    var articles = data.articles;
    var users = data.users;
    $(".hot-list li").each(function () {
        this.remove();
    });
    for (var article of articles) {

        var title = article.title;
        var article_id = article.id;
        var node = article.node;
        var url = "/article/" + node + "/" + article_id;
        $(".hot-list").append("<li><a href='" + url + "'>" + title + "</a></li>")
    }
}

$(function () {
    userInfo();
    getNotification(0);
    getHotArticle();
});