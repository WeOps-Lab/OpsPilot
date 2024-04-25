import redis

from loguru import logger

from actions.constants.server_settings import server_settings

redis_pool = redis.ConnectionPool(host=server_settings.redis_host,
                                  port=server_settings.redis_port,
                                  db=server_settings.redis_db,
                                  password=server_settings.redis_password,
                                  decode_responses=True, encoding='utf8')

redis_client = redis.StrictRedis(
    connection_pool=redis_pool,
    decode_responses=True, encoding='utf8'
)


class RedisUtils:
    @staticmethod
    def set_value(key, value, expire_time=None):
        try:
            redis_client.set(key, value, ex=expire_time)
        except Exception as e:
            logger.error(f"set_value error: {e}")

    @staticmethod
    def get_value(key):
        try:
            return redis_client.get(key)
        except Exception as e:
            logger.error(f"get_value error: {e}")
            return None

    @staticmethod
    def delete_value(key):
        try:
            redis_client.delete(key)
        except Exception as e:
            logger.error(f"delete_value error: {e}")
            return None
