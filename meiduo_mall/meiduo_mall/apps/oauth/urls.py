#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/16 21:50
# @Author  : Seven
# @File    : urls.py
# @Software: PyCharm
from django.urls import path, include, re_path

from oauth.views import QQAuthURLView, QQAuthUserView

app_name = 'oauth'

urlpatterns = [
    path('qq/login/', QQAuthURLView.as_view()),
    path('oauth_callback/', QQAuthUserView.as_view()),
]
