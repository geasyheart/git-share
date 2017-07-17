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
            var nickname = payload.nickname;
            var avatar = payload.avatar;
            $("#login-nav").addClass("hidden");
            $("#userinfo").text(nickname);
            $('.basic-info img').attr('src', avatar);
            $("#name").text(nickname);

        } else {
            $.getJSON("/api/user/" + parseInt(uid), null, function (data) {
                localStorage.setItem("userinfo", JSON.stringify(data));
                location.reload();
            })
        }
    } else {
        $("#userinfo-nav").addClass("hidden");
        localStorage.removeItem("userinfo");
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

var handlerEmbed = function (captchaObj) {
    $("#signup").click(function (e) {
        var validate = captchaObj.getValidate();
        if (!validate) {
            $("#notice").css("display", "block");
            setTimeout(function () {
                $("#notice").css("display", "none");
            }, 2000);
            e.preventDefault();
        } else {
            var email = $("#email").val();
            var pwd = $("#pwd").val();
            var geetest_challenge = $("input[name='geetest_challenge']").val();
            var geetest_validate = $("input[name='geetest_validate']").val();
            var geetest_seccode = $("input[name='geetest_seccode']").val();
            var data = {
                email: email, pwd: pwd,
                geetest_challenge: geetest_challenge,
                geetest_validate: geetest_validate,
                geetest_seccode: geetest_seccode
            };
            $.ajax({
                url: "/api/signin",
                type: 'post',
                dataType: 'json',
                data: data,
                success: function (data) {
                    if (data.code != 0) {
                        $("#login-warn").text(data.message);
                    } else {
                        localStorage.setItem("userinfo", JSON.stringify(data.payload));
                        window.location = "/";

                    }
                }
            })
        }
    });
    // append相关的参数
    captchaObj.appendTo(".geetest_radar_tip");
    captchaObj.onReady(function () {
    });
};

function getGeetest() {
    $.ajax({
        url: "/api/geetest",
        type: "get",
        dataType: "json",
        success: function (data) {
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "embed",
                offline: !data.success
            }, handlerEmbed);
        }
    });
}

function bindGit() {
    $.getJSON("/api/oauth/github", null, function (data) {
        window.location = data.url;
    })

}

$(function () {
    getGeetest();
    userInfo();
});
