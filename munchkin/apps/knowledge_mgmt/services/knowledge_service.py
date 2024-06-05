import copy
import json
from typing import Dict

from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_elasticsearch import ElasticsearchRetriever
from langchain.memory import ChatMessageHistory
from apps.contentpack_mgmt.models import BotActions, BotActionRule
from loguru import logger

from apps.core.utils.llm_driver import LLMDriver
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from apps.model_provider_mgmt.models import EmbedModelChoices, LLMModelChoices
from munchkin.components.elasticsearch import ELASTICSEARCH_URL, ELASTICSEARCH_PASSWORD


class KnowledgeService:
    def knowledge_search(self, knowledge_base_name, search_keyword):
        knowledge_base_folder = KnowledgeBaseFolder.objects.get(name=knowledge_base_name)
        if knowledge_base_folder.embed_model.embed_model == EmbedModelChoices.FASTEMBED:
            model_configs = knowledge_base_folder.embed_model.embed_config
            embedding = FastEmbedEmbeddings(model_name=model_configs['model'], cache_dir='models')

        index_name = f"knowledge_base_{knowledge_base_folder.id}"

        vector_retriever = ElasticsearchRetriever.from_es_params(
            index_name=index_name,
            body_func=lambda x: self.vector_query(x, embedding,
                                                  knowledge_base_folder.rag_k,
                                                  knowledge_base_folder.rag_num_candidates,
                                                  knowledge_base_folder.text_search_weight,
                                                  knowledge_base_folder.vector_search_weight,
                                                  ),
            content_field='text',
            url=ELASTICSEARCH_URL,
            username='elastic',
            password=ELASTICSEARCH_PASSWORD
        )

        result = vector_retriever.invoke(search_keyword)
        return [res.to_json() for res in result]

    def vector_query(self, search_query: str, embeddings,
                     k, num_candidates,
                     text_search_weight=0.9,
                     vector_search_weight=0.1,
                     ) -> Dict:
        vector = embeddings.embed_query(search_query)
        search_query = {
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
            },
            "_source": ["text", "metadata"]
        }
        return search_query
