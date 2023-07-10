import redis

from actions.constant.server_settings import server_settings
from loguru import logger

redis_pool = redis.ConnectionPool(host=server_settings.redis_host,
                                  port=server_settings.redis_port,
                                  db=server_settings.redis_db,
                                  password=server_settings.redis_password, decode_responses=True, encoding='utf8')
redis_client = redis.StrictRedis(
    connection_pool=redis_pool,
    decode_responses=True, encoding='utf8'
)


class RedisUtils:

    @staticmethod
    def get_prompt_template():
        return redis_client.get('prompt_template')

    @staticmethod
    def get_fallback_prompt():
        return redis_client.get('fallback_prompt')

    @staticmethod
    def set_default_prompt(force):
        logger.info('初始化OpsPilot默认参数')

        default_fallback_prompt = '扮演专业的运维工程师'

        fallback_prompt = redis_client.get('fallback_prompt')
        redis_client.set('fallback_prompt', default_fallback_prompt)

        if force:
            redis_client.set('fallback_prompt', default_fallback_prompt)
        else:
            if fallback_prompt is None:
                logger.info(f'初始化默认FallBack Prompt为[{default_fallback_prompt}]')
                redis_client.set('fallback_prompt', default_fallback_prompt)
            else:
                logger.info(f'FallBack Prompt已经设置，当前Prompt为[{fallback_prompt}]')

        default_prompt_template = """Use the following pieces of context to answer the question at the end.
             If you don't know the answer, just say that you don't know, don't try to make up an answer.

            {context}
            
            {index_context}
            
            Question: {question}
            Answer in Chinese:"""
        if force:
            redis_client.set('prompt_template', default_prompt_template)
        else:
            prompt_template = redis_client.get('prompt_template')
            if prompt_template is None:
                logger.info(f'初始化默认Prompt Template为[{default_prompt_template}]')
                redis_client.set('prompt_template', default_prompt_template)
            else:
                logger.info(f'Prompt Template已经设置，当前Prompt为[{prompt_template}]')

        logger.info('参数初始化完成')
