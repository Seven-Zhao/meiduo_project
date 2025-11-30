#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/8 18:20
# @Author  : Seven
# @File    : utils.py
# @Software: PyCharm
# 自定义用户认证的后端：实现多账号登录
import re

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from itsdangerous import URLSafeTimedSerializer as Serializer, BadData

from users.models import User
from verifications import constants


def check_verify_email_token(token):
    """
    验证token并提取user
    :param token: 用户信息签名后的结果
    :return: user, None
    """
    serializer = Serializer(secret_key=settings.SECRET_KEY)
    try:
        data = serializer.loads(token, max_age=constants.ACCESS_TOKEN_EXPIRES)
    except BadData:
        return None
    else:
        user_id = data.get('user_id')
        email = data.get('email')
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user


def generate_verify_email_url(user):
    """
    生成邮箱验证链接
    :param user: 当前登录用户
    :return: verify_url
    """
    serializer = Serializer(secret_key=settings.SECRET_KEY)
    data = {'user_id': user.id, 'email': user.email}
    token = serializer.dumps(data)
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    return verify_url


def get_user_by_account(account):
    """
    根据account查询用户
    :param account: 用户名或者手机号
    :return: user
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 手机号登录
            user = User.objects.get(mobile=account)
        else:
            # 用户名登录
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证后端"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写认证方法，实现多账号登录
        :param request: 请求对象
        :param username: 用户名或手机号
        :param password: 密码
        :param kwargs: 其他参数
        :return: user
        """
        #
        # 根据传入的username获取user对象。username可以是手机号也可以是账号
        user = get_user_by_account(username)

        # 校验user是否存在并校验密码是否正确
        if user and user.check_password(password):
            return user
