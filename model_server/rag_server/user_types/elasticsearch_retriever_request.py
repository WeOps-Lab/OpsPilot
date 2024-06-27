from user_types.elasticsearch_request import ElasticSearchRequest


class ElasticSearchRetrieverRequest(ElasticSearchRequest):
    index_name: str
    search_query: str
    text_search_weight: float = 0.9
    rag_k: int = 10
    rag_num_candidates: int = 1000
    vector_search_weight: float = 0.1
    metadata_filter: dict = {}
    enable_rerank: bool = False
    rerank_model_address: str = ''
    rerank_top_k: int = 5
