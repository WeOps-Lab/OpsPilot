import os.path
import tempfile

import elasticsearch
from celery import shared_task
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader, AsyncHtmlLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchStore
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from loguru import logger
from tqdm import tqdm

from apps.core.utils.embedding_driver import EmbeddingDriver
from apps.knowledge_mgmt.models import KnowledgeBaseFolder, FileKnowledge, ManualKnowledge, WebPageKnowledge
from munchkin.components.elasticsearch import ELASTICSEARCH_URL, ELASTICSEARCH_PASSWORD

load_dotenv()


def embed_manual_knowledgebase(knowledge_base_folder, knowledge):
    docs = []
    if knowledge_base_folder.enable_general_parse:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=knowledge_base_folder.general_parse_chunk_size,
                                                       chunk_overlap=knowledge_base_folder.general_parse_chunk_overlap)
        docs += text_splitter.split_documents([Document(knowledge.content)])
    return docs


def embed_webpage_knowledgebase(knowledge_base_folder, knowledge):
    docs = []
    loader = AsyncHtmlLoader(knowledge.url)
    web_docs = loader.load()
    transformer = BeautifulSoupTransformer()
    web_docs = transformer.transform_documents(web_docs)
    if knowledge_base_folder.enable_general_parse:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=knowledge_base_folder.general_parse_chunk_size,
            chunk_overlap=knowledge_base_folder.general_parse_chunk_overlap)
        docs += text_splitter.split_documents(web_docs)
    return docs


def embed_file_knowledgebase(knowledge_base_folder, knowledge):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        # 读取文件内容到临时文件
        content = knowledge.file.read()
        f.write(content)

        docs = []
        # 获取文件类型
        file_type = os.path.splitext(knowledge.file.name)[1]

        if file_type == '.md':
            # TODO: 需要把Markdown转换为PDF，统一用PDF格式进行处理
            # TODO: 切分模式现在被固定为了single，需要修改为参数
            loader = UnstructuredMarkdownLoader(f.name, mode='single')
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]

            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
            md_header_splits = markdown_splitter.split_text(loader.load()[0].page_content)

            if knowledge_base_folder.enable_general_parse:
                # 使用循环分块进行切分
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=knowledge_base_folder.general_parse_chunk_size,
                    chunk_overlap=knowledge_base_folder.general_parse_chunk_overlap)
                docs += text_splitter.split_documents(md_header_splits)
        else:
            # TODO:针对 PPT、Word、Excel、PDF，分别有不同的处理方式，需要更加精细化的处理
            # TODO: 切分模式现在被固定为了single，需要修改为参数
            loader = UnstructuredFileLoader(f.name, mode='single')
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=knowledge_base_folder.general_parse_chunk_size,
                                                           chunk_overlap=knowledge_base_folder.general_parse_chunk_overlap)
            if knowledge_base_folder.enable_general_parse:
                docs += text_splitter.split_documents(loader.load())
        return docs


@shared_task
def general_embed(knowledge_base_folder_id):
    logger.info(f'开始生成知识库[{knowledge_base_folder_id}]的Embedding索引')

    knowledge_base_folder = KnowledgeBaseFolder.objects.get(id=knowledge_base_folder_id)
    index_name = knowledge_base_folder.knowledge_index_name()

    logger.info(f'初始化索引: {index_name}')
    es = elasticsearch.Elasticsearch(hosts=[ELASTICSEARCH_URL],
                                     basic_auth=('elastic', ELASTICSEARCH_PASSWORD))

    if es.indices.exists(index=index_name):
        logger.info(f'删除已存在的索引: {index_name}')
        es.indices.delete(index=index_name)

    try:
        knowledge_base_folder.train_status = 1
        knowledge_base_folder.train_progress = 0
        knowledge_base_folder.save()

        logger.info(f'获取Embedding模型: {knowledge_base_folder.embed_model}')
        embedding = EmbeddingDriver().get_embedding(knowledge_base_folder.embed_model)

        knowledges = []

        file_knowledges = FileKnowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()
        logger.info(f'知识库[{knowledge_base_folder_id}]包含[{len(file_knowledges)}]个文件知识')
        for obj in file_knowledges:
            knowledges.append(obj)

        manual_knowledges = ManualKnowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()
        logger.info(f'知识库[{knowledge_base_folder_id}]包含[{len(manual_knowledges)}]个手动知识')
        for obj in manual_knowledges:
            knowledges.append(obj)

        web_page_knowledges = WebPageKnowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()
        logger.info(f'知识库[{knowledge_base_folder_id}]包含[{len(web_page_knowledges)}]个网页知识')
        for obj in web_page_knowledges:
            knowledges.append(obj)

        total_knowledges = len(knowledges)
        for index, knowledge in tqdm(enumerate(knowledges)):
            knowledge_docs = []
            if knowledge_base_folder.enable_general_parse:
                if isinstance(knowledge, FileKnowledge):
                    logger.debug(f'开始处理文件知识: {knowledge.title}')
                    knowledge_docs += embed_file_knowledgebase(knowledge_base_folder, knowledge)
                    logger.info(f'文件知识[{knowledge.title}]共提取[{len(knowledge_docs)}]个文档片段')

                elif isinstance(knowledge, ManualKnowledge):
                    logger.debug(f'开始处理手动知识: {knowledge.title}')
                    knowledge_docs += embed_manual_knowledgebase(knowledge_base_folder, knowledge)

                    logger.info(f'手动知识[{knowledge.title}]共提取[{len(knowledge_docs)}]个文档片段')

                elif isinstance(knowledge, WebPageKnowledge):
                    logger.debug(f'开始处理网页知识: {knowledge.title}')
                    knowledge_docs += embed_webpage_knowledgebase(knowledge_base_folder, knowledge)
                    logger.info(f'网页知识[{knowledge.title}]共提取[{len(knowledge_docs)}]个文档片段')

            for doc in knowledge_docs:
                doc.metadata['knowledge_id'] = knowledge.id
                doc.metadata['knowledge_folder_id'] = knowledge_base_folder_id
                for key, value in knowledge.custom_metadata.items():
                    doc.metadata[key] = value

            logger.debug(f'开始生成知识库[{knowledge_base_folder_id}]的Embedding索引')
            db = ElasticsearchStore.from_documents(knowledge_docs, embedding, es_connection=es,
                                                   index_name=index_name)
            db.client.indices.refresh(index=index_name)

            progress = round((index + 1) / total_knowledges * 100, 2)
            logger.debug(f'知识库[{knowledge_base_folder_id}]的Embedding索引生成进度: {progress:.2f}%')
            knowledge_base_folder.train_progress = progress
            knowledge_base_folder.save()

        knowledge_base_folder.train_status = 2
        knowledge_base_folder.train_progress = 100
        knowledge_base_folder.save()

    except Exception as e:
        logger.exception(e)

        knowledge_base_folder.train_status = 3
        knowledge_base_folder.train_progress = 100
        knowledge_base_folder.save()
