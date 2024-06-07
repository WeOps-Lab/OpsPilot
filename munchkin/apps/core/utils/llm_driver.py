from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, \
    PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI

from apps.model_provider_mgmt.models import LLMModelChoices


class LLMDriver:
    def __init__(self, llm_model):
        self.llm_model = llm_model
        llm_config = llm_model.decrypted_llm_config
        if llm_model.llm_model == LLMModelChoices.CHAT_GPT:
            self.qa_client = OpenAI(
                openai_api_key=llm_config['openai_api_key'],
                openai_api_base=llm_config['openai_base_url'],
                temperature=llm_config['temperature'],
                model=llm_config['model']
            )
            self.client = ChatOpenAI(
                openai_api_key=llm_config['openai_api_key'],
                openai_api_base=llm_config['openai_base_url'],
                temperature=llm_config['temperature'],
                model=llm_config['model']
            )

    def get_qa_client(self):
        return self.client

    def chat(self, system_message_prompt, user_message):
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_prompt)

        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=self.client, prompt=chat_prompt)

        result = chain.run(user_message)
        return result

    def openai_chat_with_history(self,
                                 system_message_prompt, user_message,
                                 message_history, window_size=10,
                                 rag_content=''):

        if rag_content:
            system_message_prompt = f"\n\n背景知识:{rag_content}\n\n{system_message_prompt}"

        prompt = PromptTemplate(
            input_variables=["chat_history", "input"],
            template=system_message_prompt
        )
        memory = ConversationBufferWindowMemory(
            memory_key="chat_history", chat_memory=message_history, k=window_size
        )
        llm_chain = ConversationChain(llm=self.client, prompt=prompt, memory=memory, verbose=True)

        result = llm_chain.predict(input=user_message)
        return result
