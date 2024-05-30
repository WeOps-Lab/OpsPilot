import nltk
from django.core.management import BaseCommand
from langchain_community.embeddings import FastEmbedEmbeddings
from loguru import logger


class Command(BaseCommand):
    help = '下载模型'

    def handle(self, *args, **options):
        nltk.download('all')

        fastembed_models = [
            'BAAI/bge-small-en-v1.5',
            'BAAI/bge-small-zh-v1.5'
        ]
        for model_name in fastembed_models:
            logger.info(f'下载模型:{model_name}')
            FastEmbedEmbeddings(model_name=model_name, cache_dir='models')
