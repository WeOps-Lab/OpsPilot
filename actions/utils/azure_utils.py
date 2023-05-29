import os
import openai
from logzero import logger

from dotenv import load_dotenv

load_dotenv()


def query_chatgpt(promot):
    openai.api_key = os.getenv('AZURE_OPENAI_KEY')
    openai.api_base = os.getenv('AZURE_OPENAI_ENDPOINT')
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'
    logger.info('开始请求Azuer ChatGPT.......')
    response = openai.ChatCompletion.create(
        engine=os.getenv('AZURE_OPENAI_MODEL_NAME'),
        messages=[
            {"role": "user", "content": promot},
        ]
    )
    text = response['choices'][0]['message']['content']
    # .replace('\n', '').replace(' .', '.').strip()
    logger.info(f'返回内容为:{text}')
    return text
