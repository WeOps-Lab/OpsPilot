from typing import Dict, List

from BCEmbedding.tools.langchain import BCERerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchRetriever

from apps.model_provider_mgmt.services.embedding_service import EmbeddingService
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from apps.model_provider_mgmt.models import RerankModelChoices
from apps.model_provider_mgmt.services.rerank_service import RerankService
from munchkin.components.elasticsearch import ELASTICSEARCH_URL, ELASTICSEARCH_PASSWORD


class KnowledgeSearchService:
    def vector_query(self, search_query: str, embeddings,
                     knowledge_base_folder: KnowledgeBaseFolder,
                     metadata={}) -> Dict:
        vector = embeddings.embed_query(search_query)
        es_query = {
            "query": {
                "bool": {
                    "must": {
                        "term": {"text": search_query}
                    },
                    "filter": [],
                    "boost": knowledge_base_folder.text_search_weight
                }
            },
            "knn": {
                "field": 'vector',
                "query_vector": vector,
                "k": knowledge_base_folder.rag_k,
                "filter": [],
                "num_candidates": knowledge_base_folder.rag_num_candidates,
                "boost": knowledge_base_folder.vector_search_weight
            }
        }
        for key, value in metadata.items():
            es_query['query']['bool']['filter'].append({
                "term": {
                    f"metadata.{key}": value
                }
            })
        es_query['knn']['filter'] = es_query['query']['bool']['filter']
        return es_query

    def search(self, knowledge_base_folders, query, metadata={}) -> List[Document]:
        docs = []

        for knowledge_base_folder in knowledge_base_folders:
            embedding = EmbeddingService().get_embedding(knowledge_base_folder.embed_model)

            vector_retriever = ElasticsearchRetriever.from_es_params(
                index_name=knowledge_base_folder.knowledge_index_name(),
                body_func=lambda x: self.vector_query(x, embedding, knowledge_base_folder, metadata),
                content_field='text',
                url=ELASTICSEARCH_URL,
                username='elastic',
                password=ELASTICSEARCH_PASSWORD
            )
            if knowledge_base_folder.enable_rerank is False:
                result = vector_retriever.invoke(query)
            else:
                reranker_service = RerankService()
                reranker = reranker_service.get_reranker(knowledge_base_folder.rerank_model,
                                                         knowledge_base_folder.rerank_top_k)

                compression_retriever = ContextualCompressionRetriever(
                    base_compressor=reranker, base_retriever=vector_retriever
                )
                result = compression_retriever.get_relevant_documents(query)
            for doc in result:
                docs.append(doc)

        return docs
