import os
from typing import Optional

from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    fallback_llm: str = 'OPENAI'
    fallback_prompt: str = '扮演专业的运维工程师'

    openai_model_name: Optional[str] = None
    openai_endpoint: Optional[str] = None
    openai_key: Optional[str] = None
    openai_api_temperature: Optional[float] = 0.7

    jenkins_url: Optional[str] = None
    jenkins_username: Optional[str] = None
    jenkins_password: Optional[str] = None

    bing_search_url: Optional[str] = None
    bing_search_key: Optional[str] = None

    vec_db_path: Optional[str] = None

    run_mode: str = 'Dev'
    fallback_chat_mode: str = 'knowledgebase'

    class Config:
        env_file = '.env'


server_settings = ServerSettings()
