import redis
from redis.exceptions import ConnectionError, TimeoutError


def test_redis_read_write():
    # 配置 Redis 连接参数（与你的 dev.py 中 Redis 配置一致）
    redis_config = {
        "host": "192.168.10.50",  # Redis 服务器 IP
        "port": 6379,  # 端口
        "db": 0,  # 数据库编号（对应 dev.py 中的 /0）
        "password": "123456",  # 若 Redis 有密码，填写实际密码（你的配置中未设置，留空）
        "decode_responses": True,  # 自动将 bytes 转换为字符串（可选，方便处理）
        "socket_timeout": 5  # 连接超时时间（秒）
    }

    try:
        # 1. 建立 Redis 连接
        r = redis.Redis(**redis_config)

        # 2. 测试写入数据
        test_key = "test_direct"
        test_value = "hello_redis_direct"
        expire_seconds = 60  # 60秒后过期
        r.set(test_key, test_value, ex=expire_seconds)
        print(f"写入成功：key={test_key}, value={test_value}")

        # 3. 测试读取数据
        read_value = r.get(test_key)
        if read_value == test_value:
            print(f"读取成功：key={test_key}, value={read_value}")
        else:
            print(f"读取失败：预期 {test_value}，实际 {read_value}")

        # 4. 测试删除数据（可选）
        # delete_result = r.delete(test_key)
        # if delete_result == 1:
        #     print(f"删除成功：key={test_key}")

    except ConnectionError:
        print("连接失败：请检查 Redis 服务器 IP、端口是否正确，或服务器是否启动")
    except TimeoutError:
        print("连接超时：Redis 服务器无响应，请检查网络或服务器状态")
    except Exception as e:
        print(f"其他错误：{str(e)}")


if __name__ == "__main__":
    test_redis_read_write()
