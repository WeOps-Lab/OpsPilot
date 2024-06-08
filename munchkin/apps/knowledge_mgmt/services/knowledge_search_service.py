from typing import Dict, List

from BCEmbedding.tools.langchain import BCERerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchRetriever

from apps.core.utils.embedding_driver import EmbeddingDriver
from apps.model_provider_mgmt.models import RerankModelChoices
from munchkin.components.elasticsearch import ELASTICSEARCH_URL, ELASTICSEARCH_PASSWORD


class KnowledgeSearchService:
    def vector_query(self, search_query: str, embeddings,
                     k, num_candidates,
                     text_search_weight=0.9,
                     vector_search_weight=0.1) -> Dict:
        vector = embeddings.embed_query(search_query)
        return {
            "query": {
                "match": {
                    'text': {
                        "query": search_query,
                        "boost": text_search_weight
                    }
                },
            },
            "knn": {
                "field": 'vector',
                "query_vector": vector,
                "k": k,
                "num_candidates": num_candidates,
                "filter": {
                    "term": {
                        "text": "knowledge_base",
                    },
                },
                "boost": vector_search_weight
            }
        }

    def search(self, knowledge_base_folders, query) -> List[Document]:
        docs = []

        for knowledge_base_folder in knowledge_base_folders:
            embedding = EmbeddingDriver().get_embedding(knowledge_base_folder.embed_model)

            vector_retriever = ElasticsearchRetriever.from_es_params(
                index_name=knowledge_base_folder.knowledge_index_name(),
                body_func=lambda x: self.vector_query(x, embedding,
                                                      knowledge_base_folder.rag_k,
                                                      knowledge_base_folder.rag_num_candidates,
                                                      knowledge_base_folder.text_search_weight,
                                                      knowledge_base_folder.vector_search_weight),
                content_field='text',
                url=ELASTICSEARCH_URL,
                username='elastic',
                password=ELASTICSEARCH_PASSWORD
            )
            if knowledge_base_folder.enable_rerank is False:
                result = vector_retriever.invoke(query)
            else:
                if knowledge_base_folder.rerank_model.rerank_model == RerankModelChoices.BCE:
                    reranker_args = {'model': knowledge_base_folder.rerank_model.rerank_config['model'],
                                     'top_n': knowledge_base_folder.rerank_top_k}
                    reranker = BCERerank(**reranker_args)
                compression_retriever = ContextualCompressionRetriever(
                    base_compressor=reranker, base_retriever=vector_retriever
                )
                result = compression_retriever.get_relevant_documents(query)
            for doc in result:
                docs.append(doc)

        return docs
