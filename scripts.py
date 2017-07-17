from mongoengine import connect
from app.settings import MONGODB_SETTINGS
from app.models.accounts.users import EmailTemplate
from app.models.plaza.article import ArticleNode


connect(host=MONGODB_SETTINGS, alias='default', tz_aware=True)
# 创建用户注册模板


TEMP = """
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title><style>body{background:#e2e2e2;height:600px}.container{width:606px;height:300px;background:#fff;position:absolute;top:50%;left:50%;margin-left:-303px;margin-top:-150px}a{color:#fff;text-decoration:none}.header{background:#347ef2;padding-left:2px;height:50px;color:#fff;line-height:50px}.content{padding:30px;font-family:PingFang SC-Thin,Source Han Sans,Microsoft Yahei,sans-serif;font-size:15px;line-height:25px}.signature{float:right}</style></head><body><div class="container"><div class="header"><span class="logo"><a href="http://git-share.com">GitShare</a></span> <span class="fenge">|</span> <span>分享您的项目!</span></div><div class="content"><div>尊敬的用户：</div><div style="text-indent:2em">您好，感谢您注册GitShare！</div>您的验证码是：<span>{{ code }}</span>。<div>如您未做出此操作，可能是他人误填，请忽略此邮件。</div><div>本邮件为系统发送，请勿回复。</div><div class="signature">GitShare团队</div></div></div></body></html>
"""

EmailTemplate.create_temp("欢迎注册GitShare账号", TEMP, 1, "注册使用")

# 创建节点
ArticleNode.create_node("编程")
ArticleNode.create_node("Python")
ArticleNode.create_node("PHP")
ArticleNode.create_node("Java")
