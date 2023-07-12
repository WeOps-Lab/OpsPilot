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
    def get_fallback_prompt(context=''):
        return redis_client.get('fallback_prompt').replace('{context}', context)

    @staticmethod
    def set_default_prompt(force):
        logger.info('初始化OpsPilot默认参数')

        default_fallback_prompt = """ 我希望你扮演运维工程师，你是一个非常严谨的人，不会给出模棱两可的回答，我要求你具备以下特点：
                                                           1、 一步一步的思考
                                                           2、回答问题严谨，不会回答任何你不清楚的信息，假如你没有把握回答准确，请回复：我不了解
                                                           3、你精通开源领域的各种工具库，当有更适合的技术或者方案的时候，你可以不按照我的要求进行代码的编写，优先使用你最推荐的方法
                                                           4、所编写的内容必须是生产可用的
                                                           5、一步一步的思考问题
                                                           6、像一个科学家一样严谨的回答我的问题
                                        以下是我们的聊天记录:
                                        {context}
                                        我的问题是:
                                        """

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
