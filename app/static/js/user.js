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
    if (uid) {
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
    } else {
        $("#userinfo-nav").addClass("hidden");
        $("#show-login").removeClass("hidden");
        $("#user-basic-info").addClass("hidden");
    }
}
function dispatch() {
    var keyword = $("#search-keyword").val();
    if (keyword != "") {
        var url = 'https://www.google.com/search?q=site:git-share.com/t%20' + keyword;
        window.open(url, "_black");
        return false;
    }
    return false;
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


function getUserInfo() {
    var path = location.pathname.split('/');
    var uid = parseInt(path[path.length - 1]);
    $.getJSON("/api/user/" + uid, null, function (data) {
        $("#avatar").attr("src", data.avatar);
        $("#nickname").text(data.nickname)
        $("#git").text(data.github)
    })
}


function getFavorite() {
    var path = location.pathname.split('/');
    var uid = parseInt(path[path.length - 1]);
    $.getJSON("/api/favorite/user/" + uid, {page: 1, per_page: 10}, listFavorite)
}
function getArticle() {
    var path = location.pathname.split('/');
    var uid = parseInt(path[path.length - 1]);
    $.getJSON("/api/article/user/" + uid, {page: 1, per_page: 10}, function (data) {
        var articles = data.articles;
        var avatar = $("#avatar").attr("src");
        $("#article-list li").each(function () {
            this.remove()
        });
        for (var article of articles) {
            var id = article.id;
            var node = article.node;
            var time = getTime(article.time);
            var title = article.title;
            var link = "/article/" + node + "/" + id;
            $("#article-list").append('<li> \
                        <img src="' + avatar + '" alt=""> \
                        <span class="fs"> \
                        <a href="' + link + '">' + title + '</a> \
                        <span>' + time + '</span> \
                        </span> \
                    </li>')
        }
    })
}


function listFavorite(data) {
    if (data.code == 704) {
        $("#favorite-list").append("<li>用户设置了相关权限!</li>")
    } else {
        var favorite = data.favorite;
        $("#favorite-list li").each(function () {
            this.remove()
        });
        var avatar = $("#avatar").attr("src");
        for (var f of favorite) {
            var node = f.node;
            var rid = f.rid;
            var title = f.title;
            var time = getTime(f.time);
            var link = "/article/" + node + "/" + rid;

            $("#favorite-list").append('<li> \
                        <img src="' + avatar + '" alt=""> \
                        <span class="fs"> \
                        <a href="' + link + '">' + title + '</a> \
                        <span>' + time + '</span> \
                        </span> \
                    </li>')
        }
    }
}

var popNotice = function (title, body, icon) {
    if (Notification.permission == "granted") {
        var notification = new Notification(title, {
            body: body,
            icon: icon
        });

        notification.onclick = function () {
            notification.close();
            window.location = "/message";
        };
    }
};

//获取message
function getNewMessage() {
    var uid = getCookie("uid");
    if (uid) {
        $.getJSON("/api/message/new", null, function (data) {
            var count = data.count;
            var avatar = $(".basic-info img").attr("src");
            if (count != 0) {
                popNotice("未读消息", "您有" + count + "条消息!", avatar);
            }
        })
    }
}


$(function () {
    userInfo();
    getUserInfo();
    getFavorite();
    getArticle();
    getNewMessage();
});