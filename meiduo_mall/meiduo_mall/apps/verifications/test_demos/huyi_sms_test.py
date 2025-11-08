#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/2 21:40
# @Author  : Seven
# @File    : huyi_sms_test.py
# @Software: PyCharm
# python3
# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户https://user.ihuyi.com/new/register.html
# 注意事项：
# （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
# （2）请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

import random
import urllib.parse
import urllib.request


def get_code(num=4):
    """
    生成指定位数的验证码，如果不传值，就默认生成4位的验证码
    :param num: 要生成几位的验证码
    :return: 生成的验证码
    """
    return random.randint(
        int('1{}'.format('0' * (num - 1))),
        int('9{}'.format('9' * (num - 1)))
    )


def send_sms(mobile, code_num=4):
    """
    发送短信验证码
    :param mobile: 你要发给谁
    :param code_num: 发送几位的验证码
    :return:
    """
    # 接口地址
    url = 'https://106.ihuyi.com/webservice/sms.php?method=Submit'

    verify_code = get_code(6)

    # 定义请求的数据
    values = {
        'account': 'C93350795',
        'password': 'b532060188bdc68c41006804a99bc150',
        'mobile': mobile,
        'content': f'您的验证码是：{verify_code}。请不要把验证码泄露给其他人。',
        'format': 'json',
    }

    # 将数据进行编码
    data = urllib.parse.urlencode(values).encode(encoding='UTF8')

    # 发起请求
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    res = response.read()

    # 打印结果，然后你的手机应该就能接到短信了
    print(res.decode("utf8"))  # {"code":2,"msg":"提交成功","smsid":"16842079209571524017"}


if __name__ == '__main__':
    send_sms('18502319543')
