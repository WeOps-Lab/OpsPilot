from typing import Optional

from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    run_mode: str = "dev"

    redis_host: Optional[str] = None
    redis_port: Optional[int] = None
    redis_db: Optional[int] = None
    redis_password: Optional[str] = None

    fastgpt_endpoint: Optional[str] = None
    fastgpt_key: Optional[str] = None
    fastgpt_content_summary_key: Optional[str] = None
    fastgpt_ticket_key: Optional[str] = None

    chatgpt_model_max_history: int = 5

    enable_jenkins_skill: bool = False
    jenkins_url: Optional[str] = None
    jenkins_username: Optional[str] = None
    jenkins_password: Optional[str] = None

    celery_broker_url: Optional[str] = None
    celery_result_backend: Optional[str] = None

    rasa_credentials: Optional[str] = 'credentials.yml'
    rasa_action_server_url: Optional[str] = 'http://localhost:5005'

    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    supabase_username: Optional[str] = None
    supabase_password: Optional[str] = None

    ocr_service: Optional[str] = None
    azure_ocr_endpoint: Optional[str] = None
    azure_ocr_key: Optional[str] = None

    class Config:
        env_file = ".env"


server_settings = ServerSettings()
