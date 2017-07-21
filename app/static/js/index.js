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
                var git_split = github.split("/");
                var git_name = git_split[git_split.length - 1];
                $("#github").append("<a href='" + github + "'>" + git_name + "</a>")
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
        $("#reward").addClass("hidden");
        $("#git-pub").addClass("hidden");
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


function linkPub() {
    window.location = '/git-pub';
}

function getNode() {
    $.getJSON("/api/node", null, listNode)
}
var NODELIST = {};

function listNode(data) {
    var count = 0;
    for (var node of data.node) {
        count += 1;
        var node_id = node.id;
        var node_name = node.node;
        NODELIST[node_id] = node_name;
        if (count < 10) {
            $("#recommend").before("<a data-id='" + node_id + "' onclick='searchNode(this)'>" + node_name + "</a>");
        }
        $("#node-list").after("<span data-id='" + node_id + "' onclick='searchNode(this)'>" + node_name + "</span>")
    }
    orderBy();
}

var SEARCH = {
    node: null,
    order_by: '-pk',
    page: 1,
    per_page: 12
};

function getArticle(url) {
    var param = $.param(SEARCH);
    $.getJSON(url, param, listArticle)
}

function searchNode(e) {
    SEARCH.order_by = '-pk';
    SEARCH.page = 1;
    var node = e.getAttribute("data-id");
    SEARCH.node = node;
    getArticle("/api/article/node/" + node);
}

function orderBy(e) {
    if (e) {
        SEARCH.order_by = e.getAttribute("data-id");
    }
    if (SEARCH.node) {
        getArticle("/api/article/node/" + SEARCH.node);
    } else {
        getArticle("/api/article");
    }


}

function prevPage() {
    var page = SEARCH.page;
    if (page <= 1) {
        return
    } else {
        SEARCH.page -= 1;
        orderBy();
    }
}
function nextPage() {
    if ($(".cell").length < 1) {
        return
    } else {
        SEARCH.page += 1;
        orderBy();
    }
}

function recommend() {
    var uid = getCookie("uid");
    if (!uid) {
        alert("需要登录才会推荐哦！")
    } else {
        $(".page").addClass("hidden");
        $.getJSON("/api/recommend", null, function (data) {
            listArticle(data);
        })
    }
}


function listArticle(data) {
    var articles = data.articles;
    var users = data.users;
    $(".cell").each(function () {
        this.remove();
    });

    for (var article of articles) {
        var click = article.click;
        var comment = article.comment;
        var favorite = article.favorite;
        var id = article.id;
        var like = article.like;
        var login = article.login;
        var time = getTime(article.time);
        var node = article.node;
        var origin = (article.origin) ? "原创" : "转载";

        var node_name = NODELIST[node];
        var title = article.title;
        var who = article.who;
        for (user of users) {
            if (user.uid == who) {
                var user_id = user.uid;
                var nickname = user.nickname;
                var avatar = user.avatar;
            }
        }

        $("#article-list").append('<div class="cell" style="font-size: 12px"> \
                    <table width="100%" cellspacing="0" cellpadding="0" border="0"><tbody><tr>  \
                            <td valign="top" class="avatar" style="width:48px"> \
                                <a href="" class="dark"></a> \
                                <a href="/user/' + user_id + '"> \
                                    <img style="max-width: 48px; max-height: 48px;" alt="图片" \
                                         src="' + avatar + '"> \
                                </a> \
                            </td> \
                            <td valign="top" style="padding-left: 8px"> \
                                <div class="fr"> \
                                    <a href="" class="count_livid">' + click + '</a> \
                                </div> \
                                <div class="sep3"></div> \
                                <span class="item_title" style="color:#000"> \
                                <a href="/article/' + node + '/' + id + '">' + title + '</a> \
                            </span> \
                                <div class="sep5"></div> \
                                <span class="small fade"> \
                                <strong><a href="javascript:;" class="node">' + node_name + '</a></strong> • \
                                <strong> \
                                    <a href="/user/' + user_id + '" class="dark">' + nickname + '</a> \
                                </strong>•' + origin + '•' + time + '•' + favorite + '收藏•' + comment + '回复•' + like + '喜欢</span></td>  \
                        </tr> \
                        </tbody> \
                    </table> \
                </div>')
    }

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


function showFeedback() {
    $(".cover").css("display", "block");
    $(".window").css("display", "block");
    $(".cover").on('click', function () {
        $(".cover").css("display", "none");
        $(".window").css("display", "none");
    })

}


function feedback() {
    $(".cover").css("display", "none");
    $(".window").css("display", "none");
    var content = $("#feedback").val();
    $.ajax({
        url: '/api/feedback',
        type: 'post',
        data: {content: content},
        dataType: 'json',
        success: function (data) {
            if (data.code == 0) {
                alert("非常感谢您的反馈，我们会慎重考虑！")
            }
        }
    })
}

function getPermission() {
    if (window.Notification) {
        if (Notification.permission != "denied") {
            Notification.requestPermission();
        }
    }
}
function bindGit() {
    $.getJSON("/api/oauth/github", null, function (data) {
        window.location = data.url;
    })

}

$(function () {
    userInfo();
    getNode();
    getHotArticle();
    getPermission();
    getNewMessage();
});

