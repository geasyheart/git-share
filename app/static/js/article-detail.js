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
        $("#reward").addClass("hidden");
        $("#git-pub").addClass("hidden");
        $(".reply-comment").addClass("hidden");
        $("#show-login2").removeClass("hidden");

    }
}

function getHotArticle() {
    $.getJSON("/api/hot/article", null, listHotArticle);
}
function listHotArticle(data) {
    var articles = data.articles;
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


function getArticle() {
    var url = "/api" + location.pathname;
    $.getJSON(url, null, listArticle)
}
function listArticle(data) {
    var click = data.click;
    var comment = data.comment;
    var content = data.content;
    var favorite = data.favorite;
    var id = data.id;
    var like = data.like;
    var login = data.login;
    var node = data.node;
    var time = getTime(data.time);
    var title = data.title;
    var avatar = data.avatar;
    var nickname = data.nickname;
    var uid = data.uid;
    var like_bool = data.like_bool;
    var favorite_bool = data.favorite_bool;

    $("#title").text(title);
    $(".article-body").html(marked(content));
    var cur_uid = getCookie("uid");
    if (cur_uid) {
        if (like_bool && favorite_bool) {
            $(".article-info").append('<span>时间:' + time + '•</span> \
                    <span>作者:<a href="/user/' + uid + '">' + nickname + '</a></span> \
                    <span>浏览:' + click + '•</span> \
                    <span>喜欢:' + like + '•</span> \
                    <span>收藏:' + favorite + '•</span> \
                    <span>评论:' + comment + '•</span> \
                    <span id="like" onclick="unLike(this)" data-id="' + id + '">取消点赞</span> \
                    <span id="favorite" onclick="unFavorite(this)" data-id="' + id + '">取消收藏</span>');
        } else if (!like_bool && favorite_bool) {
            $(".article-info").append('<span>时间:' + time + '•</span> \
                    <span>作者:<a href="/user/' + uid + '">' + nickname + '</a></span> \
                    <span>浏览:' + click + '•</span> \
                    <span>喜欢:' + like + '•</span> \
                    <span>收藏:' + favorite + '•</span> \
                    <span>评论:' + comment + '•</span> \
                    <span id="like"   onclick="like(this)" data-id="' + id + '">点赞</span> \
                    <span id="favorite" onclick="unFavorite(this)" data-id="' + id + '">取消收藏</span>');
        } else if (like_bool && !favorite_bool) {
            $(".article-info").append('<span>时间:' + time + '•</span> \
                    <span>作者:<a href="/user/' + uid + '">' + nickname + '</a></span> \
                    <span>浏览:' + click + '•</span> \
                    <span>喜欢:' + like + '•</span> \
                    <span>收藏:' + favorite + '•</span> \
                    <span>评论:' + comment + '•</span> \
                    <span id="like"    onclick="unLike(this)" data-id="' + id + '">取消点赞</span> \
                    <span id="favorite" onclick="favorite(this)" data-id="' + id + '">收藏</span>');
        } else {
            $(".article-info").append('<span>时间:' + time + '•</span> \
                    <span>作者:<a href="/user/' + uid + '">' + nickname + '</a></span> \
                    <span>浏览:' + click + '•</span> \
                    <span>喜欢:' + like + '•</span> \
                    <span>收藏:' + favorite + '•</span> \
                    <span>评论:' + comment + '•</span> \
                    <span id="like"    onclick="like(this)" data-id="' + id + '">点赞</span> \
                    <span id="favorite" onclick="favorite(this)" data-id="' + id + '">收藏</span>');
        }
    } else {
        $(".article-info").append('<span>时间:' + time + '•</span> \
                    <span>作者:<a href="/user/' + uid + '">' + nickname + '</a></span> \
                    <span>浏览:' + click + '•</span> \
                    <span>喜欢:' + like + '•</span> \
                    <span>收藏:' + favorite + '•</span> \
                    <span>评论:' + comment + '•</span> \
                    <span id="like" class="hidden" onclick="like(this)" data-id="' + id + '">点赞</span> \
                    <span id="favorite" class="hidden" onclick="favorite(this)" data-id="' + id + '">收藏</span>');
    }
}

function like(e) {
    var article_id = e.getAttribute("data-id");
    var uid = getCookie("uid");
    if (!uid) {
        window.location = '/signin?next=' + location.pathname;
        return;
    }
    $.ajax({
        url: '/api/like/article/' + article_id,
        type: 'post',
        success: function (data) {
            if (data.code != 0) {
                alert(data.message);
            } else {
                $("#like").text("取消点赞");
                $("#like").attr("onclick", "unLike(this)");
            }
        }
    })
}
function unLike(e) {
    var article_id = e.getAttribute("data-id");
    var uid = getCookie("uid");
    if (!uid) {
        window.location = '/signin';
        return;
    }
    $.ajax({
        url: '/api/like/article/' + article_id,
        type: 'delete',
        dataType: 'json',
        success: function (data) {
            if (data.code != 0) {
                alert(data.message);
            } else {
                $("#like").text("点赞");
                $("#like").attr("onclick", "like(this)");
            }
        }
    })
}

function favorite(e) {
    var article_id = e.getAttribute("data-id");
    var uid = getCookie("uid");
    if (!uid) {
        window.location = '/signin';
        return;
    }
    $.ajax({
        url: '/api/favorite/article/' + article_id,
        type: 'post',
        success: function (data) {
            if (data.code != 0) {
                alert(data.message);
            } else {
                $("#favorite").text("取消收藏");
                $("#favorite").attr("onclick", "unFavorite(this)");
            }
        }
    })
}


function unFavorite(e) {
    var article_id = e.getAttribute("data-id");
    var uid = getCookie("uid");
    if (!uid) {
        window.location = '/signin';
        return;
    }
    $.ajax({
        url: '/api/favorite/article/' + article_id,
        type: 'delete',
        success: function (data) {
            if (data.code != 0) {
                alert(data.message);
            } else {
                $("#favorite").text("收藏");
                $("#favorite").attr("onclick", "favorite(this)");
            }
        }
    })
}
function linkPub() {
    window.location = '/git-pub';
}

var editor = new Editor();
editor.render($(".editor")[0]);


// 评论
var at;
function addAt(e) {
    at = $(e).parent().children().eq(0).attr("data-id");
    var nickname = $(e).parent().children().eq(0).text();
    editor.codemirror.setValue("@" + nickname + " ");
    window.scrollTo(0, document.body.scrollHeight);

}


function newComment() {
    var path = location.pathname.split("/");
    var article_id = path[path.length - 1];
    var editor_content = editor.codemirror.getValue();
    var get_at = editor_content.match(/^@([a-zA-Z0-9]{1,}) /);
    var content = editor_content;
    if (get_at) {
        var at_nickname = get_at[1];
        var url = location.protocol + "//" + location.host + "/user/" + at;
        content = editor_content.replace(get_at[0], "[@" + at_nickname + " ](" + url + ")");

    }

    var uid = getCookie("uid");
    if (!uid) {
        window.location = '/signin';
        return;
    }
    if (content.length > 300) {
        alert("评论长度不能超过300!");
        return
    }
    $.ajax({
        url: '/api/comment/' + article_id,
        type: 'post',
        data: {at: at, content: content},
        dataType: 'json',

        success: function (data) {
            if (data.code != 0) {
                alert(data.message);
            } else {
                $(".comment table").each(function () {
                    this.remove()
                });
                editor.codemirror.setValue('');
                $(".list-more").attr('data-id', 2);
                getComment();

            }
        }
    })

}

function getComment(e) {
    var page;
    if (typeof(e) == "undefined") {
        page = 1;
    } else {
        if ($(".comment-table").length < 1) {
            alert("就这么多评论了~~");
            return
        } else {
            page = e.getAttribute('data-id');
            e.setAttribute('data-id', parseInt(page) + 1);
        }
    }
    var path = location.pathname.split("/");
    var article_id = path[path.length - 1];
    $.getJSON("/api/comment/" + article_id, {'page': page}, function (data) {
        var comments = data.comments;
        var users = data.users;
        if (comments.length == 0) {
            return
        }
        for (var comment of comments) {
            var content = comment.content;
            var floor = comment.floor;
            var rid = comment.rid;
            var self = comment.self;
            var uid = comment.uid;
            var id = comment.id;
            var time = getTime(comment.time);
            var userinfo;
            for (var user of users) {
                if (user.uid == uid) {
                    userinfo = user;
                }
            }
            if (self) {
                $(".comment").append('<table class="comment-table" data-id="' + id + '"> \
                    <tr> \
                        <td class="comment-table-td"> \
                            <img class="user-avatar" \
                                 src="' + userinfo.avatar + '" alt="pic"> \
                        </td> \
                        <td> \
                            <div class="comment-info"> \
                                <span data-id="' + uid + '" class="comment-span"><a class="reply-nickname" href="/user/' + uid + '">' + userinfo.nickname + '</a></span> \
                                <span class="comment-span">' + time + '</span> \
                                <span class="comment-span">第' + floor + '层</span>\
                                <span class="comment-span" data-id="' + id + '" onclick="deleteComment(this)">删除</span>\
                                <span onclick="addAt(this)" class="comment-reply"><img src="../../static/public/img/reply.png" alt=""></span> \
                            </div> \
                            <div class="reply-comment-content">' + marked(content) + '</div>\
                        </td> \
                    </tr> \
                </table>')
            } else {
                $(".comment").append('<table class="comment-table" data-id="' + id + '"> \
                    <tr> \
                        <td class="comment-table-td"> \
                            <img class="user-avatar" \
                                 src="' + userinfo.avatar + '" alt="pic"> \
                        </td> \
                        <td> \
                            <div class="comment-info"> \
                                <span data-id="' + uid + '" class="comment-span"><a class="reply-nickname" href="/user/' + uid + '">' + userinfo.nickname + '</a></span> \
                                <span class="comment-span">' + time + '</span> \
                                <span class="comment-span">第' + floor + '层</span>\
                                <span onclick="addAt(this)" class="comment-reply"><img src="../../static/public/img/reply.png" alt=""></span> \
                            </div> \
                            <div class="reply-comment-content">' + marked(content) + '</div>\
                        </td> \
                    </tr> \
                </table>')
            }
        }
    })
}

function deleteComment(e) {
    var comment_id = $(e).attr('data-id');
    var path = location.pathname.split("/");
    var article_id = path[path.length - 1];
    $.ajax({
        url: '/api/comment/' + article_id + '/' + comment_id,
        type: 'delete',
        dataType: 'json',
        success: function (data) {
            if (data.code != 0) {
                alert(data.message);
            } else {
                $(".comment table").each(function () {
                    this.remove()
                });
                $(".list-more").attr('data-id', 2);
                getComment();
            }
        }

    })
}

//获取message
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

function bindGit() {
    $.getJSON("/api/oauth/github", null, function (data) {
        window.location = data.url;
    })

}

$(function () {
    getArticle();
    userInfo();
    getHotArticle();
    getComment();
    getNewMessage();
});

