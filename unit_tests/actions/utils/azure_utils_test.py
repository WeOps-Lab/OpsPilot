from actions.utils.azure_utils import query_chatgpt
from logzero import logger


def test_chat_with_azure_gpt():
    logger.info(query_chatgpt("扮演专业的Python开发工程师", "如何学习Python"))
