#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/17 23:18
# @Author  : Seven
# @File    : urls.py
# @Software: PyCharm
from django.contrib import admin
from django.urls import path, include

from areas.views import AreasView

app_name = 'areas'

urlpatterns = [
    # 省市区的三级联动
    path('areas/', AreasView.as_view()),
]
