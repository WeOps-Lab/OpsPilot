import os

import fire
from langchain.document_loaders import PyPDFium2Loader, UnstructuredFileLoader, TextLoader, UnstructuredMarkdownLoader
from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import MarkdownTextSplitter, SentenceTransformersTokenTextSplitter, \
    RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from tqdm import tqdm

from actions.utils.langchain_utils import langchain_qa
from actions.utils.redis_utils import RedisUtils


class BootStrap(object):
    def init_data(self):
        RedisUtils.set_default_prompt()

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

        prompt_template = RedisUtils.get_prompt_template()
        while True:
            query = input("请输入问题（输入exit退出终端）：")
            if query == "exit":
                break
            # print(doc_search.similarity_search(query,k=5))
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

    def embed_local_knowledge(self, knowledge_path: str,
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
        knowledge_files = []
        for root, dirs, files in os.walk(knowledge_path, topdown=False):
            for name in files:
                knowledge_files.append(os.path.join(root, name))

        knowledge_docs = []
        for knowledge_file in tqdm(knowledge_files):
            if knowledge_file.lower().endswith(".md"):
                loader = UnstructuredMarkdownLoader(knowledge_file)
                text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=0)
                knowledge_docs += loader.load_and_split(text_splitter)
            elif knowledge_file.lower().endswith(".pdf"):
                loader = PyPDFium2Loader(knowledge_file)
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                knowledge_docs += loader.load_and_split(text_splitter)
        embeddings = HuggingFaceEmbeddings(model_name=model_name, cache_folder=cache_folder,
                                           encode_kwargs={
                                               'show_progress_bar': True
                                           })
        doc_search = Chroma.from_documents(knowledge_docs, embeddings, persist_directory=vec_db_path)
        doc_search.persist()


if __name__ == '__main__':
    os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', './cache/models')
    fire.Fire(BootStrap)
