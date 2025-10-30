#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/10/29 22:43
# @Author  : Seven
# @File    : converters.py
# @Software: PyCharm
from django.urls import converters, register_converter


class UsernameConverter(object):
    """
    自定义用户名转换器：
        - 匹配字母、数字、下划线、减号（[a-zA-Z0-9_-]）
        - 长度 5-20 字符
    """
    # 正则匹配规则（与原 re_path 保持一致）
    # 注意：原正则中的 {5, 20} 空格需去掉，否则无效
    regex = r'[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        """将 URL 中的字符串转换为 Python 变量（直接返回即可）"""
        return value

    def to_url(self, value):
        """将 Python 变量转换为 URL 中的字符串（直接返回即可）"""
        return value


class MobileConverter(object):
    """
    自定义用户名转换器：
        - 匹配字母、数字、下划线、减号（[a-zA-Z0-9_-]）
        - 长度 5-20 字符
    """
    # 正则匹配规则（与原 re_path 保持一致）
    # 注意：原正则中的 {5, 20} 空格需去掉，否则无效
    regex = r'1[3-9]\d{9}'

    def to_python(self, value):
        """将 URL 中的字符串转换为 Python 变量（直接返回即可）"""
        return value

    def to_url(self, value):
        """将 Python 变量转换为 URL 中的字符串（直接返回即可）"""
        return value


# 注册转换器，指定别名（如 'username'）
register_converter(UsernameConverter, 'username')
register_converter(MobileConverter, 'mobile')
