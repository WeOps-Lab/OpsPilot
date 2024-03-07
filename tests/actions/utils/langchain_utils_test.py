from dotenv import load_dotenv
from loguru import logger
from actions.utils.langchain_utils import LangChainUtils


def test_chat_llm_with_memory():
    load_dotenv()
    result = LangChainUtils.chat_llm_with_memory('demo', '你是谁')
    logger.info(result)
