import os
import openai
from langchain import LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from logzero import logger


def chat_with_azure_gpt():
    pass


def query_chatgpt(system_message, user_message):
    if os.getenv('RUN_MODE') == 'DEV':
        return "WeOps Debug Fallback"
    else:
        logger.info('开始请求Azuer ChatGPT.......')
        llm = AzureChatOpenAI(openai_api_base=os.getenv('AZURE_OPENAI_ENDPOINT'),
                              openai_api_key=os.getenv('AZURE_OPENAI_KEY'),
                              deployment_name="GPT35", temperature=0.7, openai_api_version="2023-05-15")
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=llm, prompt=chat_prompt)
        result = chain.run(user_message)
        return result
