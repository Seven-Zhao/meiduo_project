# -*- coding:utf-8 -*-
import threading

from meiduo_mall.conf import configs
# import ssl
# 解决Mac开发环境下，网络错误的问题
# ssl._create_default_https_context =ssl._create_stdlib_context

from verifications.libs.yuntongxun.CCPRestSDK import REST

_softVersion = '2013-12-26'


class CCP(object):
    """发送短信验证码的单例类"""
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __init__(self, server_ip, server_port, account_sid, account_token, app_id, soft_version=_softVersion):
        if not self._initialized:
            self.rest = REST(server_ip, server_port, soft_version)
            self.rest.setAccount(account_sid, account_token)
            self.rest.setAppId(app_id)
            self._initialized = True

    def __new__(cls, *args, **kwargs):
        """
        定义单例的初始化方法
        :return: 单例
        """
        # 判断单例是否存在：_instance属性中存储的就是单例
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    # 如果单例不存在，初始化单例
                    cls._instance = super(CCP, cls).__new__(cls)

        # 返回单例
        return cls._instance

    def send_template_sms(self, to, datas, tempId):
        """
        发送短信验证码单例方法
        :param to: 手机号
        :param datas: 内容数据
        :param tempId: 模板ID
        :return: 成功：0 失败：-1
        """
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        if result.get('statusCode') == '000000':
            return 0
        else:
            return -1


if __name__ == '__main__':
    # 注意： 测试的短信模板编号为1
    # sendTemplateSMS('17600992168', ['123456', 5], 1)

    # 单例类发送短信验证码
    ccp = CCP(
        server_ip=configs.SERVER_IP,
        server_port=configs.SERVER_PORT,
        soft_version="2013-12-26",
        account_sid=configs.ACCOUNT_SID,
        account_token=configs.ACCOUNT_TOKEN,
        app_id=configs.APP_ID
    )
    ccp.send_template_sms('18502319543', ['123456', 1], 1)
