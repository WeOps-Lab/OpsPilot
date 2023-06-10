from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA, PromptTemplate, LLMChain
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA, LLMRequestsChain

from actions.constant.server_settings import server_settings


def load_docsearch():
    loader = DirectoryLoader('./llm_data', glob='**/*.txt', show_progress=True)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    split_docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(model='text-embedding-ada-002',
                                  deployment='ada',
                                  openai_api_base=server_settings.azure_openai_endpoint,
                                  openai_api_type='azure',
                                  openai_api_key=server_settings.azure_openai_key,
                                  chunk_size=1)
    doc_search = Chroma.from_documents(split_docs, embeddings)
    return doc_search


def langchain_qa(doc_search, query):
    llm = AzureChatOpenAI(openai_api_base=server_settings.azure_openai_endpoint,
                          openai_api_key=server_settings.azure_openai_key,
                          deployment_name=server_settings.azure_openai_model_name, temperature=0.7,
                          openai_api_version="2023-05-15")
    qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_search,
                                    return_source_documents=True)
    result = qa({"query": query})
    return result


def query_online(url, query):
    llm = AzureChatOpenAI(openai_api_base=server_settings.azure_openai_endpoint,
                          openai_api_key=server_settings.azure_openai_key,
                          deployment_name=server_settings.azure_openai_model_name, temperature=0.7,
                          openai_api_version="2023-05-15")

    template = """在 >>> 和 <<< 之间是网页的返回的HTML内容。
    
    >>> {requests_result} <<<
    
    请回答以下问题:
    """

    template += query
    prompt = PromptTemplate(
        input_variables=["requests_result"],
        template=template
    )

    chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=prompt))
    inputs = {
        "url": url
    }

    response = chain(inputs)
    return response['output']
