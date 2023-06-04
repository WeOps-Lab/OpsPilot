import os

from langchain import LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from actions.utils.azure_utils import query_chatgpt


def test_chat_with_azure_gpt():
    print(query_chatgpt("扮演专业的Python开发工程师", "如何学习Python"))
