from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from core.server_settings import server_settings


class LLMDriver:
    def __init__(self, model="gpt-3.5-turbo-16k", temperature=0.7):
        self.client = ChatOpenAI(
            openai_api_key=server_settings.openai_api_key,
            openai_api_base=server_settings.openai_base_url,
            temperature=temperature,
            model=model
        )

    def chat(self, system_message_prompt: str, user_message: str):
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_prompt)

        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=self.client, prompt=chat_prompt)
        result = chain.run(user_message)
        return result

    def chat_with_history(self, system_message_prompt, query, message_history, window_size=10):
        prompt = PromptTemplate(
            input_variables=["chat_history", "input"],
            template=system_message_prompt
        )
        memory = ConversationBufferWindowMemory(
            memory_key="chat_history", chat_memory=message_history, k=window_size
        )
        llm_chain = ConversationChain(llm=self.client, prompt=prompt, memory=memory,verbose=True)
        answer = llm_chain.predict(input=query)
        return answer
