from dotenv import load_dotenv

from actions.utils.langchain_utils import LangChainUtils


def test_chat_llm_with_memory():
    load_dotenv()
    result = LangChainUtils.chat_llm_with_memory('demo', '你是谁')
    print(result)
