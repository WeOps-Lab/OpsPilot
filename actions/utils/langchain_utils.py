from operator import itemgetter

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

from actions.constants.server_settings import server_settings


class LangChainUtils:

    @staticmethod
    def chat_llm_with_memory(user_id, message):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are helpful ai helper, a large language model trained by OpenAI. Answer as detailed as possible and use Chinese to answer.",
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )

        message_history = RedisChatMessageHistory(
            url=f"redis://:{server_settings.redis_password}@{server_settings.redis_host}:{server_settings.redis_port}/{server_settings.redis_db}",
            ttl=300,
            session_id=user_id,
        )

        memory = ConversationBufferMemory(
            memory_key="history", chat_memory=message_history, return_messages=True
        )

        llm = ChatOpenAI(
            openai_api_key=server_settings.openai_key,
            openai_api_base=server_settings.openai_endpoint,
            temperature=server_settings.openai_api_temperature,
        )

        llm_chain = (
            RunnablePassthrough.assign(
                history=RunnableLambda(memory.load_memory_variables)
                | itemgetter("history")
            )
            | prompt
            | llm
            | StrOutputParser()
        )

        inputs = {"input": message}
        response = llm_chain.invoke(inputs)
        memory.save_context(inputs, {"output": response})
        return response
