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

    class Config:
        env_file = ".env"


server_settings = ServerSettings()
