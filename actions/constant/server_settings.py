import os
from typing import Optional

from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    fallback_llm: str
    fallback_prompt: str

    azure_openai_model_name: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_key: Optional[str] = None

    jenkins_url: Optional[str] = None
    jenkins_username: Optional[str] = None
    jenkins_password: Optional[str] = None

    bing_search_url: Optional[str] = None
    bing_search_key: Optional[str] = None

    run_mode: str

    class Config:
        env_file = '.env'


server_settings = ServerSettings()
