import re

MAX_PW_LEN = 32  # 最大允许长度
MIN_PW_LEN = 7  # 最小允许长度
AVAILABLE_CHARS = '^[a-zA-Z][a-zA-Z0-9_\\.\\!_]{%s,%s}$' % (MIN_PW_LEN, MAX_PW_LEN)
RE_AVAILABLE_CHARS = re.compile(AVAILABLE_CHARS)

RE_EMAIL = re.compile(
    # dot-atom
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    # quoted-string
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
    # domain (max length of an ICAAN TLD is 22 characters)
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))$', re.IGNORECASE
)

URL_REGEX = re.compile(
    r'^(?:[a-z0-9\.\-]*)://'  # scheme is validated separately
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

NICKNAME_REGEX = re.compile(r"^[a-zA-Z0-9_\\!]{3,20}$")


def verify_password(password):
    """ 验证密码的合法性

    合法的密码：
    1. 长度在 8 － 32 位之间
    2. 合法字符集为: 密码为至少8位，字符集[a-Z0-9,.!_]

    返回密码是否合法

    :param str password: Password that need to be verify
    :return: True on passes, False on fail.
    """
    match = RE_AVAILABLE_CHARS.match(password)

    if not match:
        return False
    return True


def verify_email(email):
    """ 验证邮箱合法性

    :param str email: 要验证的邮箱, 需少于64位长度
    :rtype: int
    """
    match = RE_EMAIL.match(email)

    if not match:
        return False
    return True


def verify_url(url):
    match = URL_REGEX.match(url)
    if not match:
        return False
    return True


def verify_nickname(nickname):
    match = NICKNAME_REGEX.match(nickname)
    if not match:
        return False
    return True
