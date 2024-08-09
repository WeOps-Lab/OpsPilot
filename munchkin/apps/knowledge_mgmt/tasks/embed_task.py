from apps.knowledge_mgmt.models import FileKnowledge, KnowledgeBaseFolder, ManualKnowledge, WebPageKnowledge
from dotenv import load_dotenv
from langserve import RemoteRunnable
from loguru import logger
from tqdm import tqdm

from celery import shared_task
from munchkin.components.elasticsearch import ELASTICSEARCH_PASSWORD, ELASTICSEARCH_URL
from munchkin.components.remote_service import (
    FILE_CHUNK_SERIVCE_URL,
    MANUAL_CHUNK_SERVICE_URL,
    REMOTE_INDEX_URL,
    WEB_PAGE_CHUNK_SERVICE_URL,
)

load_dotenv()


@shared_task
def general_embed(knowledge_base_folder_id):
    file_remote = RemoteRunnable(FILE_CHUNK_SERIVCE_URL)
    manual_remote = RemoteRunnable(MANUAL_CHUNK_SERVICE_URL)
    web_page_remote = RemoteRunnable(WEB_PAGE_CHUNK_SERVICE_URL)
    remote_indexer = RemoteRunnable(REMOTE_INDEX_URL)

    knowledge_base_folder = KnowledgeBaseFolder.objects.get(id=knowledge_base_folder_id)
    index_name = knowledge_base_folder.knowledge_index_name()

    try:
        knowledge_base_folder.train_status = 1
        knowledge_base_folder.train_progress = 0
        knowledge_base_folder.save()

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
        knowledge_docs = []
        for index, knowledge in tqdm(enumerate(knowledges)):
            semantic_embedding_address = ""

            semantic_chunk_parse_embedding_model = knowledge.semantic_chunk_parse_embedding_model
            if semantic_chunk_parse_embedding_model is not None:
                semantic_embedding_address = semantic_chunk_parse_embedding_model.embed_config["base_url"]

            ocr_provider_address = ""
            if knowledge_base_folder.ocr_model is not None:
                ocr_provider_address = knowledge_base_folder.ocr_model.ocr_config["base_url"]

            if isinstance(knowledge, FileKnowledge):
                logger.debug(f"开始处理文件知识: {knowledge.title}")

                remote_docs = file_remote.invoke(
                    {
                        "enable_recursive_chunk_parse": knowledge.enable_general_parse,
                        "recursive_chunk_size": knowledge.general_parse_chunk_size,
                        "recursive_chunk_overlap": knowledge.general_parse_chunk_overlap,
                        "enable_semantic_chunck_parse": knowledge.enable_semantic_chunck_parse,
                        "enable_ocr_parse": knowledge.enable_ocr_parse,
                        "semantic_embedding_address": semantic_embedding_address,
                        "excel_header_row_parse": knowledge.excel_header_row_parse,
                        "excel_full_content_parse": knowledge.excel_full_content_parse,
                        "ocr_provider_address": ocr_provider_address,
                        "file_name": knowledge.file.name,
                        "file": knowledge.get_file_base64(),
                        "custom_metadata": {
                            "knowledge_type": "file",
                            "knowledge_id": knowledge.id,
                            "knowledge_title": knowledge.title,
                            "knowledge_folder_id": knowledge.knowledge_base_folder.id,
                            **knowledge.custom_metadata,
                        },
                    }
                )
                knowledge_docs.extend(remote_docs)
                logger.info(f"文件知识[{knowledge.title}]共提取[{len(remote_docs)}]个文档片段")

            elif isinstance(knowledge, ManualKnowledge):
                logger.debug(f"开始处理手动知识: {knowledge.title}")

                remote_docs = manual_remote.invoke(
                    {
                        "enable_recursive_chunk_parse": knowledge.enable_general_parse,
                        "recursive_chunk_size": knowledge.general_parse_chunk_size,
                        "recursive_chunk_overlap": knowledge.general_parse_chunk_overlap,
                        "enable_semantic_chunck_parse": knowledge.enable_semantic_chunck_parse,
                        "semantic_embedding_address": semantic_embedding_address,
                        "content": knowledge.title + knowledge.content + str(knowledge.custom_metadata),
                        "custom_metadata": {
                            "knowledge_type": "manual",
                            "knowledge_id": knowledge.id,
                            "knowledge_title": knowledge.title,
                            "knowledge_folder_id": knowledge.knowledge_base_folder.id,
                            **knowledge.custom_metadata,
                        },
                    }
                )
                knowledge_docs.extend(remote_docs)
                logger.info(f"手动知识[{knowledge.title}]共提取[{len(remote_docs)}]个文档片段")

            elif isinstance(knowledge, WebPageKnowledge):
                logger.debug(f"开始处理网页知识: {knowledge.title}")
                remote_docs = web_page_remote.invoke(
                    {
                        "enable_recursive_chunk_parse": knowledge.enable_general_parse,
                        "recursive_chunk_size": knowledge.general_parse_chunk_size,
                        "recursive_chunk_overlap": knowledge.general_parse_chunk_overlap,
                        "enable_semantic_chunck_parse": knowledge.enable_semantic_chunck_parse,
                        "semantic_embedding_address": semantic_embedding_address,
                        "url": knowledge.url,
                        "max_depth": 1,
                        "custom_metadata": {
                            "knowledge_type": "webpage",
                            "knowledge_id": knowledge.id,
                            "knowledge_title": knowledge.title,
                            "knowledge_folder_id": knowledge.knowledge_base_folder.id,
                            **knowledge.custom_metadata,
                        },
                    }
                )
                knowledge_docs.extend(remote_docs)
                logger.info(f"网页知识[{knowledge.title}]共提取[{len(remote_docs)}]个文档片段")

            progress = round((index + 1) / total_knowledges * 100, 2)
            logger.debug(f"知识库[{knowledge_base_folder_id}]的Embedding索引生成进度: {progress:.2f}%")
            knowledge_base_folder.train_progress = progress
            knowledge_base_folder.save()

        logger.debug(f"开始写入知识库[{knowledge_base_folder_id}]")
        remote_indexer.invoke(
            {
                "elasticsearch_url": ELASTICSEARCH_URL,
                "elasticsearch_password": ELASTICSEARCH_PASSWORD,
                "embed_model_address": knowledge_base_folder.embed_model.embed_config["base_url"],
                "index_name": index_name,
                "index_mode": "overwrite",
                "docs": knowledge_docs,
            }
        )

        knowledge_base_folder.train_status = 2
        knowledge_base_folder.train_progress = 100
        knowledge_base_folder.save()

    except Exception as e:
        logger.exception(e)

        knowledge_base_folder.train_status = 3
        knowledge_base_folder.train_progress = 100
        knowledge_base_folder.save()
