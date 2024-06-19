from typing import Dict, List

from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from apps.model_provider_mgmt.services.embedding_service import embedding_service
from apps.model_provider_mgmt.services.rerank_service import rerank_service
from langchain.retrievers import ContextualCompressionRetriever
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchRetriever

from munchkin.components.elasticsearch import ELASTICSEARCH_PASSWORD, ELASTICSEARCH_URL


class KnowledgeSearchService:
    def vector_query(
            self,
            search_query: str,
            embeddings,
            knowledge_base_folder: KnowledgeBaseFolder,
            metadata={},
    ) -> Dict:
        vector = embeddings.embed_query(search_query)
        es_query = {
            "query": {
                "bool": {
                    "must": {"term": {"text": search_query}},
                    "filter": [],
                    "boost": knowledge_base_folder.text_search_weight,
                }
            },
            "knn": {
                "field": "vector",
                "query_vector": vector,
                "k": knowledge_base_folder.rag_k,
                "filter": [],
                "num_candidates": knowledge_base_folder.rag_num_candidates,
                "boost": knowledge_base_folder.vector_search_weight,
            },
        }
        for key, value in metadata.items():
            es_query["query"]["bool"]["filter"].append({"term": {f"metadata.{key}": value}})
        es_query["knn"]["filter"] = es_query["query"]["bool"]["filter"]
        return es_query

    def search(self, knowledge_base_folders, query, metadata={}, score_threshold=0) -> List[Document]:
        docs = []

        for knowledge_base_folder in knowledge_base_folders:
            embedding = embedding_service.get_embedding(knowledge_base_folder.embed_model)

            vector_retriever = ElasticsearchRetriever.from_es_params(
                index_name=knowledge_base_folder.knowledge_index_name(),
                body_func=lambda x: self.vector_query(x, embedding, knowledge_base_folder, metadata),
                content_field="text",
                url=ELASTICSEARCH_URL,
                username="elastic",
                password=ELASTICSEARCH_PASSWORD,
            )
            if knowledge_base_folder.enable_rerank is False:
                result = vector_retriever.invoke(query)
            else:
                reranker = rerank_service.get_reranker(
                    knowledge_base_folder.rerank_model,
                    knowledge_base_folder.rerank_top_k,
                )

                compression_retriever = ContextualCompressionRetriever(
                    base_compressor=reranker, base_retriever=vector_retriever
                )
                result = compression_retriever.get_relevant_documents(query)
            for doc in result:
                score = doc.metadata['_score'] * 10
                if score > score_threshold:
                    doc_info = {
                        "content": doc.page_content,
                        "score": doc.metadata['_score'] * 10,
                        "knowledge_title": doc.metadata['_source']['metadata']['knowledge_title'],
                        "knowledge_id": doc.metadata['_source']['metadata']['knowledge_id'],
                        "knowledge_folder_id": doc.metadata['_source']['metadata']['knowledge_folder_id'],
                    }
                    if knowledge_base_folder.enable_rerank:
                        doc_info["rerank_score"] = doc.metadata["relevance_score"]
                    docs.append(doc_info)

        return docs
