from typing import List

from langchain.embeddings import CacheBackedEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_elasticsearch import ElasticsearchEmbeddingsCache
from langchain_openai import OpenAIEmbeddings
from langserve import RemoteRunnable

from apps.model_provider_mgmt.models import EmbedProvider, EmbedModelChoices
from munchkin.components.elasticsearch import ELASTICSEARCH_URL, ELASTICSEARCH_PASSWORD


class CustomRemoteRunnable(RemoteRunnable):
    def embed_query(self, text: str) -> List[float]:
        return self.invoke(text)


class EmbeddingService(Embeddings):
    def __init__(self, embed_provider: EmbedProvider):
        self.embed_provider = embed_provider

        model_configs = embed_provider.decrypted_embed_config
        if self.embed_provider.embed_model in [
            EmbedModelChoices.BCEEMBEDDING,
            EmbedModelChoices.FASTEMBED
        ]:
            embedding = CustomRemoteRunnable(model_configs['base_url'])

        if self.embed_provider.embed_model in [
            EmbedModelChoices.OPENAI
        ]:
            embedding = OpenAIEmbeddings(
                model=model_configs["model"],
                openai_api_key=model_configs["openai_api_key"],
                openai_api_base=model_configs["openai_base_url"],
            )
        store = ElasticsearchEmbeddingsCache(
            index_name=f'embed-cache-{embed_provider.id}',
            es_url=ELASTICSEARCH_URL,
            es_user="elastic",
            es_password=ELASTICSEARCH_PASSWORD,
        )
        self.embed_service = CacheBackedEmbeddings.from_bytes_store(
            underlying_embeddings=embedding,
            document_embedding_cache=store,
            query_embedding_cache=store,
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []
        for doc in texts:
            embeddings.append(self.embed_query(doc))
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embed_service.embed_query(text)

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        return await self.embed_documents(texts)

    async def aembed_query(self, text: str) -> List[float]:
        return await self.embed_query(text)
