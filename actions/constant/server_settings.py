import os
from typing import Optional

import redis
from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    fallback_llm: str = 'OPENAI'

    openai_endpoint: Optional[str] = None
    openai_key: Optional[str] = None
    openai_api_temperature: Optional[float] = 0.7

    enable_jenkins_skill: bool = False
    jenkins_url: Optional[str] = None
    jenkins_username: Optional[str] = None
    jenkins_password: Optional[str] = None

    bing_search_url: Optional[str] = None
    bing_search_key: Optional[str] = None

    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    run_mode: str = 'Dev'
    fallback_chat_mode: str = 'knowledgebase'
    enable_online_chat: bool = False

    embed_model_name: Optional[str] = 'shibing624/text2vec-base-chinese'
    embed_model_cache_home: Optional[str] = 'cache/models'
    vec_db_path: Optional[str] = 'vec_db'
    indexer_db_path: Optional[str] = 'indexdir'

    default_thinking_message = 'OpsPilot正在思考中........'

    chatgpt_model_max_history: Optional[int] = 10

    neo4j_url: Optional[str] = ''
    neo4j_username: Optional[str] = ''
    neo4j_password: Optional[str] = ''

    class Config:
        env_file = '.env'


server_settings = ServerSettings()
