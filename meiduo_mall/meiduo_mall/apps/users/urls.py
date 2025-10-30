#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/10/27 13:05
# @Author  : Seven
# @File    : urls.py
# @Software: PyCharm
from django.urls import path, include, re_path
from .views import RegisterView, UsernameCountView, MobileCountView
from meiduo_mall.utils.converters import UsernameConverter, MobileConverter

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', UsernameCountView.as_view(), name='username'),
    path('usernames/<username:username>/count/', UsernameCountView.as_view(), name='username'),
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view(), name='mobile')
]
