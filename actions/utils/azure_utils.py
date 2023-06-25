from langchain import LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from logzero import logger

from actions.constant.server_settings import server_settings


def query_chatgpt(system_message, user_message):
    logger.info(f'开始请求Azuer ChatGPT,system_prompt:[{system_message}],user_prompt:[{user_message}]')

    llm = AzureChatOpenAI(openai_api_base=server_settings.azure_openai_endpoint,
                          openai_api_key=server_settings.azure_openai_key,
                          deployment_name=server_settings.azure_openai_model_name,
                          temperature=server_settings.azure_openai_api_temperature,
                          openai_api_version=server_settings.azure_openai_api_version)

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(llm=llm, prompt=chat_prompt)
    result = chain.run(user_message)
    return result
