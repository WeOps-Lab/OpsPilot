import os
import shutil

import fire
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFium2Loader, UnstructuredMarkdownLoader, UnstructuredWordDocumentLoader, \
    UnstructuredPowerPointLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import MarkdownTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from loguru import logger
from tqdm import tqdm

from actions.constant.server_settings import server_settings
from actions.utils.indexer_utils import Searcher
from actions.utils.langchain_utils import langchain_qa
from actions.utils.redis_utils import RedisUtils


class BootStrap(object):
    def init_data(self, force=False):
        """
        初始化系统配置
        Args:
            force: 是否将所有系统设置调整为默认设置
        """
        RedisUtils.set_default_prompt(force)

    def query_embed_knowledge(self):
        """
        进入命令行模式进行本地知识问答
        """
        embeddings = HuggingFaceEmbeddings(model_name=server_settings.embed_model_name,
                                           cache_folder=server_settings.embed_model_cache_home,
                                           encode_kwargs={
                                               'show_progress_bar': True
                                           })
        doc_search = Chroma(persist_directory=server_settings.vec_db_path, embedding_function=embeddings)

        searcher = Searcher()

        while True:
            query = input("请输入问题（输入exit退出终端）：")
            if query == "exit":
                break

            prompt_template = RedisUtils.get_prompt_template()
            prompt_template = searcher.format_prompt(prompt_template, query)

            results = langchain_qa(doc_search, prompt_template, query)

            logger.info(f'回复:[{results["result"]}]')

    def embed_local_knowledge(self, knowledge_path: str, ):
        """
        索引目标路径下的文件，存放至向量数据库与倒排索引中
        Args:
            knowledge_path: 本地知识存放的绝对路径
        """

        logger.info('清理索引文件....')

        if os.path.exists(server_settings.vec_db_path):
            logger.info(f'清理语义向量数据库文件:[{server_settings.vec_db_path}]')
            shutil.rmtree(server_settings.vec_db_path)

        if os.path.exists(server_settings.indexer_db_path):
            logger.info(f'清理倒排索引数据库文件:[{server_settings.indexer_db_path}]')
            shutil.rmtree(server_settings.indexer_db_path)

        knowledge_files = []
        for root, dirs, files in os.walk(knowledge_path, topdown=False):
            for name in files:
                knowledge_files.append(os.path.join(root, name))

        knowledge_docs = []
        for knowledge_file in tqdm(knowledge_files, desc='索引文件中....'):
            if knowledge_file.lower().endswith(".md"):
                loader = UnstructuredMarkdownLoader(knowledge_file)
                text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=0)
                knowledge_docs += loader.load_and_split(text_splitter)
            elif knowledge_file.lower().endswith(".pdf"):
                loader = PyPDFium2Loader(knowledge_file)
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                knowledge_docs += loader.load_and_split(text_splitter)
            elif knowledge_file.lower().endswith(".docx"):
                loader = UnstructuredWordDocumentLoader(knowledge_file, mode="elements")
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                knowledge_docs += loader.load_and_split(text_splitter)
            elif knowledge_file.lower().endswith(".pptx"):
                loader = UnstructuredPowerPointLoader(knowledge_file, mode="elements")
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                knowledge_docs += loader.load_and_split(text_splitter)
        knowledge_contents = [x.page_content for x in knowledge_docs]

        logger.info('建立知识的语义索引......')
        embeddings = HuggingFaceEmbeddings(model_name=server_settings.embed_model_name,
                                           cache_folder=server_settings.embed_model_cache_home,
                                           encode_kwargs={
                                               'show_progress_bar': True
                                           })
        doc_search = Chroma.from_documents(knowledge_docs, embeddings, persist_directory=server_settings.vec_db_path)
        doc_search.persist()

        logger.info('建立知识内容的倒排索引.....')
        search = Searcher()
        search.index_knowledge(knowledge_contents)


if __name__ == '__main__':
    load_dotenv()
    os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', server_settings.embed_model_cache_home)
    fire.Fire(BootStrap)
