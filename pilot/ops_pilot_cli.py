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

    def get_bot_config_data(self):
        logger.info(f'获取Pilot[{server_settings.munchkin_bot_id}]配置信息....')

        credentials = {
            'socketio': {
                'user_message_evt': 'user_uttered',
                'bot_message_evt': 'bot_uttered',
                'session_persistence': False,
            },
            # TODO: 后续移动为Munchkin配置
            'channels.automation_channel.AutomationChannel': {
                'secret_token': 'ops-pilot'
            }
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
                'url': f'{server_settings.munchkin_base_url}/api/rasa_model/model_download?bot_id={server_settings.munchkin_bot_id}',
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
