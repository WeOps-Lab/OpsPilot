from typing import List

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langserve import RemoteRunnable
from tqdm import tqdm

from apps.model_provider_mgmt.models import EmbedProvider, EmbedModelChoices
import logging

logging.getLogger('httpx').setLevel(logging.CRITICAL)


class RemoteRunnableEmbed(RemoteRunnable):
    def embed_query(self, text: str) -> List[float]:
        return self.invoke(text)


class RemoteEmbeddings(Embeddings):
    def __init__(self, embed_provider: EmbedProvider):
        self.embed_provider = embed_provider

        model_configs = embed_provider.embed_config
        self.embedding = RemoteRunnableEmbed(model_configs['base_url'])

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []
        for doc in tqdm(texts):
            embeddings.append(self.embed_query(doc))
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embedding.embed_query(text)
