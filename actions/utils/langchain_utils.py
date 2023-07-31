import trafilatura
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.agents import AgentType, initialize_agent
from langchain.chains import RetrievalQA, GraphCypherQAChain
from langchain.chat_models import ChatOpenAI
from langchain.graphs import Neo4jGraph
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.tools import Tool
from langchain.utilities import BingSearchAPIWrapper
from rasa_sdk import logger
from trafilatura.settings import use_config

from actions.constant.server_settings import server_settings


def langchain_qa(doc_search, prompt_template, query):
    llm = ChatOpenAI(openai_api_key=server_settings.openai_key,
                     openai_api_base=server_settings.openai_endpoint,
                     temperature=server_settings.openai_api_temperature)
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": prompt, "verbose": True}

    retriever = doc_search.as_retriever()
    retriever.search_kwargs = {'k': 3}
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                     return_source_documents=True, chain_type_kwargs=chain_type_kwargs)
    qa.verbose = True
    result = qa({"query": query})
    return result


def query_online(url, query):
    config = use_config()
    config.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")
    result = trafilatura.extract(trafilatura.fetch_url(url), config=config)

    template = f"""在 >>> 和 <<< 之间是网页的返回的HTML内容。
    
    >>> {result} <<<
    
    请回答以下问题:
    """
    return query_chatgpt(template, query)


def chat_online(query):
    llm = ChatOpenAI(openai_api_key=server_settings.openai_key,
                     openai_api_base=server_settings.openai_endpoint,
                     temperature=server_settings.openai_api_temperature)

    search = BingSearchAPIWrapper(bing_subscription_key=server_settings.bing_search_key,
                                  bing_search_url=server_settings.bing_search_url)
    tools = [
        Tool.from_function(
            func=search.run,
            name="Search",
            description="useful for when you need to answer questions about current events"
        ),
    ]

    PREFIX = '''You are an AI data scientist. 
    You have done years of research in studying all the AI algorthims. 
    You also love to write.
     On free time you write blog post for articulating what you have learned about different AI algorithms.
      Do not forget to include information on the algorithm's benefits, disadvantages, and applications.
       Additionally, the blog post should explain how the algorithm advances model reasoning by a whopping 70% and how it is a plug in and play version,
        connecting seamlessly to other components.
    '''

    FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:
    '''
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    '''

    When you have gathered all the information regarding AI algorithm, just write it to the user in the form of a blog post.

    '''
    Thought: Do I need to use a tool? No
    AI: [write a blog post]
    '''
    """

    SUFFIX = '''

    Begin!

    Previous conversation history:
    {chat_history}

    Instructions: {input}
    {agent_scratchpad}
    '''
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
                             prefix=PREFIX,
                             suffix=SUFFIX,
                             format_instructions=FORMAT_INSTRUCTIONS
                             )
    return agent.run(query)


def query_chatgpt(system_message, user_message):
    logger.info(f'开始请求ChatGPT,system_prompt:[{system_message}],user_prompt:[{user_message}]')

    llm = ChatOpenAI(openai_api_key=server_settings.openai_key,
                     openai_api_base=server_settings.openai_endpoint,
                     temperature=server_settings.openai_api_temperature)

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(llm=llm, prompt=chat_prompt)

    result = chain.run(user_message)
    return result


def graph_db_chat(query):
    llm = ChatOpenAI(openai_api_key=server_settings.openai_key,
                     openai_api_base=server_settings.openai_endpoint,
                     temperature=server_settings.openai_api_temperature)
    graph = Neo4jGraph(
        url=server_settings.neo4j_url, username=server_settings.neo4j_username, password=server_settings.neo4j_password
    )
    chain = GraphCypherQAChain.from_llm(
        llm, graph=graph, verbose=True
    )
    chain.verbose = True
    return chain.run(query)


def query_chatgpt_with_memory(user_id, query, ttl=300):
    """通过redis存储用户会话，实现对chatgpt的多轮问答

    Args:
        user_id (str): 企微用户ID
        query (str): 用户问题
        ttl (int, optional): 用户会话过期时间，单位秒. Defaults to 300.

    Returns:
        str: 基于历史问答信息的回答
    """
    template = """
    You are ChatGPT, a large language model trained by OpenAI. Answer as detailed as possible and use Chinese to answer.

    {chat_history}
    Question: {input}
    """

    prompt = PromptTemplate(
        input_variables=["chat_history", "input"], template=template
    )
    message_history = RedisChatMessageHistory(
        url=f"redis://{server_settings.redis_password}@{server_settings.redis_host}:{server_settings.redis_port}/{server_settings.redis_db}",
        ttl=ttl,
        session_id=user_id,
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history", chat_memory=message_history
    )
    llm_chain = LLMChain(
        llm=ChatOpenAI(
            openai_api_key=server_settings.openai_key,
            openai_api_base=server_settings.openai_endpoint,
            temperature=server_settings.openai_api_temperature,
        ),
        prompt=prompt,
        memory=memory,
        verbose=False,
    )
    answer = llm_chain.predict(input=query)
    return answer.replace("AI: ", "")
