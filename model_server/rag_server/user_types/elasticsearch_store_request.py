from typing import List

from langchain_core.documents import Document

from user_types.elasticsearch_request import ElasticSearchRequest


class ElasticSearchStoreRequest(ElasticSearchRequest):
    index_name: str
    index_mode: str
    chunk_size: int = 50
    max_chunk_bytes: int = 200000000
    docs: List[Document]
