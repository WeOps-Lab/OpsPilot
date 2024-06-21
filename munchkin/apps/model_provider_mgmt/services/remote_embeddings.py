from typing import List

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langserve import RemoteRunnable

from apps.model_provider_mgmt.models import EmbedProvider, EmbedModelChoices


class RemoteRunnableEmbed(RemoteRunnable):
    def embed_query(self, text: str) -> List[float]:
        return self.invoke(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.batch(texts)


class RemoteEmbeddings(Embeddings):
    def __init__(self, embed_provider: EmbedProvider):
        self.embed_provider = embed_provider

        model_configs = embed_provider.decrypted_embed_config
        if self.embed_provider.embed_model_type == EmbedModelChoices.LANG_SERVE:
            self.embedding = RemoteRunnableEmbed(model_configs['base_url'])

        if self.embed_provider.embed_model_type in [
            EmbedModelChoices.OPENAI
        ]:
            self.embedding = OpenAIEmbeddings(
                model=model_configs["model"],
                openai_api_key=model_configs["openai_api_key"],
                openai_api_base=model_configs["openai_base_url"],
            )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.embedding.embed_query(text)
