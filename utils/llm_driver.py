import json

import requests
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

    def rag_search(self, qeury):
        if server_settings.munchkin_api_key is None or server_settings.munchkin_base_url is None:
            return ""

        result = requests.post(server_settings.munchkin_base_url + "/api/rag_search",
                               headers={
                                   "Authorization": f"Token {server_settings.munchkin_api_key}",
                                   "Content-Type": "application/json"
                               }, data=json.dumps(
                {
                    "ids": [int(x) for x in server_settings.munchkin_knowledge_base_ids.split(",")],
                    "query": qeury
                }
            )).json()['context']
        content = ''
        for r in result:
            content += r.replace('{', '').replace('}', '') + '\n'
        return content

    def chat(self, system_message_prompt: str, user_message: str, enable_rag=False):

        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_prompt)

        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=self.client, prompt=chat_prompt)

        if enable_rag:
            rag_result = self.rag_search(user_message)
            user_message = f"\n\n背景知识:{rag_result}\n\n我的问题是:{user_message}"
        result = chain.run(user_message)
        return result

    def chat_with_history(self, system_message_prompt, query, message_history, window_size=10, enable_rag=True):
        prompt = PromptTemplate(
            input_variables=["chat_history", "input"],
            template=system_message_prompt
        )
        memory = ConversationBufferWindowMemory(
            memory_key="chat_history", chat_memory=message_history, k=window_size
        )
        llm_chain = ConversationChain(llm=self.client, prompt=prompt, memory=memory, verbose=True)

        if enable_rag:
            rag_result = self.rag_search(query)
            query = f"\n\n背景知识:{rag_result}\n\n我的问题是:{query}"
        answer = llm_chain.predict(input=query)
        return answer
