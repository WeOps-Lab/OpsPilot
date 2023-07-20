import os
import shutil

import fire
from dotenv import load_dotenv
import pandas as pd
import sqlalchemy
from langchain import FAISS
from langchain.document_loaders import PyPDFium2Loader, UnstructuredMarkdownLoader, UnstructuredWordDocumentLoader, \
    UnstructuredPowerPointLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import MarkdownTextSplitter, RecursiveCharacterTextSplitter
from loguru import logger
from tqdm import tqdm

from actions.constant.server_settings import server_settings
from actions.utils.indexer_utils import Searcher
from actions.utils.langchain_utils import langchain_qa
from actions.utils.redis_utils import RedisUtils
from channels.enterprise_wechat_mysql import create_mysql_engine, mysql_connect


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
        doc_search = FAISS.load_local(server_settings.vec_db_path, embeddings)

        searcher = Searcher()

        while True:
            query = input("请输入问题（输入exit退出终端）：")
            if query == "exit":
                break

            prompt_template = RedisUtils.get_prompt_template()
            prompt_template = searcher.format_prompt(prompt_template, query)

            results = langchain_qa(doc_search, prompt_template, query)

            logger.info(f'回复:[{results["result"]}]')

    def embed_local_knowledge(self, knowledge_path: str):
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
        faiss_db = FAISS.from_documents(knowledge_docs, embeddings)
        faiss_db.save_local(folder_path=server_settings.vec_db_path)
        logger.info('建立知识内容的倒排索引.....')
        search = Searcher()
        search.index_knowledge(knowledge_contents)

    def init_db_table(self):
        """根据企微后台通讯录应用导出的excel，将其中用于一键拉群的字段写入mysql；
        函数包括建库、建表、导入三部分
        """
        # 数据库连接，无数据库
        db, cursor = mysql_connect(exist_db=False)

        create_db_sql = """CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;""".format(
            MYSQL_DATABASE
        )
        try:
            cursor.execute(create_db_sql)
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        # 关闭数据库连接
        db.close()

        # 建立数据表，有数据库名
        db, cursor = mysql_connect()
        create_table_sql = """CREATE TABLE `qywx_contacts` (
            `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT COMMENT '默认主键',
            `user_id` varchar(20) NOT NULL DEFAULT '' COMMENT '帐号',
            `name` varchar(16) NOT NULL DEFAULT '' COMMENT '姓名',
            `sex` char(2) DEFAULT '' COMMENT '性别',
            `department` varchar(100) DEFAULT '' COMMENT '部门',
            `phone_number` varchar(20) DEFAULT '' COMMENT '手机',
            `email` varchar(50) DEFAULT '' COMMENT '企业邮箱',
            
            PRIMARY KEY (`id`),
            KEY `k_name` (`name`)
            ) CHARSET=utf8 COMMENT='企微通讯录';""".format(
            MYSQL_DATABASE
        )
        try:
            cursor.execute(create_table_sql)
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        # 关闭数据库连接
        db.close()


    def contacts_to_mysql(self, contacts_path):
        """将通讯录相关字段写入Mysql

        Args:
            contacts_path (str): 企微后台导出的通讯录的地址，类似"../XX公司通讯录.xlsx"
        """
        conn = create_mysql_engine()
        contacts_df = pd.read_excel(
            contacts_path,
            engine="openpyxl",
            header=9,
            usecols=["帐号", "姓名", "性别", "部门", "手机", "企业邮箱"],
            index_col=None
        )
        contacts_df = contacts_df.reset_index(drop=True)
        contacts_df = contacts_df.rename(columns={"帐号":"user_id", "姓名":"name", "性别":"sex", "部门":"department", "手机":"phone_number", "企业邮箱":"email"})
        contacts_df.to_sql(
            "qywx_contacts",
            con=conn,
            if_exists="append",
            dtype={
                "user_id": sqlalchemy.VARCHAR(length=30),
                "name": sqlalchemy.VARCHAR(length=16),
                "sex": sqlalchemy.CHAR(length=2),
                "department": sqlalchemy.VARCHAR(length=100),
                "phone_number": sqlalchemy.VARCHAR(length=20),
                "email": sqlalchemy.VARCHAR(length=50)
            },
            index=False
        )



if __name__ == '__main__':
    load_dotenv()
    os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', server_settings.embed_model_cache_home)
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    fire.Fire(BootStrap)
