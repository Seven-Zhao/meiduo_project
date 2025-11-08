#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/2 19:25
# @Author  : Seven
# @File    : rly_sms_test.py
# @Software: PyCharm
from ronglian_sms_sdk import SmsSDK

accId = '2c94811c9860a9c4019a43d0a6634604'
accToken = '9c68bd66ed184ca1a9e40faccad94788'
appId = '2c94811c9860a9c4019a43d0a823460b'

# 直接修改SmsSDK的url属性为沙箱测试环境
SmsSDK.url = "https://sandboxapp.cloopen.com:8883"


def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    mobile = '15013632916'
    # datas 元组中，第一个是验证码，第二个是有效时长，单位为分钟
    datas = ('1234', '5')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)


if __name__ == '__main__':
    send_message()
