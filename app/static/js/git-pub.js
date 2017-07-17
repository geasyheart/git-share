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
        var pathname = location.pathname;
        window.location = '/signin?next=' + pathname;
        // $("#userinfo-nav").addClass("hidden");
        // $("#show-login").removeClass("hidden");
        // $("#user-basic-info").addClass("hidden");

    }

}
function getNode() {
    $.getJSON("/api/node", null, listNode);
}
function listNode(data) {
    var nodes = data.node;
    for (var node of nodes) {
        var node_id = node.id;
        var node_name = node.node;
        $("#category").append("<option value=" + node_id + ">" + node_name + "</option>")
    }
}


function articlePub() {
    var title = $("#title").val();
    var content = editor.codemirror.getValue();
    var node = $("#category").val();
    var uid = getCookie("uid");
    if (!uid) {
        window.location = "/signin?next=/git-pub";
    } else {
        if (title.trim().length > 100 || title.trim().length == 0) {
            $("#pub-warn").text("题目:0<title<100!");
            return
        }
        if (content && content.trim().length > 10000) {
            $("#pub-warn").text("内容:content<10000!");
            return
        }
        var data = {
            title: title,
            content: content,
            node: node,
            login: 0 // 现在直接false
        };
        $.ajax({
            url: '/api/article',
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data.code != 0) {
                    $("#pub-warn").text(data.message);
                } else {
                    window.location = '/';

                }
            }
        })
    }
}


var editor = new Editor();
editor.render($(".editor")[0]);


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


$(function () {
    userInfo();
    getNode();
});

