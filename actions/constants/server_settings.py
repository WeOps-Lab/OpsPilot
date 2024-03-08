from typing import Optional

from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    run_mode: str = "dev"
    llm_fallback_mode: Optional[str] = None

    dify_key: Optional[str] = None
    dify_endpoint: Optional[str] = None

    fastgpt_key: Optional[str] = None
    fastgpt_endpoint: Optional[str] = None

    openai_key: Optional[str] = None
    openai_endpoint: Optional[str] = None
    openai_api_temperature: Optional[float] = 0.7

    redis_host: Optional[str] = ""
    redis_port: Optional[int] = 6379
    redis_db: Optional[int] = 0
    redis_password: Optional[str] = ""

    jenkins_username: Optional[str] = None
    jenkins_password: Optional[str] = None
    jenkins_url: Optional[str] = None

    class Config:
        env_file = ".env"


server_settings = ServerSettings()
