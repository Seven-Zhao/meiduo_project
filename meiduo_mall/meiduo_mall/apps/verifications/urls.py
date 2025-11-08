#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/10/30 18:29
# @Author  : Seven
# @File    : urls.py
# @Software: PyCharm
from django.urls import path, include, re_path
from .views import ImageCodeView, SMSCodeView

app_name = 'verifications'

urlpatterns = [
    # 图形验证码
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$', ImageCodeView.as_view()),
    # 短信验证码
    re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', SMSCodeView.as_view())
]
