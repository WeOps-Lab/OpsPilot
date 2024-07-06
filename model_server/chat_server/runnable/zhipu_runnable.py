from typing import List

from langchain_core.runnables import RunnableLambda

from runnable.runnable_mixin import RunnableMixin
from user_types.zhipu_chat_request import ZhipuChatRequest
from utils.zhipu_driver import ZhipuDriver


class ZhipuRunnable(RunnableMixin):
    def chat(self, req: ZhipuChatRequest) -> List[float]:
        driver = ZhipuDriver(
            api_base=req.api_base,
            api_key=req.api_key,
            temperature=req.temperature,
            model=req.model,
        )
        return self.chat_llm(driver, req)

    def instance(self):
        runnable = RunnableLambda(self.chat).with_types(input_type=ZhipuChatRequest, output_type=str)
        return runnable
