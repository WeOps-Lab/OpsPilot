import os

from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', './cache/models')