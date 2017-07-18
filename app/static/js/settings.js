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
                $("#github").append("<a href='"+github+"'>"+git_name+"</a>")
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
        // $("#userinfo-nav").addClass("hidden");
        // $("#show-login").removeClass("hidden");
        // $("#user-basic-info").addClass("hidden");
        var pathname = location.pathname;
        window.location = '/signin?next=' + pathname;
    }
}

function linkPub() {
    window.location = "/git-pub";
}


var avatars = ['/static/public/avatar/0.png', '/static/public/avatar/1.png', '/static/public/avatar/2.png', '/static/public/avatar/3.png', '/static/public/avatar/4.png', '/static/public/avatar/5.png', '/static/public/avatar/6.png', '/static/public/avatar/7.png', '/static/public/avatar/8.png', '/static/public/avatar/9.png', '/static/public/avatar/10.png', '/static/public/avatar/11.png', '/static/public/avatar/12.png', '/static/public/avatar/13.png', '/static/public/avatar/14.png', '/static/public/avatar/15.png', '/static/public/avatar/16.png', '/static/public/avatar/17.png', '/static/public/avatar/18.png', '/static/public/avatar/19.png', '/static/public/avatar/20.png', '/static/public/avatar/21.png', '/static/public/avatar/22.png', '/static/public/avatar/23.png', '/static/public/avatar/24.png', '/static/public/avatar/25.png', '/static/public/avatar/26.png', '/static/public/avatar/27.png', '/static/public/avatar/28.png', '/static/public/avatar/29.png', '/static/public/avatar/30.png', '/static/public/avatar/31.png', '/static/public/avatar/32.png', '/static/public/avatar/33.png', '/static/public/avatar/34.png', '/static/public/avatar/35.png', '/static/public/avatar/36.png', '/static/public/avatar/37.png', '/static/public/avatar/38.png', '/static/public/avatar/39.png', '/static/public/avatar/40.png', '/static/public/avatar/41.png', '/static/public/avatar/42.png', '/static/public/avatar/43.png', '/static/public/avatar/44.png', '/static/public/avatar/45.png', '/static/public/avatar/46.png', '/static/public/avatar/47.png', '/static/public/avatar/48.png'];

function prevAvatar() {
    var avatar = parseInt($("#avatar").attr("data-id")) - 1;
    if (avatar < 0) {
        $("#avatar").attr("src", avatars[avatars.length - 1])
        $("#avatar").attr("data-id", avatars.length - 1)
    } else {
        $("#avatar").attr("src", avatars[avatar])
        $("#avatar").attr("data-id", avatar)
    }
}
function nextAvatar() {
    var avatar = parseInt($("#avatar").attr("data-id")) + 1;
    if (avatar > (avatars.length - 1)) {
        $("#avatar").attr("src", avatars[0])
        $("#avatar").attr("data-id", 0)
    } else {
        $("#avatar").attr("src", avatars[avatar])
        $("#avatar").attr("data-id", avatar)
    }
}


function modifySettings() {
    var uid = getCookie("uid");
    if (!uid) {
        window.location = "/signin"
    } else {
        var nickname = $("#nickname").val();
        var github = $("#git").val();
        var avatar = $("#avatar").attr("src");
        var fp_btn = $("#div1").attr("class");
        var favorite_public = (fp_btn == "open1") ? 1 : 0;
        var data = {
            nickname: nickname,
            github: github,
            avatar: avatar,
            favorite_public: favorite_public
        };
        $.ajax({
            url: '/api/settings',
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data.code != 0) {
                    alert(data.message)
                } else {
                    var payload = data.payload;
                    localStorage.setItem("userinfo", JSON.stringify(payload))
                    alert("保存成功!");

                }
            }
        })
    }
}

$("#pwd").blur(function () {
    var pwd = $("#pwd").val();
    var p = new RegExp("^[a-zA-Z][a-zA-Z0-9_.!]{7,32}");
    if (!p.test(pwd)) {
        $("#pwd-warn").text("密码格式以字母开头,至少8位,最多32位!");
        setTimeout(function () {
            $("#pwd-warn").text("");
        }, 2000);
    }
});

function modifyPwd() {
    var cur_pwd = $("#cur-pwd").val();
    var pwd = $("#pwd").val();
    var data = {cur_pwd: cur_pwd, pwd: pwd};
    $.ajax({
        type: 'put',
        url: '/api/settings',
        data: data,
        dataType: 'json',
        success: function (data) {
            if (data.code != 0) {
                alert(data.message)
            } else {
                alert("修改成功!");
            }
        }
    })
}

function getUserinfo() {
    var uid = parseInt(getCookie("uid"));
    $.getJSON("/api/user/" + uid, null, function (data) {
        $("#nickname").val(data.nickname);
        $("#git").val(data.github);
        $("#avatar").attr("src", data.avatar);
        $("#avatar").attr("data-id", avatars.indexOf(data.avatar));
        var div2 = document.getElementById("div2");
        var div1 = document.getElementById("div1");
        if (data.fp) {
            div1.className = "open1";
            div2.className = "open2";

        } else {
            div1.className = "close1";
            div2.className = "close2";
        }
    })
}


function publicFavoriteBtn() {
    var div2 = document.getElementById("div2");
    var div1 = document.getElementById("div1");
    div2.onclick = function () {
        div1.className = (div1.className == "close1") ? "open1" : "close1";
        div2.className = (div2.className == "close2") ? "open2" : "close2";
    }
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

function checkGitBind() {
    $.getJSON("/api/oauth/github/bind", null, function (data) {
        if (data.code == 804) {
            $("#git-bind").removeClass("hidden");
        }
    })
}

function bindGit() {
    $.getJSON("/api/oauth/github", null, function (data) {
        window.location = data.url;
    })

}

$(function () {
    userInfo();
    getUserinfo();
    publicFavoriteBtn();
    getNewMessage();
    checkGitBind();
});