import os.path
import tempfile

import elasticsearch
from celery import shared_task
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchStore
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from loguru import logger
from tqdm import tqdm

from apps.core.utils.embedding_driver import EmbeddingDriver
from apps.core.utils.llm_driver import LLMDriver
from apps.knowledge_mgmt.models import KnowledgeBaseFolder, FileKnowledge
from apps.knowledge_mgmt.utils import get_index_name
from munchkin.components.elasticsearch import ELASTICSEARCH_URL, ELASTICSEARCH_PASSWORD
from langchain.evaluation.qa import QAGenerateChain

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

        embedding = EmbeddingDriver().get_embedding(knowledge_base_folder.embed_model)

        file_knowledges = FileKnowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()
        knowledges = []

        for obj in file_knowledges:
            knowledges.append(obj)

        total_knowledges = len(knowledges)
        for index, knowledge in tqdm(enumerate(knowledges)):

            if knowledge_base_folder.enable_general_parse:
                if isinstance(knowledge, FileKnowledge):
                    knowledge_docs = train_file_knowledgebase(knowledge, knowledge_base_folder.general_parse_chunk_size,
                                                              knowledge_base_folder.general_parse_chunk_overlap)
            if knowledge_base_folder.enable_general_parse:
                llm_driver = LLMDriver(knowledge_base_folder.qa_generation_llm)
                gen_chain = QAGenerateChain.from_llm(llm_driver.get_qa_client())
                raw_data = [{"doc": t.page_content} for t in knowledge_docs]
                qa_examples = gen_chain.apply_and_parse(raw_data[:5])
                for obj in qa_examples:
                    doc = Document(page_content=f'问题:[{obj["qa_pairs"]["query"]}] 答案:[{obj["qa_pairs"]["answer"]}]')
                    knowledges.append(doc)
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
