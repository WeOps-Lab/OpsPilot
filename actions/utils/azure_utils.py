import os
from langchain.chat_models import AzureChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from logzero import logger


def query_chatgpt(messages):
    if os.getenv('RUN_MODE') == 'DEV':
        return "WeOps Debug Fallback"
    else:
        openai.api_key = os.getenv('AZURE_OPENAI_KEY')
        openai.api_base = os.getenv('AZURE_OPENAI_ENDPOINT')
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15'
        logger.info('开始请求Azuer ChatGPT.......')
        response = openai.ChatCompletion.create(
            engine=os.getenv('AZURE_OPENAI_MODEL_NAME'),
            messages=messages
        )
        text = response['choices'][0]['message']['content']
        # .replace('\n', '').replace(' .', '.').strip()
        logger.info(f'返回内容为:{text}')
        return text
