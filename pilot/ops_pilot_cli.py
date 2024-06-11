import os
import subprocess

import fire
import yaml
from dotenv import load_dotenv
from loguru import logger
import requests
import shutil
from core.server_settings import server_settings
import zipfile

load_dotenv()


class BootStrap(object):
    def download_train_data(self):
        logger.info("Downloading train data")
        response = requests.get(
            server_settings.munchkin_base_url + f'/api/contentpack/train_data_download?model_id={os.getenv("RASA_MODEL_ID")}',
            headers={
                'Authorization': f'TOKEN {server_settings.munchkin_api_key}',
                'Content-Type': 'application/json'
            },
            stream=True)
        response.raise_for_status()
        with open('data.zip', 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

    def unzip_train_data(self):
        # remove existing data folder first
        try:
            shutil.rmtree('data')
        except FileNotFoundError:
            pass

        logger.info("Unzipping train data")

        with zipfile.ZipFile('data.zip', 'r') as zip_ref:
            zip_ref.extractall('data')

    def upload_train_model(self):
        with open('models/ops-pilot.tar.gz', 'rb') as f:
            files = {'file': f}
            response = requests.post(
                server_settings.munchkin_base_url + f'/api/contentpack/model_upload?model_id={os.getenv("RASA_MODEL_ID")}',
                headers={
                    'Authorization': f'TOKEN {server_settings.munchkin_api_key}',
                },
                files=files)
            response.raise_for_status()

    def get_bot_config_data(self):
        credentials = {
            'socketio': {
                'user_message_evt': 'user_uttered',
                'bot_message_evt': 'bot_uttered',
                'session_persistence': False,
            },
        }
        response = requests.get(
            server_settings.munchkin_base_url + f'/api/bot/{server_settings.munchkin_bot_id}',
            headers={
                'Authorization': f'TOKEN {server_settings.munchkin_api_key}',
                'Content-Type': 'application/json'
            },
            stream=True)
        response.raise_for_status()

        result = response.json()
        for channel in result['channels']:
            credentials.update(channel['channel_config'])

        with open('data/credentials.yml', 'w', encoding='utf-8') as f:
            yaml.dump(credentials, f, allow_unicode=True)

        endpoints = {
            'action_endpoint': {
                'url': 'http://localhost:5055/webhook',
            },
            'models': {
                'url': f'{server_settings.munchkin_base_url}/api/contentpack/model_download?bot_id={server_settings.munchkin_bot_id}',
                'wait_time_between_pulls': None,
            },
            'tracker_store': {
                'type': 'SQL',
                'dialect': 'sqlite',
                'url': '',
                'db': 'tracker.db',
                'username': '',
                'password': ''
            },
            'event_broker': {
                'type': 'pika',
                'url': 'rabbitmq-service',
                'username': server_settings.rabbitmq_username,
                'password': server_settings.rabbitmq_password,
                'queues': [
                    'pilot'
                ]
            }
        }
        with open('data/endpoints.yml', 'w', encoding='utf-8') as f:
            yaml.dump(endpoints, f, allow_unicode=True)


if __name__ == "__main__":
    load_dotenv()
    fire.Fire(BootStrap)
