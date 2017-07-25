define({ "api": [
  {
    "version": "1.0.0",
    "type": "post",
    "url": "/api/feedback",
    "title": "反馈",
    "name": "FeedbackApi",
    "group": "Feedback",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "content",
            "description": "<p>反馈内容</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      }
    },
    "filename": "app/modules/feedback/apis.py",
    "groupTitle": "Feedback",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/repos/:username",
    "title": "获取github此<username>的所有公开的repos",
    "name": "GitSpiderApi",
    "group": "GitSpider",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>github用户名字</p>"
          }
        ]
      }
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "GitSpider"
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/oauth/github",
    "title": "请求用户授权",
    "name": "GitAuthApi",
    "group": "Oauth_Github",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"url\": \"http://github.com/login/oauth/authorize?client_id=0427a878cffd69c57d24&redirect_uri=http://www.git-share.com/api/oauth/github/callback&scope=user&state=HVU3w1CXGNYzA7EtgjFP90h2dDBoyR\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/oauth/github.py",
    "groupTitle": "Oauth_Github"
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/oauth/github/bind",
    "title": "检测当前用户是否已经绑定了Github",
    "name": "GitBindApi",
    "group": "Oauth_Github",
    "filename": "app/modules/oauth/github.py",
    "groupTitle": "Oauth_Github",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "804",
            "description": "<p>Github尚未绑定</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "post",
    "url": "/api/oauth/github/bind",
    "title": "对未注册用户会回掉至此进行注册绑定",
    "name": "GitBindApiPost",
    "group": "Oauth_Github",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "nickname",
            "description": "<p>昵称</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>邮箱</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>邮箱注册码</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "pwd",
            "description": "<p>密码</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response",
          "content": "{\n    \"uid\": 123,\n    \"nickname\": \"ff\",\n    \"role\": 1,\n    \"gender\": 1,\n    \"avatar\": 1,\n    \"github\": \"asdfafa\",\n    \"fp\": true\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/oauth/github.py",
    "groupTitle": "Oauth_Github",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "601",
            "description": "<p>格式错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "805",
            "description": "<p>绑定失败</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "603",
            "description": "<p>邮箱验证码错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "605",
            "description": "<p>邮箱已经被注册</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "1000",
            "description": "<p>验证错误</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/oauth/github/callback",
    "title": "用户授权成功后回调",
    "name": "GitCallBackApi",
    "group": "Oauth_Github",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>用户授权code</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "state",
            "description": "<p>防止csrf的state</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>如果正常，则会跳转，否则会返回json格式报错信息</p>"
          }
        ]
      }
    },
    "filename": "app/modules/oauth/github.py",
    "groupTitle": "Oauth_Github",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "800",
            "description": "<p>用户取消授权</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "801",
            "description": "<p>验证码错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "802",
            "description": "<p>授权失败</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "803",
            "description": "<p>获取用户信息失败</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "805",
            "description": "<p>绑定失败</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/geetest",
    "title": "获取geetest",
    "name": "Geetest",
    "group": "User",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "challenge",
            "description": "<p>Challenge</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>返回码</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "gt",
            "description": "<p>GT</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "new_captcha",
            "description": "<p>New_captcha</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/accounts/apis.py",
    "groupTitle": "User"
  },
  {
    "version": "1.0.0",
    "type": "post",
    "url": "/api/email",
    "title": "发送邮件",
    "name": "MailApi",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>邮箱</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0 开发模式会额外返回email_code</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/accounts/apis.py",
    "groupTitle": "User",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "601",
            "description": "<p>格式错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "605",
            "description": "<p>邮箱已经被注册</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "602",
            "description": "<p>访问限制</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "post",
    "url": "/api/signin",
    "title": "登录",
    "name": "SigninApi",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "challenge",
            "description": "<p>Challenge</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "gt",
            "description": "<p>GT</p>"
          },
          {
            "group": "Parameter",
            "type": "Boolean",
            "optional": false,
            "field": "new_captcha",
            "description": "<p>New_captcha</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>邮箱</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "pwd",
            "description": "<p>密码</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "0",
            "description": "<p>登录成功</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"uid\": 123,\n    \"nickname\": \"昵称\",\n    \"role\": \"role\",\n    \"gender\": \"gender\",\n    \"avatar\": \"avatar\",\n    \"github\": \"github\",\n    \"fp\": \"fp\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/accounts/apis.py",
    "groupTitle": "User",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "604",
            "description": "<p>邮箱或者密码错误</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "post",
    "url": "/api/signup",
    "title": "注册",
    "name": "SignupApi",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "challenge",
            "description": "<p>Challenge</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "gt",
            "description": "<p>GT</p>"
          },
          {
            "group": "Parameter",
            "type": "Boolean",
            "optional": false,
            "field": "new_captcha",
            "description": "<p>New_captcha</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>注册邮箱</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "pwd",
            "description": "<p>注册密码</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>邮箱验证码</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "nickname",
            "description": "<p>昵称</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "0",
            "description": "<p>注册成功</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"uid\": 123,\n    \"nickname\": \"昵称\",\n    \"role\": \"role\",\n    \"gender\": \"gender\",\n    \"avatar\": \"avatar\",\n    \"github\": \"github\",\n    \"fp\": \"fp\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/accounts/apis.py",
    "groupTitle": "User",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "603",
            "description": "<p>邮箱验证码错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "600",
            "description": "<p>重复</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/user/:id",
    "title": "返回用户的信息以及其他信息",
    "name": "UserInfoApi",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>用户ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"uid\": 123,\n    \"nickname\": \"昵称\",\n    \"role\": \"role\",\n    \"gender\": \"gender\",\n    \"avatar\": \"avatar\",\n    \"github\": \"github\",\n    \"fp\": \"fp\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/accounts/apis.py",
    "groupTitle": "User"
  },
  {
    "version": "1.0.0",
    "type": "post",
    "url": "/api/settings",
    "title": "修改个人信息",
    "name": "UserSettings",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "nickname",
            "description": "<p>昵称</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "github",
            "description": "<p>Github</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "avatar",
            "description": "<p>头像</p>"
          },
          {
            "group": "Parameter",
            "type": "Boolean",
            "optional": false,
            "field": "favorite_public",
            "description": "<p>公开个人收藏</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"uid\": 123,\n    \"nickname\": \"昵称\",\n    \"role\": \"role\",\n    \"gender\": \"gender\",\n    \"avatar\": \"avatar\",\n    \"github\": \"github\",\n    \"fp\": \"fp\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/accounts/apis.py",
    "groupTitle": "User",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "put",
    "url": "/api/settings",
    "title": "修改个人密码",
    "name": "UserSettings2",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cur_pwd",
            "description": "<p>当前密码</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "pwd",
            "description": "<p>新密码</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      }
    },
    "filename": "app/modules/accounts/apis.py",
    "groupTitle": "User",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "607",
            "description": "<p>密码错误</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/nickname",
    "title": "查询此昵称是否已经使用",
    "name": "____",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "string",
            "optional": false,
            "field": "nickname",
            "description": "<p>昵称</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0: 表示没有使用</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/accounts/apis.py",
    "groupTitle": "User",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "606",
            "description": "<p>昵称已经被使用</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "post",
    "url": "/api/article",
    "title": "发布文章",
    "name": "ArticleApi",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "title",
            "description": "<p>题目</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "content",
            "description": "<p>正文</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "node",
            "description": "<p>节点</p>"
          },
          {
            "group": "Parameter",
            "type": "Boolean",
            "optional": false,
            "field": "login",
            "description": "<p>登录</p>"
          }
        ]
      }
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "700",
            "description": "<p>没有找到</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/comment/:article_id",
    "title": "获取评论",
    "name": "ArticleCommentApi",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "article_id",
            "description": "<p>文章ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "page",
            "description": "<p>第几页</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "per_page",
            "description": "<p>每页多少</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"comments\": [\n        {\n            content: \"ghjk\",\n            floor: 1,\n            id: \"59769cd508ba1e382ca491f7\",\n            rid: \"596d5f6b5192000009e370f9\",\n            time: 123123131,\n            uid: 123,\n            self: true\n        }\n        ...\n    ],\n    \"users\":[\n        {\n            \"uid\": 123,\n            \"nickname\": \"aa\",\n            \"role\": 1,\n            \"gender\": 1,\n            \"avatar\": asd,\n            \"github\": github,\n            \"fp\": self.favorite_public\n        }\n    ],\n    \"count\" : 21\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza"
  },
  {
    "version": "1.0.0",
    "type": "delete",
    "url": "/api/comment/:article_id/:comment_id",
    "title": "删除评论",
    "name": "ArticleCommentApiDelet",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "article_id",
            "description": "<p>文章ID</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "comment_id",
            "description": "<p>评论ID</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      }
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "702",
            "description": "<p>评论错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "post",
    "url": "/api/comment/:article_id",
    "title": "发表评论",
    "name": "ArticleCommentApiPost",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "content",
            "description": "<p>评论内容</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "at",
            "description": "<p>@用户</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      }
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "701",
            "description": "<p>文章错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/article/:node/:article",
    "title": "返回文章",
    "name": "ArticleDetailApi",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "node",
            "description": "<p>节点</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "article",
            "description": "<p>文章id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"id\": \"asdfa\",\n    \"node\": \"asd\",\n    \"title\": \"a\",\n    \"comment\": \"a\",\n    \"top\": true,\n    \"time\": 1233213213,\n    \"click\": 123,\n    \"like\": 32,\n    \"favorite\": true,\n    \"who\": 123,\n    \"login\": true,\n    \"origin\": true,\n    \"content\":\"hello world!\",\n    \"like_bool\": true,\n    \"favorite_bool\": true\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "701",
            "description": "<p>文章错误</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "post",
    "url": "/api/favorite/article/:article_id",
    "title": "收藏文章",
    "name": "ArticleFavoriteApi",
    "group": "plaza",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      }
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "701",
            "description": "<p>文章错误</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "delete",
    "url": "/api/favorite/article/:article_id",
    "title": "取消收藏文章",
    "name": "ArticleFavoriteApi2",
    "group": "plaza",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      }
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "701",
            "description": "<p>文章错误</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/hot/article",
    "title": "返回最近一月热议的项目",
    "name": "ArticleHotApi",
    "group": "plaza",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"articles\": [\n        {\n            \"id\": \"asdfa\",\n            \"node\": \"asd\",\n            \"title\": \"a\",\n            \"comment\": \"a\",\n            \"top\": true,\n            \"time\": 1233213213,\n            \"click\": 123,\n            \"like\": 32,\n            \"favorite\": true,\n            \"who\": 123,\n            \"login\": true,\n            \"origin\": true\"\n        },\n        {\n            \"id\": \"asdfa\",\n            \"node\": \"asd\",\n            \"title\": \"a\",\n            \"comment\": \"a\",\n            \"top\": true,\n            \"time\": 1233213213,\n            \"click\": 123,\n            \"like\": 32,\n            \"favorite\": true,\n            \"who\": 123,\n            \"login\": true,\n            \"origin\": true\"\n        }\n        ...\n    ],\n    \"users\": [\n        {\n            \"uid\": 123,\n            \"nickname\": \"asdf\",\n            \"role\": 1,\n            \"gender\": 1,\n            \"avatar\": \"www.ggadsf.com/asdfsafd.img\",\n            \"github\": \"github.com/adsfasdf\",\n            \"fp\": true\n        },\n        {\n            \"uid\": 123,\n            \"nickname\": \"asdf\",\n            \"role\": 1,\n            \"gender\": 1,\n            \"avatar\": \"www.ggadsf.com/asdfsafd.img\",\n            \"github\": \"github.com/adsfasdf\",\n            \"fp\": true\n        }\n    ],\n    \"count\": 123\n    \n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza"
  },
  {
    "version": "1.0.0",
    "type": "post",
    "url": "/api/like/article/:article_id",
    "title": "点赞",
    "name": "ArticleLikeApi",
    "group": "plaza",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      }
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "701",
            "description": "<p>文章错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "delete",
    "url": "/api/like/article/:article_id",
    "title": "取消点赞",
    "name": "ArticleLikeApi2",
    "group": "plaza",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      }
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "100",
            "description": "<p>参数错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "701",
            "description": "<p>文章错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/article",
    "title": "返回文章列表",
    "name": "ArticleListApi",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "page",
            "description": "<p>第几页</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "per_page",
            "description": "<p>每页多少</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "order_by",
            "description": "<p>排序规则</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"articles\": [\n        {\n            \"id\": \"asdfa\",\n            \"node\": \"asd\",\n            \"title\": \"a\",\n            \"comment\": \"a\",\n            \"top\": true,\n            \"time\": 1233213213,\n            \"click\": 123,\n            \"like\": 32,\n            \"favorite\": true,\n            \"who\": 123,\n            \"login\": true,\n            \"origin\": true\"\n        },\n        {\n            \"id\": \"asdfa\",\n            \"node\": \"asd\",\n            \"title\": \"a\",\n            \"comment\": \"a\",\n            \"top\": true,\n            \"time\": 1233213213,\n            \"click\": 123,\n            \"like\": 32,\n            \"favorite\": true,\n            \"who\": 123,\n            \"login\": true,\n            \"origin\": true\"\n        }\n        ...\n    ],\n    \"users\": [\n        {\n            \"uid\": 123,\n            \"nickname\": \"asdf\",\n            \"role\": 1,\n            \"gender\": 1,\n            \"avatar\": \"www.ggadsf.com/asdfsafd.img\",\n            \"github\": \"github.com/adsfasdf\",\n            \"fp\": true\n        },\n        {\n            \"uid\": 123,\n            \"nickname\": \"asdf\",\n            \"role\": 1,\n            \"gender\": 1,\n            \"avatar\": \"www.ggadsf.com/asdfsafd.img\",\n            \"github\": \"github.com/adsfasdf\",\n            \"fp\": true\n        }\n    ],\n    \"count\": 123\n    \n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza"
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/recommend",
    "title": "简单返回推荐",
    "name": "ArticleRecommendApi",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "page",
            "description": "<p>第几页</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "per_page",
            "description": "<p>每页多少</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"articles\": [\n        {\n            \"id\": \"asdfa\",\n            \"node\": \"asd\",\n            \"title\": \"a\",\n            \"comment\": \"a\",\n            \"top\": true,\n            \"time\": 1233213213,\n            \"click\": 123,\n            \"like\": 32,\n            \"favorite\": true,\n            \"who\": 123,\n            \"login\": true,\n            \"origin\": true\"\n        },\n        {\n            \"id\": \"asdfa\",\n            \"node\": \"asd\",\n            \"title\": \"a\",\n            \"comment\": \"a\",\n            \"top\": true,\n            \"time\": 1233213213,\n            \"click\": 123,\n            \"like\": 32,\n            \"favorite\": true,\n            \"who\": 123,\n            \"login\": true,\n            \"origin\": true\"\n        }\n        ...\n    ],\n    \"users\": [\n        {\n            \"uid\": 123,\n            \"nickname\": \"asdf\",\n            \"role\": 1,\n            \"gender\": 1,\n            \"avatar\": \"www.ggadsf.com/asdfsafd.img\",\n            \"github\": \"github.com/adsfasdf\",\n            \"fp\": true\n        },\n        {\n            \"uid\": 123,\n            \"nickname\": \"asdf\",\n            \"role\": 1,\n            \"gender\": 1,\n            \"avatar\": \"www.ggadsf.com/asdfsafd.img\",\n            \"github\": \"github.com/adsfasdf\",\n            \"fp\": true\n        }\n    ],\n    \"count\": 123\n    \n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza"
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/user/:uid",
    "title": "根据uid返回创建的文章",
    "name": "ArticleUidApi",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "uid",
            "description": "<p>用户ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "page",
            "description": "<p>第几页</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "per_page",
            "description": "<p>每页多少</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"articles\": [\n        {\n            \"node\": \"123\",\n            \"id\": \"12321\",\n            \"title\": \"asdfafd\",\n            \"time\": 123231234,\n        },\n        {\n            \"node\": \"123\",\n            \"id\": \"12321\",\n            \"title\": \"asdfafd\",\n            \"time\": 123231234,\n        },\n        ...\n    ],\n    \"count\": 1234\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza"
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/favorite/user/:uid",
    "title": "返回某人的收藏",
    "name": "FavoriteApi",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "uid",
            "description": "<p>用户ID</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "page",
            "description": "<p>第几页</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "per_page",
            "description": "<p>每页多少</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"favorite\": [\n        {\n            \"time\": 123,\n            \"rid\": \"123\",\n            \"node\": \"123\",\n            \"title\": \"title\"\n        },\n        {\n            \"time\": 123,\n            \"rid\": \"123\",\n            \"node\": \"123\",\n            \"title\": \"title\"\n        }\n        \n    ],\n    \"count\": 123\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "704",
            "description": "<p>主人设置了相关权限,禁止查看</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/node",
    "title": "返回所有的节点",
    "name": "NodeListApi",
    "group": "plaza",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"node\":[\n        {\n            \"id\": \"asdfafasdfafadfadfa\",\n            \"node\": \"adsfafsajfajf\"\n        },\n        {\n            \"id\": \"asdfafasdfafadfadfa2\",\n            \"node\": \"adsfafsajfajf\"\n        },\n    ]\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza"
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/article/node/:node",
    "title": "根据节点返回文章列表",
    "name": "NodeListDetailApi",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "node",
            "description": "<p>ObjectId类型</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "page",
            "description": "<p>第几页</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "per_page",
            "description": "<p>每页多少</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "order_by",
            "description": "<p>排序规则</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"articles\": [\n        {\n            \"id\": \"asdfa\",\n            \"node\": \"asd\",\n            \"title\": \"a\",\n            \"comment\": \"a\",\n            \"top\": true,\n            \"time\": 1233213213,\n            \"click\": 123,\n            \"like\": 32,\n            \"favorite\": true,\n            \"who\": 123,\n            \"login\": true,\n            \"origin\": true\"\n        },\n        {\n            \"id\": \"asdfa\",\n            \"node\": \"asd\",\n            \"title\": \"a\",\n            \"comment\": \"a\",\n            \"top\": true,\n            \"time\": 1233213213,\n            \"click\": 123,\n            \"like\": 32,\n            \"favorite\": true,\n            \"who\": 123,\n            \"login\": true,\n            \"origin\": true\"\n        }\n        ...\n    ],\n    \"users\": [\n        {\n            \"uid\": 123,\n            \"nickname\": \"asdf\",\n            \"role\": 1,\n            \"gender\": 1,\n            \"avatar\": \"www.ggadsf.com/asdfsafd.img\",\n            \"github\": \"github.com/adsfasdf\",\n            \"fp\": true\n        },\n        {\n            \"uid\": 123,\n            \"nickname\": \"asdf\",\n            \"role\": 1,\n            \"gender\": 1,\n            \"avatar\": \"www.ggadsf.com/asdfsafd.img\",\n            \"github\": \"github.com/adsfasdf\",\n            \"fp\": true\n        }\n    ],\n    \"count\": 123\n    \n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza"
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/message",
    "title": "获取未/已读消息",
    "name": "NoticeApi",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "status",
            "description": "<p>消息状态,1未读,2已读</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "page",
            "description": "<p>第几页</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "per_page",
            "description": "<p>每页多少</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"notification\": [\n        {\n            \"desc\": \"[@root ](http://www.git-share.com/user/1)\\n\\n** test **\",\n            \"from\": {\n                \"avatar\": \"/static/public/avatar/12.png\",\n                \"fp\": true,\n                \"gender\": null,\n                \"github\": \"https://github.com/zonghow\",\n                \"nickname\": \"zonghow\",\n                \"role\": 1,\n                \"uid\": 2\n            },\n            \"id\": \"596c535d0adde8000974c235\",\n            \"status\": 2,\n            \"time\": 1500271453,\n            \"title\": \"在文章163FM第2楼\",\n            \"to\": 1,\n            \"url\": \"/article/596c417c65d44029759edcee/596c4dde43ac1700081b4098\"\n        }\n    ]\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "delete",
    "url": "/api/message/:notice_id",
    "title": "删除消息",
    "name": "NoticeApi_Delete",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "optional": false,
            "field": "notice_id",
            "description": "<p>消息ID</p>"
          }
        ]
      }
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "703",
            "description": "<p>通知错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "put",
    "url": "/api/message/:notice_id",
    "title": "修改消息状态",
    "name": "NoticeApi_put",
    "group": "plaza",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "optional": false,
            "field": "notice_id",
            "description": "<p>消息ID</p>"
          },
          {
            "group": "Parameter",
            "optional": false,
            "field": "status",
            "description": "<p>消息状态</p>"
          }
        ]
      }
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "703",
            "description": "<p>通知错误</p>"
          },
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          }
        ]
      }
    }
  },
  {
    "version": "1.0.0",
    "type": "get",
    "url": "/api/message/new",
    "title": "预获取未读消息",
    "name": "NoticePreApi",
    "group": "plaza",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>0</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": 0,\n    \"count\": 12\n}",
          "type": "json"
        }
      ]
    },
    "filename": "app/modules/plaza/apis.py",
    "groupTitle": "plaza",
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "Integer",
            "optional": false,
            "field": "403",
            "description": "<p>需要重新授权登录</p>"
          }
        ]
      }
    }
  }
] });
