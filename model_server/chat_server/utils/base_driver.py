from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from loguru import logger


class BaseDriver:
    def chat(self, system_message_prompt, user_message):
        try:
            system_message_prompt = SystemMessagePromptTemplate.from_template(
                system_message_prompt
            )

            human_template = "{text}"
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt, human_message_prompt]
            )
            chain = LLMChain(llm=self.client, prompt=chat_prompt)

            result = chain.run(user_message)
            return result
        except Exception as e:
            logger.error(f"聊天出错: {e}")
            return f"服务端异常:{e}"

    def chat_with_history(
            self,
            system_message_prompt,
            user_message,
            message_history,
            window_size=10,
            rag_content="",
    ):
        try:
            prompt = PromptTemplate(
                input_variables=["chat_history", "input"], template=system_message_prompt
            )
            memory = ConversationBufferWindowMemory(
                memory_key="chat_history", chat_memory=message_history, k=window_size
            )
            llm_chain = ConversationChain(
                llm=self.client, prompt=prompt, memory=memory, verbose=True
            )

            user_message = f"{rag_content} {user_message}"
            result = llm_chain.predict(input=user_message)
            return result
        except Exception as e:
            logger.error(f"聊天出错: {e}")
            return f"服务端异常:{e}"
