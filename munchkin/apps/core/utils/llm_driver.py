from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, \
    PromptTemplate
from langchain_openai import ChatOpenAI


class LLMDriver:
    def openai_chat(self, openai_base_url, openai_api_key,
                    system_message_prompt, user_message,
                    model="gpt-3.5-turbo-16k", temperature=0.7):
        client = ChatOpenAI(
            openai_api_key=openai_api_key,
            openai_api_base=openai_base_url,
            temperature=temperature,
            model=model
        )
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_prompt)

        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        chain = LLMChain(llm=client, prompt=chat_prompt)

        result = chain.run(user_message)
        return result

    def openai_chat_with_history(self, openai_base_url, openai_api_key,
                                 system_message_prompt, user_message,
                                 message_history, window_size=10,
                                 rag_content='',
                                 model="gpt-3.5-turbo-16k", temperature=0.7):
        client = ChatOpenAI(
            openai_api_key=openai_api_key,
            openai_api_base=openai_base_url,
            temperature=temperature,
            model=model
        )

        if rag_content:
            system_message_prompt = f"\n\n背景知识:{rag_content}\n\n{system_message_prompt}"

        prompt = PromptTemplate(
            input_variables=["chat_history", "input"],
            template=system_message_prompt
        )
        memory = ConversationBufferWindowMemory(
            memory_key="chat_history", chat_memory=message_history, k=window_size
        )
        llm_chain = ConversationChain(llm=client, prompt=prompt, memory=memory, verbose=True)

        result = llm_chain.predict(input=user_message)
        return result
