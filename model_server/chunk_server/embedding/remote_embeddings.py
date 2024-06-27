import logging
from typing import List

from langchain_core.embeddings import Embeddings
from langserve import RemoteRunnable

logging.getLogger('httpx').setLevel(logging.CRITICAL)


class RemoteRunnableEmbed(RemoteRunnable):
    def embed_query(self, text: str) -> List[float]:
        return self.invoke(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.batch(texts)


class RemoteEmbeddings(Embeddings):
    def __init__(self, base_url):
        self.embedding = RemoteRunnableEmbed(base_url)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embedding.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.embedding.embed_query(text)
