from typing import Optional
import yaml
from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    chatgpt_model_max_history: int = 10

    rabbitmq_host: Optional[str] = None
    rabbitmq_port: Optional[str] = None
    rabbitmq_username: Optional[str] = None
    rabbitmq_password: Optional[str] = None

    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None

    munchkin_bot_id: Optional[str] = None
    munchkin_api_key: Optional[str] = None
    munchkin_base_url: Optional[str] = None

    class Config:
        env_file = ".env"


server_settings = ServerSettings()
