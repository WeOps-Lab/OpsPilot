from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    azure_openai_model_name: str
    azure_openai_endpoint: str
    azure_openai_key: str

    jenkins_url: str
    jenkins_username: str
    jenkins_password: str

    run_mode: str

    class Config:
        env_file = '.env'


server_settings = ServerSettings()
