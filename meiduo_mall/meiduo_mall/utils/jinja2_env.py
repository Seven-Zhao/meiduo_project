#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/10/23 23:28
# @Author  : Seven
# @File    : jinja2_env.py
# @Software: PyCharm
import jinja2
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def jinja2_environment(**options):
    """
    Jinja2 环境
    :param options:
    :return:
    """
    # 创建环境对象
    env = jinja2.Environment(**options)
    # 自定义语法：{{ static('静态文件相对路径') }} , {{ path('路由命名空间') }}
    env.globals.update({
        'static': staticfiles_storage.url,
        'path': reverse
    })
    # 返回环境对象，
    return env
