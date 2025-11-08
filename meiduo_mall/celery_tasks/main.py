#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/7 22:37
# @Author  : Seven
# @File    : main.py
# @Software: PyCharm

# Celery 入口
from celery import Celery

# 创建celery实例
celery_app = Celery('meiduo')

# 加载celery配置
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
