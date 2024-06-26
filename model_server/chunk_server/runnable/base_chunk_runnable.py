from typing import List

from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter

from embedding.remote_embeddings import RemoteEmbeddings
from user_types.base_chunk_request import BaseChunkRequest
from loguru import logger


class BaseChunkRunnable:

    def parse_docs(self, docs: List[Document], request: BaseChunkRequest) -> List[Document]:
        table_docs = []

        # 所有表格型的内容都不参与内容分割
        for doc in docs:
            if doc.metadata.get("format", "") == "table":
                table_docs.append(doc)

        for doc in table_docs:
            docs.remove(doc)

        if request.enable_semantic_chunck_parse:
            semantic_embedding_model = RemoteEmbeddings(request.semantic_embedding_address)
            semantic_chunker = SemanticChunker(embeddings=semantic_embedding_model,
                                               sentence_split_regex=r'(?<=[.?!。？！])\s*')
            docs = semantic_chunker.split_documents(docs)
            logger.info(f'语义分割后的文档数：{len(docs)}')

        if request.enable_recursive_chunk_parse:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=request.recursive_chunk_size,
                chunk_overlap=request.recursive_chunk_overlap,
            )
            docs = text_splitter.split_documents(docs)
            logger.info(f'递归分割后的文档数：{len(docs)}')

        for doc in docs:
            doc.metadata.update(request.custom_metadata)
            doc.page_content = doc.page_content.replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()
            if 'source' in doc.metadata:
                del doc.metadata["source"]
        docs = docs + table_docs

        logger.info(f'最终文档数：{len(docs)}')

        return docs
