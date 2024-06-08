import os

from BCEmbedding import EmbeddingModel

from apps.model_provider_mgmt.models import EmbedModelChoices
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import FastEmbedEmbeddings, HuggingFaceEmbeddings


class EmbeddingDriver:
    def __init__(self):
        self.cache = {}

    def get_embedding(self, embed_model):
        if embed_model.embed_model in self.cache:
            return self.cache[embed_model.embed_model]

        model_configs = embed_model.decrypted_embed_config
        embedding = None

        if embed_model.embed_model == EmbedModelChoices.FASTEMBED:
            embedding = FastEmbedEmbeddings(model_name=model_configs['model'], cache_dir='models')
        elif embed_model.embed_model == EmbedModelChoices.BCEEMBEDDING:
            embedding = HuggingFaceEmbeddings(
                model_name=model_configs['model'],
                encode_kwargs={
                    'normalize_embeddings': True,
                    'batch_size': 32,
                },
            )
        elif embed_model.embed_model == EmbedModelChoices.OPENAI:
            embedding = OpenAIEmbeddings(model=model_configs['model'],
                                         openai_api_key=model_configs['openai_api_key'],
                                         openai_api_base=model_configs['openai_base_url'])

        if embedding is not None:
            self.cache[embed_model.embed_model] = embedding

        return embedding
