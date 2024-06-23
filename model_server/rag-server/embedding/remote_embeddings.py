from typing import List

from langchain_core.embeddings import Embeddings
from langserve import RemoteRunnable
from tqdm import tqdm

import logging

logging.getLogger('httpx').setLevel(logging.CRITICAL)


class RemoteRunnableEmbed(RemoteRunnable):
    def embed_query(self, text: str) -> List[float]:
        return self.invoke(text)


class RemoteEmbeddings(Embeddings):
    def __init__(self, base_url):
        self.embedding = RemoteRunnableEmbed(base_url)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []
        for doc in tqdm(texts):
            embeddings.append(self.embed_query(doc))
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embedding.embed_query(text)
