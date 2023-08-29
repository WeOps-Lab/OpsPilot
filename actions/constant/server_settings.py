from typing import Optional

from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    fallback_mode: str = "LOCAL_LLM"

    fastgpt_endpoint: Optional[str] = None
    fastgpt_key: Optional[str] = None

    openai_endpoint: Optional[str] = None
    openai_key: Optional[str] = None
    openai_api_temperature: Optional[float] = 0.7

    redis_host: str = ""
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""

    run_mode: str = "Dev"
    fallback_chat_mode: str = "chat"

    embed_model_name: Optional[str] = "shibing624/text2vec-base-chinese"
    embed_model_cache_home: Optional[str] = "cache/models"
    vec_db_path: Optional[str] = "vec_db"
    indexer_db_path: Optional[str] = "indexdir"

    default_thinking_message = "OpsPilot正在思考中........"

    chatgpt_model_max_history: Optional[int] = 10

    neo4j_url: Optional[str] = ""
    neo4j_username: Optional[str] = ""
    neo4j_password: Optional[str] = ""

    bkapp_app_code: Optional[str] = ""
    bkapp_app_token: Optional[str] = ""
    bkapp_bk_paas_host: Optional[str] = ""
    bkapp_api_ver: Optional[str] = ""

    class Config:
        env_file = ".env"


server_settings = ServerSettings()
