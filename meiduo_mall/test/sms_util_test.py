#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/3 21:59
# @Author  : Seven
# @File    : sms_util_test.py
# @Software: PyCharm
import os

import django

from meiduo_mall.utils.sms_util import sms_util, get_code, _get_caller_directory, _get_logger

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')
    django.setup()
    mobile = '18502319543'
    code_num = 6
    # result = sms_util.send_sms(mobile, code_num)
    code = get_code()

