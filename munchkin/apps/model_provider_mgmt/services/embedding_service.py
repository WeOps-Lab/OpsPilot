from langchain_community.embeddings import FastEmbedEmbeddings, HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

from apps.model_provider_mgmt.models import EmbedModelChoices, EmbedProvider


class EmbeddingService:
    def __init__(self):
        self.cache = {}

    def embed_content(self, embed_provider: EmbedProvider, content: str):
        embedding = self.get_embedding(embed_provider)
        return embedding.embed_query(content)

    def get_embedding(self, embed_provider: EmbedProvider):
        model_configs = embed_provider.decrypted_embed_config

        if embed_provider.id in self.cache:
            return self.cache[embed_provider.id]

        embedding = None

        if embed_provider.embed_model == EmbedModelChoices.FASTEMBED:
            embedding = FastEmbedEmbeddings(model_name=model_configs['model'], cache_dir='models')
        elif embed_provider.embed_model == EmbedModelChoices.BCEEMBEDDING:
            embedding = HuggingFaceEmbeddings(
                model_name=model_configs['model'],
                encode_kwargs={
                    'normalize_embeddings': True,
                    'batch_size': 32,
                },
            )
        elif embed_provider.embed_model == EmbedModelChoices.OPENAI:
            embedding = OpenAIEmbeddings(
                model=model_configs['model'],
                openai_api_key=model_configs['openai_api_key'],
                openai_api_base=model_configs['openai_base_url']
            )

        self.cache[embed_provider.id] = embedding
        return embedding


emdedding_service = EmbeddingService()
