from langchain_openai import OpenAIEmbeddings
from langserve import RemoteRunnable

from apps.model_provider_mgmt.models import EmbedProvider, EmbedModelChoices


class EmbeddingService:
    def __init__(self, embed_provider: EmbedProvider):
        self.embed_provider = embed_provider

        model_configs = embed_provider.decrypted_embed_config
        if self.embed_provider.embed_model in [
            EmbedModelChoices.BCEEMBEDDING,
            EmbedModelChoices.FASTEMBED
        ]:
            self.embed_service = RemoteRunnable(model_configs['base_url'])

        if self.embed_provider.embed_model in [
            EmbedModelChoices.OPENAI
        ]:
            self.embed_service = OpenAIEmbeddings(
                model=model_configs["model"],
                openai_api_key=model_configs["openai_api_key"],
                openai_api_base=model_configs["openai_base_url"],
            )

    def embed_content(self, docs: str):
        if embed_provider.embed_model in [
            EmbedModelChoices.BCEEMBEDDING,
            EmbedModelChoices.FASTEMBED
        ]:
            return self.embed_service.invoke({"content": content})
        else:
            return self.embed_service.embed_query(content)


embedding_service = EmbeddingService()
