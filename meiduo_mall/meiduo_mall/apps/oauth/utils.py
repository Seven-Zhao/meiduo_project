#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/16 23:32
# @Author  : Seven
# @File    : utils.py
# @Software: PyCharm
from django.conf import settings
from itsdangerous import TimedSerializer as Serializer, BadData

from verifications import constants


def check_access_token(access_token_openid):
    """
    反解、反序列化access_token_openid
    :param access_token_openid: openid的密文
    :return: openid的明文
    """
    # 创建序列化器对象：序列化和反序列化器的参数必须保持一致
    serializer = Serializer(secret_key=settings.SECRET_KEY)
    # 反序列化openid密文
    try:
        data = serializer.loads(access_token_openid, max_age=constants.ACCESS_TOKEN_EXPIRES)
    except BadData:
        # Token 过期
        return None
    else:
        # 返回openid明文
        openid = data.get('openid')
        return openid


def generate_access_token(openid):
    """
    签名openid
    :param openid: 用户的openid
    :return: access_token
    """
    # 创建序列化器对象
    serializer = Serializer(secret_key=settings.SECRET_KEY)
    # 准备带序列化的字典数据
    data = {'openid': openid}
    # 调用序列化器的dumps方法进行序列化：返回的类型是bytes
    token = serializer.dumps(data)
    access_token = token.decode()
    return access_token
