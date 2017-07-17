from jinja2 import Template

from app.celery_tasks.celery_init import celery
from app.models.accounts.users import EmailTemplate


@celery.task(bind=True, name="celery_tasks.send_email")
def celery_send_mail(self, sender, to, subject, html_content, content=None):
    pass


class Email(object):
    def __init__(self, sender, to, temp_id, **temp_args):
        """
        发送邮件
        :type sender:dict
        :type to: str or list
        :type temp_id: int
        :param sender: {"email":"","password":""}
        :param to: 最好单发，不要群发
        :param temp_id:  表示EmailTemplate对应的模板ID
        :param temp_args: 表示需要渲染的参数
        """
        self.sender = sender
        self.to = to
        et_ins = EmailTemplate.with_id(temp_id)
        if not et_ins:
            raise NotImplementedError("这个模板没有找到!")
        self.subject = et_ins.subject
        template = et_ins.temp
        temp = Template(template)
        self.html = temp.render(temp_args)

    def send(self):
        celery_send_mail.apply_async(args=[
            self.sender,
            self.to,
            self.subject,
            self.html
        ])
