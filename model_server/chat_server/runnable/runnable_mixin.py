from langchain.memory import ChatMessageHistory

from user_types.base_chat_request import BaseChatRequest
from loguru import logger


class RunnableMixin:

    def chat_llm(self, driver, req: BaseChatRequest):
        if req.chat_history:
            llm_chat_history = ChatMessageHistory()
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
            logger.info(
                f"多轮对话模式 系统信息: {req.system_message_prompt} 引用知识:{req.rag_context} 用户信息: {req.user_message} 结果: {result}")
            return result
        else:
            system_skill_prompt = req.system_message_prompt.replace("{", "").replace("}", "")
            result = driver.chat(
                system_message_prompt=system_skill_prompt,
                user_message=req.user_message,
            )
            logger.info(
                f"单轮对话模式 系统信息: {system_skill_prompt} 用户信息: {req.user_message} 结果: {result}"
            )
            return result
