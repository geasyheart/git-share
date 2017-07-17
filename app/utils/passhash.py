from passlib.hash import django_pbkdf2_sha256

from app.utils.rtype import verify_password


class PassHash(object):
    @classmethod
    def encrypt(cls, pwd):
        """
        对密码进行校验以及加密
        :type pwd:str
        :return:
        """
        if not verify_password(pwd):
            return False
        return django_pbkdf2_sha256.hash(pwd)

    @classmethod
    def verify(cls, pwd, hash):
        """
        对密码进行校验
        :type pwd: str
        :type hash: str
        :param pwd: 密码
        :param hash: 哈希值
        :return: True or False
        :rtype:bool
        """
        return django_pbkdf2_sha256.verify(pwd, hash)
