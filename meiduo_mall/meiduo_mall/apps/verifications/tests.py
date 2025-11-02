import os
import django
import time

# 手动指定Django配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')
django.setup()

from django.test import TestCase
from django.core.cache import caches
from redis.exceptions import ConnectionError as RedisConnectionError


class VerifyCodeCacheTest(TestCase):
    """验证码缓存测试类"""

    def test_verify_code_cache_write(self):
        """测试往verify_code缓存库写入key"""
        # 获取verify_code缓存实例
        verify_cache = caches['verify_code']

        try:
            # 定义测试数据
            test_key = 'test_sms_code_13800138000'
            test_value = '6666'
            expire_seconds = 30

            # 写入缓存
            verify_cache.set(test_key, test_value, expire_seconds)

            # 验证写入
            retrieved_value = verify_cache.get(test_key)
            self.assertEqual(retrieved_value, test_value,
                             "verify_code缓存写入失败：值不匹配")

            # 验证过期
            time.sleep(expire_seconds + 1)
            expired_value = verify_cache.get(test_key)
            self.assertIsNone(expired_value, "缓存过期功能异常")

        except RedisConnectionError:
            self.fail("Redis连接失败，请检查服务、地址、密码是否正确")
        except Exception as e:
            self.fail(f"操作失败：{str(e)}")
