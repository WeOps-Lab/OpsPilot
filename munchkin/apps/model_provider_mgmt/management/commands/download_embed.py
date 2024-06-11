import os

import nltk
from BCEmbedding import EmbeddingModel, RerankerModel
from django.core.management import BaseCommand
from langchain_community.embeddings import FastEmbedEmbeddings
from loguru import logger
from sentence_transformers import SentenceTransformer


class Command(BaseCommand):
    help = '下载模型'

    def handle(self, *args, **options):
        EmbeddingModel(model_name_or_path="maidalun1020/bce-embedding-base_v1", cache_dir='models')
        RerankerModel(model_name_or_path="maidalun1020/bce-reranker-base_v1", cache_dir='models')

        logger.info('下载nltk数据')
        nltk.download('all')

        fastembed_models = [
            'BAAI/bge-small-en-v1.5',
            'BAAI/bge-small-zh-v1.5'
        ]
        for model_name in fastembed_models:
            logger.info(f'下载模型:{model_name}')
            FastEmbedEmbeddings(model_name=model_name, cache_dir='models')
