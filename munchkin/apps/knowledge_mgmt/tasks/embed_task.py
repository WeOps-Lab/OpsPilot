import os.path
import tempfile

import elasticsearch
from celery import shared_task
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_elasticsearch import ElasticsearchStore
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from loguru import logger

from apps.knowledge_mgmt.models import KnowledgeBaseFolder, FileKnowledge
from apps.knowledge_mgmt.utils import get_index_name
from apps.model_provider_mgmt.models import EmbedModelChoices
from munchkin.components.elasticsearch import ELASTICSEARCH_URL, ELASTICSEARCH_PASSWORD

load_dotenv()


def train_file_knowledgebase(knowledge, chunk_size, chunk_overlap):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        content = knowledge.file.read()
        f.write(content)

        file_type = os.path.splitext(knowledge.file.name)[1]

        if file_type == '.md':
            loader = UnstructuredMarkdownLoader(f.name, mode='single')
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]

            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
            md_header_splits = markdown_splitter.split_text(loader.load()[0].page_content)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            return text_splitter.split_documents(md_header_splits)
        else:
            loader = UnstructuredFileLoader(f.name, mode='single')
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            return text_splitter.split_documents(loader.load())


@shared_task
def general_parse_embed(knowledge_base_folder_id):
    knowledge_base_folder = KnowledgeBaseFolder.objects.get(id=knowledge_base_folder_id)
    index_name = get_index_name(knowledge_base_folder_id)

    es = elasticsearch.Elasticsearch(hosts=[ELASTICSEARCH_URL],
                                     basic_auth=('elastic', ELASTICSEARCH_PASSWORD))

    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)

    try:
        knowledge_base_folder.train_status = 1
        knowledge_base_folder.train_progress = 0
        knowledge_base_folder.save()

        model_configs = knowledge_base_folder.embed_model.embed_config
        if knowledge_base_folder.embed_model.embed_model == EmbedModelChoices.FASTEMBED:
            from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
            embedding = FastEmbedEmbeddings(model_name=model_configs['model'], cache_dir='models')
            logger.info(f'初始化FastEmbed模型成功')

        if knowledge_base_folder.embed_model.embed_model == EmbedModelChoices.OPENAI:
            from langchain_openai import OpenAIEmbeddings
            embedding = OpenAIEmbeddings(model=model_configs['model'],
                                         openai_api_key=model_configs['openai_api_key'],
                                         openai_api_base=model_configs['openai_base_url'])
            logger.info(f'初始化OpenAI模型成功')

        file_knowledges = FileKnowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()
        knowledges = []

        for obj in file_knowledges:
            knowledges.append(obj)

        total_knowledges = len(knowledges)
        for index, knowledge in enumerate(knowledges):
            logger.info(f'训练知识:[{knowledge.title}]')

            if knowledge_base_folder.enable_general_parse:
                if isinstance(knowledge, FileKnowledge):
                    knowledge_docs = train_file_knowledgebase(knowledge, knowledge_base_folder.general_parse_chunk_size,
                                                              knowledge_base_folder.general_parse_chunk_overlap)

            db = ElasticsearchStore.from_documents(knowledge_docs, embedding, es_connection=es,
                                                   index_name=index_name)
            db.client.indices.refresh(index=index_name)

            progress = (index + 1) / total_knowledges * 100
            knowledge_base_folder.train_progress = progress
            knowledge_base_folder.save()

        knowledge_base_folder.train_status = 2
        knowledge_base_folder.train_progress = 100
        knowledge_base_folder.save()

    except Exception as e:
        logger.error(f'Training failed with error: {e}')
        knowledge_base_folder.train_status = 3
        knowledge_base_folder.train_progress = 100
        knowledge_base_folder.save()
