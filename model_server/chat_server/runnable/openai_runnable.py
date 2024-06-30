from typing import List

from langchain_core.runnables import RunnableLambda

from user_types.openai_chat_request import OpenAIChatRequest
from utils.openai_driver import OpenAIDriver
from langchain.memory import ChatMessageHistory


class OpenAIRunnable:
    def openai_chat(self, req: OpenAIChatRequest) -> List[float]:
        driver = OpenAIDriver(
            openai_api_key=req.openai_api_key,
            openai_base_url=req.openai_api_base,
            temperature=req.temperature,
            model=req.model,
        )

        llm_chat_history = ChatMessageHistory()
        if req.chat_history:
            for event in req.chat_history:
                if event.event == "user":
                    llm_chat_history.add_user_message(event.text)
                elif event.event == "bot":
                    llm_chat_history.add_ai_message(event.text)

            result = driver.chat_with_history(
                system_message_prompt=req.system_message_prompt,
                user_message=req.user_message,
                message_history=llm_chat_history,
                window_size=req.conversation_window_size,
                rag_content=req.rag_context,
            )
            return result
        else:
            system_skill_prompt = req.system_message_prompt.replace("{", "").replace("}", "")
            result = driver.chat(
                system_message_prompt=system_skill_prompt,
                user_message=req.user_message,
            )
            return result

    def instance(self):
        runnable = RunnableLambda(self.openai_chat).with_types(input_type=OpenAIChatRequest, output_type=str)
        return runnable
