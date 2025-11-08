#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Time    : 2025/11/3 11:19
# @Author  : Seven
# @File    : sms_util.py
# @Software: PyCharm
import inspect
import logging
import os
import random
import threading
import urllib.parse
import urllib.request
from logging.handlers import RotatingFileHandler

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


def _get_caller_directory():
    """
    获取调用者文件所在的目录
    :return: 调用者文件目录路径
    """
    # 获取调用栈
    frame = inspect.currentframe()
    try:
        # 向上追溯调用栈，找到第一个不是本文件的调用者
        while frame:
            filename = frame.f_code.co_filename
            # 如果不是当前文件，就返回其目录
            if not filename.endswith('sms_util.py'):
                caller_dir = os.path.dirname(os.path.abspath(filename))
                return caller_dir
            frame = frame.f_back
    finally:
        del frame

    # 如果没找到，返回当前工作目录
    return os.getcwd()


def _get_logger(logger_name='sms'):
    """
    获取日志记录器：优先使用Django日志，无Django环境则使用标准日志
    :param logger_name: 日志记录器名称
    :return: logging.Logger 实例
    """
    try:
        from django.conf import settings
        if hasattr(settings, 'LOGGING'):
            return logging.getLogger(logger_name)
    except (ImportError, AttributeError, ImproperlyConfigured):
        # 无 Django 环境：初始化 Python 标准日志（降级兼容）
        pass

    # 降级逻辑：python标准日志配置（输出到终端+临时文件）
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # 1.终端输出handler（StreamHandler）
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 2.临时文件Handler
    temp_log_dir = os.path.join(os.path.dirname(__file__), "temp_logs")
    os.makedirs(temp_log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        os.path.join(temp_log_dir, 'sms_util.log'),
        maxBytes=100 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_formatter = logging.Formatter(
        "%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


def get_code(num=4):
    """
    生成指定位数的验证码
    :param num: 要生成几位的验证码
    :return: 生成的验证码
    """
    return random.randint(
        int('1{}'.format('0' * (num - 1))),
        int('9{}'.format('9' * (num - 1)))
    )


class SMSUtil(object):
    """
    短信工具类 - 单例模式
    """
    _instance = None
    _lock = threading.Lock()
    _initialized = False

    logger = _get_logger(logger_name='sms')

    def __new__(cls, *args, **kwargs):
        """实现单例模式"""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, account=None, password=None, base_url=None):
        if not self._initialized:
            load_dotenv()
            self.account = account or os.getenv('IHUYI_ACCOUNT')
            self.password = password or os.getenv('IHUYI_PASSWORD')
            self.base_url = base_url or 'https://106.ihuyi.com/webservice/sms.php?method=Submit'
            self._initialized = True

    def set_base_usl(self, new_url):
        if new_url.statwith('http'):
            self.base_url = new_url
        else:
            raise ValueError('base_url 必须是合法的HTTP/HTTPS 地址')

    def send_sms(self, mobile, verify_code, template=None):
        """
        发送短信验证码
        :param mobile: 手机号
        :param verify_code: 验证码
        :param template: 自定义短信模版
        :return: 发送结果
        """

        # 使用自定义或默认模版
        if template:
            content = template.format(verify_code=verify_code)
        else:
            content = f'您的验证码是：{verify_code}。请不要把验证码泄露给其他人。'

        # 定义请求数据
        values = {
            'account': self.account,
            'password': self.password,
            'mobile': mobile,
            'content': content,
            'format': 'json',
        }

        try:
            # 将数据进行编码
            data = urllib.parse.urlencode(values).encode(encoding='UTF8')

            # 发送请求
            req = urllib.request.Request(self.base_url, data)
            response = urllib.request.urlopen(req)
            res = response.read()

            result = res.decode('utf8')
            self.logger.info(f"短信发送结果: {result}")

            # 返回验证码和发送结果
            return {
                'success': True,
                'code': verify_code,
                'result': result
            }
        except Exception as e:
            self.logger.error(f"短信发送失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'code': None
            }

    def update_config(self, account, password, base_url=None):
        """
        更新配置信息
        :param account: 账号
        :param password: 密码
        :param base_url: 接口地址
        """
        self.account = account
        self.password = password
        self.set_base_usl(base_url)

    def batch_send_sms(self, mobiles, code_num=6, template=None):
        """
        批量发送短信
        :param mobiles: 手机号列表
        :param code_num: 验证码位数
        :param template: 短信模板
        :return: 发送结果列表
        """
        results = []
        for mobile in mobiles:
            result = self.send_sms(mobile, code_num, template)
            results.append({
                'mobile': mobile,
                'result': result
            })
        return results


# 创建单例对象
sms_util = SMSUtil()
