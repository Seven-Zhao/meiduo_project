#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/10/29 19:30
# @Author  : Seven
# @File    : urls.py
# @Software: PyCharm
from django.urls import path, include
from .views import IndexView

app_name = 'contents'

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]