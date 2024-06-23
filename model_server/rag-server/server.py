from typing import List, Dict

import elasticsearch
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langchain_elasticsearch import ElasticsearchStore, ElasticsearchRetriever
from langserve import CustomUserType, add_routes, RemoteRunnable
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from embedding.remote_embeddings import RemoteEmbeddings

load_dotenv()

app = FastAPI(
    title="rag_server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


class ElasticSearchRequest(CustomUserType):
    elasticsearch_url: str = "http://elasticsearch.ops-pilot:9200"
    elasticsearch_password: str
    embed_model_address: str


class ElasticSearchStoreRequest(ElasticSearchRequest):
    index_name: str
    index_mode: str
    docs: List[Document]


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


def vector_query(
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


def elasticsearch_rag_func(req: ElasticSearchRetrieverRequest) -> List[Document]:
    vector_retriever = ElasticsearchRetriever.from_es_params(
        index_name=req.index_name,
        body_func=lambda x: vector_query(x, req),
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


def elasticsearch_index_func(req: ElasticSearchStoreRequest) -> bool:
    es = elasticsearch.Elasticsearch(hosts=[req.elasticsearch_url],
                                     basic_auth=("elastic", req.elasticsearch_password))
    embedding_service = RemoteEmbeddings(req.embed_model_address)
    if req.index_mode == 'overwrite' and es.indices.exists(index=req.index_name):
        logger.info(f"删除已存在的索引: {req.index_name}")
        es.indices.delete(index=req.index_name)

    db = ElasticsearchStore.from_documents(
        req.docs, embedding=embedding_service, es_connection=es, index_name=req.index_name
    )
    db.client.indices.refresh(index=req.index_name)
    return True


elasticsearch_index_runnable = RunnableLambda(elasticsearch_index_func).with_types(input_type=ElasticSearchStoreRequest,
                                                                                   output_type=bool)
elasticsearch_rag_runnable = RunnableLambda(elasticsearch_rag_func).with_types(input_type=ElasticSearchRetrieverRequest,
                                                                               output_type=List[Document])
add_routes(app, elasticsearch_index_runnable, path='/elasticsearch_index')
add_routes(app, elasticsearch_rag_runnable, path='/elasticsearch_rag')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8106)
