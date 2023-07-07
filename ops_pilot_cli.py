import fire
from langchain.document_loaders import DirectoryLoader, RecursiveUrlLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import MarkdownTextSplitter, TokenTextSplitter, SentenceTransformersTokenTextSplitter
from langchain.vectorstores import Chroma
import os
from logzero import logger
from actions.constant.server_settings import server_settings
from actions.utils.langchain_utils import langchain_qa
import redis


class BootStrap(object):
    def init_data(self):
        redis_pool = redis.ConnectionPool(host=server_settings.redis_host,
                                          port=server_settings.redis_port,
                                          db=server_settings.redis_db,
                                          password=server_settings.redis_password)
        redis_client = redis.Redis(connection_pool=redis_pool)
        logger.info('初始化OpsPilot默认参数')
        redis_client.set('fallback_prompt', '扮演专业的运维工程师')
        redis_client.set('prompt_template', """Use the following pieces of context to answer the question at the end.
     If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer in Chinese:""")
        logger.info('参数初始化完成')

    def query_embed_knowledge(self, model_name: str = 'shibing624/text2vec-base-chinese',
                              cache_folder='cache/models', vec_db_path: str = 'vec_db'):
        """
        进入命令行模式进行本地知识问答
         Args:
            vec_db_path: 向量数据库存放的路径
            model_name: Embedding所使用的模型名称
            cache_folder: Embedding所使用模型缓存的路径
        """
        embeddings = HuggingFaceEmbeddings(model_name=model_name, cache_folder=cache_folder,
                                           encode_kwargs={
                                               'show_progress_bar': True
                                           })
        doc_search = Chroma(persist_directory=vec_db_path, embedding_function=embeddings)

        redis_pool = redis.ConnectionPool(host=server_settings.redis_host,
                                          port=server_settings.redis_port,
                                          db=server_settings.redis_db,
                                          password=server_settings.redis_password)
        redis_client = redis.Redis(connection_pool=redis_pool)
        prompt_template = redis_client.get('prompt_template').decode('utf-8')
        while True:
            query = input("请输入问题（输入exit退出终端）：")
            if query == "exit":
                break
            results = langchain_qa(doc_search, prompt_template, query)
            print(results['result'])

    def embed_website_knowledge(self, url: str,
                                vec_db_path: str = 'vec_db', model_name: str = 'shibing624/text2vec-base-chinese',
                                cache_folder='cache/models'):
        """
        索引目标网站的信息，存放至Chroma的索引中
        Args:
            knowledge_path: 目标网站地址
            vec_db_path: 向量数据库存放的路径
            model_name: Embedding所使用的模型名称
            cache_folder: Embedding所使用模型缓存的路径
        """
        loader = RecursiveUrlLoader(url=url)
        documents = loader.load()

        text_splitter = SentenceTransformersTokenTextSplitter(model_name=model_name)
        split_docs = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name=model_name, cache_folder=cache_folder,
                                           encode_kwargs={
                                               'show_progress_bar': True
                                           })
        doc_search = Chroma.from_documents(split_docs, embeddings, persist_directory=vec_db_path)
        doc_search.persist()

    def embed_local_knowledge(self, knowledge_path: str, file_glob: str = '**/*.md',
                              vec_db_path: str = 'vec_db', model_name: str = 'shibing624/text2vec-base-chinese',
                              cache_folder='cache/models'):
        """
        索引目标路径下的文件，存放至Chroma的索引中
        Args:
            knowledge_path: 本地知识存放的绝对路径
            file_glob: 指定使用哪种glob查找knowledge_path目录下的本地知识
            vec_db_path: 向量数据库存放的路径
            model_name: Embedding所使用的模型名称
            cache_folder: Embedding所使用模型缓存的路径
        """
        loader = DirectoryLoader(knowledge_path, glob=file_glob, show_progress=True)
        documents = loader.load()

        text_splitter = MarkdownTextSplitter()
        split_docs = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name=model_name, cache_folder=cache_folder,
                                           encode_kwargs={
                                               'show_progress_bar': True
                                           })
        doc_search = Chroma.from_documents(split_docs, embeddings, persist_directory=vec_db_path)
        doc_search.persist()


if __name__ == '__main__':
    os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', './cache/models')
    fire.Fire(BootStrap)
