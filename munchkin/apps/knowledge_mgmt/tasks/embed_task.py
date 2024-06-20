import os.path
import tempfile

import chardet
import elasticsearch
from celery import shared_task
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchStore
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from loguru import logger
from tqdm import tqdm

from apps.knowledge_mgmt.loader.doc_loader import DocLoader
from apps.knowledge_mgmt.loader.image_loader import ImageLoader
from apps.knowledge_mgmt.loader.pdf_loader import PDFLoader
from apps.knowledge_mgmt.loader.ppt_loader import PPTLoader
from apps.knowledge_mgmt.loader.recursive_url_loader import RecursiveUrlLoader
from apps.knowledge_mgmt.models import FileKnowledge, KnowledgeBaseFolder, ManualKnowledge, WebPageKnowledge
from apps.model_provider_mgmt.services.embedding_service import EmbeddingService
from munchkin.components.elasticsearch import ELASTICSEARCH_PASSWORD, ELASTICSEARCH_URL

load_dotenv()


def embed_manual_knowledgebase(knowledge_base_folder, knowledge):
    docs = []
    if knowledge_base_folder.enable_general_parse:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=knowledge_base_folder.general_parse_chunk_size,
            chunk_overlap=knowledge_base_folder.general_parse_chunk_overlap,
        )
        docs += text_splitter.split_documents([Document(knowledge.content)])
    return docs


def embed_webpage_knowledgebase(knowledge_base_folder, knowledge):
    docs = []
    loader = RecursiveUrlLoader(knowledge.url, max_depth=knowledge.max_depth)
    web_docs = loader.load()
    transformer = BeautifulSoupTransformer()
    web_docs = transformer.transform_documents(web_docs)
    if knowledge_base_folder.enable_general_parse:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=knowledge_base_folder.general_parse_chunk_size,
            chunk_overlap=knowledge_base_folder.general_parse_chunk_overlap,
        )
        docs += text_splitter.split_documents(web_docs)
    return docs


def embed_file_knowledgebase(knowledge_base_folder, knowledge):
    with tempfile.NamedTemporaryFile(delete=False) as f:

        docs = []
        # 获取文件类型
        file_type = os.path.splitext(knowledge.file.name)[1]

        if file_type in [".md"]:
            # 读取文件内容到临时文件
            content = knowledge.file.read()
            detected = chardet.detect(content)
            decoded_content = content.decode(detected['encoding'])
        else:
            f.write(knowledge.file.read())

        if file_type == ".md":
            # TODO: 需要把Markdown转换为PDF，统一用PDF格式进行处理
            # TODO: 切分模式现在被固定为了single，需要修改为参数
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]

            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
            md_header_splits = markdown_splitter.split_text(decoded_content)

            # 提取所有表格
            if knowledge_base_folder.enable_general_parse:
                # 使用循环分块进行切分
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=knowledge_base_folder.general_parse_chunk_size,
                    chunk_overlap=knowledge_base_folder.general_parse_chunk_overlap,
                )
                docs += text_splitter.split_documents(md_header_splits)
            if knowledge_base_folder.enable_semantic_chunck_parse:
                semantic_chunker = SemanticChunker(
                    embeddings=embedding_service.get_embedding(
                        knowledge_base_folder.semantic_chunk_parse_embedding_model)
                )
                docs += semantic_chunker.split_documents(md_header_splits)
            return docs

        if file_type in [".ppt", ".pptx"]:
            loader = PPTLoader(f.name, mode="single")
        if file_type in [".pdf"]:
            loader = PDFLoader(f.name, mode="single")
        if file_type in [".jpg", ".png"]:
            loader = ImageLoader(f.name, mode="single")
        if file_type in [".doc", ".docx"]:
            loader = DocLoader(f.name, mode="single")
        else:
            loader = UnstructuredFileLoader(f.name, mode="single")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=knowledge_base_folder.general_parse_chunk_size,
            chunk_overlap=knowledge_base_folder.general_parse_chunk_overlap,
        )
        if knowledge_base_folder.enable_general_parse:
            docs += text_splitter.split_documents(loader.load())
        if knowledge_base_folder.enable_semantic_chunck_parse:
            semantic_chunker = SemanticChunker(
                embeddings=embedding_service.get_embedding(knowledge_base_folder.semantic_chunk_parse_embedding_model)
            )
            docs += semantic_chunker.split_documents(loader.load())

        return docs


