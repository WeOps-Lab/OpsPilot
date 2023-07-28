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

    redis_host: str = ''
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ''

    run_mode: str = 'Dev'
    fallback_chat_mode: str = 'knowledgebase'
    enable_online_chat: bool = False

    embed_model_name: Optional[str] = 'shibing624/text2vec-base-chinese'
    embed_model_cache_home: Optional[str] = 'cache/models'
    vec_db_path: Optional[str] = 'vec_db'
    indexer_db_path: Optional[str] = 'indexdir'

    default_thinking_message = 'OpsPilot正在思考中........'

    chatgpt_model_max_history: Optional[int] = 10

    neo4j_url: Optional[str] = 'bolt://10.11.25.48:7687'
    neo4j_username: Optional[str] = 'neo4j'
    neo4j_password: Optional[str] = 'megalab_umr'

    bkapp_app_code: Optional[str] = "weops_saas"
    bkapp_app_token: Optional[str] = "6a38236d-8e79-4c48-a977-504b0d286904"
    bkapp_bk_paas_host: Optional[str] = "http://paas.weops.com"
    bkapp_api_ver: Optional[str] = "v2"



    class Config:
        env_file = '.env'


server_settings = ServerSettings()
