import os

import django
from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from verifications import constants
from verifications.libs.captcha.captcha import captcha


# Create your views here.
class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """
        # 接收和校验参数
        # 实现主体业务逻辑：生成、保存、响应图形验证码
        # 生成图像验证码
        text, image = captcha.generate_captcha()
        # 保存图像验证码
        redis_conn = get_redis_connection('verify_code')
        print(redis_conn)
        # redis_conn.setex('key', 'expires', 'value')
        redis_conn.setex(f'img_{uuid}', constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 响应结果。
        return http.HttpResponse(image, content_type='image/jpg')


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')
    django.setup()
    redis_conn2 = get_redis_connection('verify_code')
    print(redis_conn2)
    # 定义测试数据
    test_key = 'test_sms_code_13800138000'
    test_value = '6666'
    expire_seconds = 30

    # 写入缓存
    redis_conn2.set(test_key, test_value, expire_seconds)

    # 验证写入
    retrieved_value = redis_conn2.get(test_key).decode('utf-8')
    print(retrieved_value)
