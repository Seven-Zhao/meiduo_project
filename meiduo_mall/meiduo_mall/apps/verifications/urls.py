#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/10/30 18:29
# @Author  : Seven
# @File    : urls.py
# @Software: PyCharm
from django.urls import path, include, re_path
from .views import ImageCodeView

app_name = 'verifications'

urlpatterns = [
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$', ImageCodeView.as_view())
]
