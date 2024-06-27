from typing import Dict, List

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langchain_elasticsearch import ElasticsearchRetriever
from langserve import RemoteRunnable

from embedding.remote_embeddings import RemoteEmbeddings
from user_types.elasticsearch_retriever_request import ElasticSearchRetrieverRequest


class ElasticSearchRagRunnable:
    def __init__(self):
        pass

    def vector_query(
            self,
            req: ElasticSearchRetrieverRequest
    ) -> Dict:
        embedding = RemoteEmbeddings(req.embed_model_address)
        vector = embedding.embed_query(req.search_query)

        es_query = {
            "query": {
                "bool": {
                    "must": {"term": {"text": req.search_query}},
                    "filter": [],
                    "boost": req.text_search_weight,
                }
            },
            "knn": {
                "field": "vector",
                "query_vector": vector,
                "k": req.rag_k,
                "filter": [],
                "num_candidates": req.rag_num_candidates,
                "boost": req.vector_search_weight,
            },
        }
        for key, value in req.metadata_filter.items():
            es_query["query"]["bool"]["filter"].append({"term": {f"metadata.{key}": value}})
        es_query["knn"]["filter"] = es_query["query"]["bool"]["filter"]

        return es_query

    def elasticsearch_rag_func(self, req: ElasticSearchRetrieverRequest) -> List[Document]:
        vector_retriever = ElasticsearchRetriever.from_es_params(
            index_name=req.index_name,
            body_func=lambda x: self.vector_query(x, req),
            content_field="text",
            url=req.elasticsearch_url,
            username="elastic",
            password=req.elasticsearch_password,
        )
        if req.enable_rerank is False:
            result = vector_retriever.invoke(req.search_query)
        else:
            search_result = vector_retriever.invoke(req.search_query)

            reranker = RemoteRunnable(req.rerank_model_address)
            params = {
                "docs": search_result,
                "query": req.search_query,
                "top_n": req.rerank_top_k
            }
            result = reranker.invoke(params)

        return result

    def instance(self):
        elasticsearch_rag_runnable = RunnableLambda(self.elasticsearch_rag_func).with_types(
            input_type=ElasticSearchRetrieverRequest,
            output_type=List[Document])
        return elasticsearch_rag_runnable
