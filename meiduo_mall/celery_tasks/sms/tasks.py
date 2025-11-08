#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/7 22:59
# @Author  : Seven
# @File    : tasks.py
# @Software: PyCharm
import logging

from celery_tasks.main import celery_app
from celery_tasks.sms import constants
from celery_tasks.sms.sms_util import sms_util
from celery_tasks.sms.yuntongxun.ccp_sms import CCP


# 定义任务（就是函数）
@celery_app.task(bind=True, name='send_sms_code', retry_backoff=3)
def send_sms_code(self, mobile, sms_code):
    """
    发送短信验证码的任务
    :param self: 当 Celery 任务装饰器中指定bind=True时，
                 Celery 会将任务实例本身作为第一个参数传入任务函数，
                 这时候函数的第一个参数就相当于 “自身实例”
    :param mobile: 手机号码
    :param sms_code: 短信验证码
    :return: 成功 0， 失败 -1
    """
    try:
        send_ret = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
                                           constants.SEND_SMS_TEMPLATE_ID)
        # 使用互亿短信平台
        # send_ret = -1
        # result = sms_util.send_sms(mobile=mobile, verify_code=sms_code)
        # if result.get('success'):
        #     send_ret = 0
    except Exception as e:
        # 有异常自动重试三次
        raise self.retry(exc=e, max_retries=3)
    if send_ret != 0:
        # 有异常自动重试三次
        raise self.retry(exc=Exception('发送短信失败'), max_retries=3)
    return send_ret
