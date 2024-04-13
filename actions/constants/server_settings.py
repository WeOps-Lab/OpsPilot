from typing import Optional

from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    run_mode: str = "dev"

    fallback_llm: str = 'FAST_GPT'

    fastgpt_endpoint: Optional[str] = None
    fastgpt_key: Optional[str] = None

    dify_key: Optional[str] = None
    dify_endpoint: Optional[str] = None

    chatgpt_model_max_history: int = 5

    enable_jenkins_skill: bool = False
    jenkins_url: Optional[str] = None
    jenkins_username: Optional[str] = None
    jenkins_password: Optional[str] = None

    class Config:
        env_file = ".env"


server_settings = ServerSettings()