@shared_task
def general_embed(knowledge_base_folder_id):
    logger.info(f"开始生成知识库[{knowledge_base_folder_id}]的Embedding索引")

    knowledge_base_folder = KnowledgeBaseFolder.objects.get(id=knowledge_base_folder_id)
    index_name = knowledge_base_folder.knowledge_index_name()

    logger.info(f"初始化索引: {index_name}")
    es = elasticsearch.Elasticsearch(hosts=[ELASTICSEARCH_URL], basic_auth=("elastic", ELASTICSEARCH_PASSWORD))

    if es.indices.exists(index=index_name):
        logger.info(f"删除已存在的索引: {index_name}")
        es.indices.delete(index=index_name)

    try:
        knowledge_base_folder.train_status = 1
        knowledge_base_folder.train_progress = 0
        knowledge_base_folder.save()

        logger.info(f"获取Embedding模型: {knowledge_base_folder.embed_model}")

        knowledges = []

        file_knowledges = FileKnowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()
        logger.info(f"知识库[{knowledge_base_folder_id}]包含[{len(file_knowledges)}]个文件知识")
        for obj in file_knowledges:
            knowledges.append(obj)

        manual_knowledges = ManualKnowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()
        logger.info(f"知识库[{knowledge_base_folder_id}]包含[{len(manual_knowledges)}]个手动知识")
        for obj in manual_knowledges:
            knowledges.append(obj)

        web_page_knowledges = WebPageKnowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()
        logger.info(f"知识库[{knowledge_base_folder_id}]包含[{len(web_page_knowledges)}]个网页知识")
        for obj in web_page_knowledges:
            knowledges.append(obj)

        total_knowledges = len(knowledges)
        for index, knowledge in tqdm(enumerate(knowledges)):
            knowledge_docs = []
            if isinstance(knowledge, FileKnowledge):
                logger.debug(f"开始处理文件知识: {knowledge.title}")
                knowledge_docs += embed_file_knowledgebase(knowledge_base_folder, knowledge)
                for doc in knowledge_docs:
                    doc.metadata["knowledge_type"] = "file"
                logger.info(f"文件知识[{knowledge.title}]共提取[{len(knowledge_docs)}]个文档片段")

            elif isinstance(knowledge, ManualKnowledge):
                logger.debug(f"开始处理手动知识: {knowledge.title}")
                knowledge_docs += embed_manual_knowledgebase(knowledge_base_folder, knowledge)
                for doc in knowledge_docs:
                    doc.metadata["knowledge_type"] = "manual"
                logger.info(f"手动知识[{knowledge.title}]共提取[{len(knowledge_docs)}]个文档片段")

            elif isinstance(knowledge, WebPageKnowledge):
                logger.debug(f"开始处理网页知识: {knowledge.title}")
                knowledge_docs += embed_webpage_knowledgebase(knowledge_base_folder, knowledge)
                for doc in knowledge_docs:
                    doc.metadata["knowledge_type"] = "webpage"
                logger.info(f"网页知识[{knowledge.title}]共提取[{len(knowledge_docs)}]个文档片段")

            for doc in knowledge_docs:
                doc.metadata["knowledge_id"] = knowledge.id
                doc.metadata["knowledge_folder_id"] = knowledge_base_folder_id
                doc.metadata["knowledge_title"] = knowledge.title
                for key, value in knowledge.custom_metadata.items():
                    doc.metadata[key] = value

            logger.debug(f"开始生成知识库[{knowledge_base_folder_id}]的Embedding索引")
            embedding_service = EmbeddingService(embed_provider=knowledge_base_folder.embed_model)
            for doc in tqdm(knowledge_docs):
                vector = embedding_service.embed_content(doc.page_content)
                # 使用es客户端，把数据写入到es中，vector一列，text一列，metadata一列，source一列
                es.index(index=index_name, body={
                    "vector": vector,
                    "text": doc.page_content,
                    "metadata": doc.metadata,
                })
            # 刷新es索引
            es.indices.refresh(index=index_name)

            progress = round((index + 1) / total_knowledges * 100, 2)
            logger.debug(f"知识库[{knowledge_base_folder_id}]的Embedding索引生成进度: {progress:.2f}%")
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
