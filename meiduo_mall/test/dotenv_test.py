#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/3 12:22
# @Author  : Seven
# @File    : dotenv_test.py
# @Software: PyCharm
import os

from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    account = os.getenv('IHUYI_ACCOUNT')
    print(account)