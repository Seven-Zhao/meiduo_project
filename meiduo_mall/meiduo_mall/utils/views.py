#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/17 16:01
# @Author  : Seven
# @File    : views.py
# @Software: PyCharm
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin

from meiduo_mall.utils.response_code import RETCODE


class LoginRequiredJSONMixin(LoginRequiredMixin):
    """自定义判断用户是否登录的扩展类：返回JSON"""

    # 为什么只需要重写handle_no_permission方法？
    # 因为判断用户是否登录的操作，在父类LoginRequiredMixin中 已经完成
    # 子类只需要关心如果用户未登录，对应怎么样。
    def handle_no_permission(self):
        """返回JSON数据"""
        return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})
