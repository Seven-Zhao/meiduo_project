import logging
import os

import django
from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from celery_tasks.sms.tasks import send_sms_code
from meiduo_mall.conf import configs
from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.utils.sms_util import get_code, sms_util
from verifications import constants
from verifications.libs.captcha.captcha import captcha
from verifications.libs.yuntongxun.ccp_sms_singleton import CCP

# 获取日志记录器
logger = logging.getLogger('django')


# Create your views here.
class SMSCodeView(View):
    """短信验证码"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 接收参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 校验参数
        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必要参数'})

        # 创建redis连接对象
        redis_conn = get_redis_connection('verify_code')

        # 判断是否频繁发送短信验证码
        send_flag = redis_conn.get(f'send_flag_{mobile}')
        if send_flag:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信过于频繁'})

        # 提取图形验证码
        image_code_server = redis_conn.get(f'img_{uuid}')
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码已失效'})

        # 删除图形验证，避免恶意测试图形验证码
        try:
            redis_conn.delete(f'img_{uuid}')
        except Exception as e:
            logger.error(e)

        # 对比图形验证码
        # redis 存取都是bytes类型，因此需要转换
        image_code_server = image_code_server.decode()
        if image_code_server.lower() != image_code_client.lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})

        # 生成短信验证码
        # 测试的时候使用容联云，发送4位验证码
        # 上线的时候使用互亿短信平台，可以发送6位验证码，且支持个人认证
        sms_code = get_code(4)
        logger.info(f'sms_code: {sms_code}')
        # 保存短信验证码
        # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        # 保存发送短信验证码的标记
        # redis_conn.setex(f'send_flag_{mobile}', constants.SEND_SMS_CODE_INTERVAL, 1)

        # 创建redis管道
        pl = redis_conn.pipeline()
        # 将命令添加到队列中
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex(f'send_flag_{mobile}', constants.SEND_SMS_CODE_INTERVAL, 1)
        # 执行
        pl.execute()

        # 发送短信验证码
        # ccp = CCP(
        #     server_ip=configs.SERVER_IP,
        #     server_port=configs.SERVER_PORT,
        #     soft_version="2013-12-26",
        #     account_sid=configs.ACCOUNT_SID,
        #     account_token=configs.ACCOUNT_TOKEN,
        #     app_id=configs.APP_ID
        # )
        # ccp.send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
        #                       constants.SEND_SMS_TEMPLATE_ID)

        # 使用互亿短信平台
        # sms_util.send_sms(mobile=mobile, verify_code=sms_code)

        # 使用Celery异步发送短信验证码
        send_sms_code.delay(mobile, sms_code)

        # 响应结果。
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})


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
        logger.info(f'image_code:{text}')
        # 保存图像验证码
        redis_conn = get_redis_connection('verify_code')
        # redis_conn.setex('key', 'expires', 'value')
        redis_conn.setex(f'img_{uuid}', constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 响应结果。
        return http.HttpResponse(image, content_type='image/jpg')
