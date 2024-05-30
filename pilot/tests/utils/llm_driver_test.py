from utils.llm_driver import LLMDriver
from loguru import logger


def test_chat():
    llm = LLMDriver()
    logger.info(llm.chat('', '你好'))
