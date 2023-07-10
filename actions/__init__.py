import os

from dotenv import load_dotenv

from actions.constant.server_settings import server_settings

load_dotenv()
os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', server_settings.embed_model_cache_home)