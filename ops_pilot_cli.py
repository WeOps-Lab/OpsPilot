import os
import subprocess
import uuid

import fire
from dotenv import load_dotenv
from loguru import logger
from supabase import create_client, Client

from actions.constants.server_settings import server_settings


class BootStrap(object):
    def prepare_train_data(self, bot_name: str):
        """
        准备训练数据
        :param bot_name:
        :return:
        """
        logger.info(f'创建临时目录......')
        tmp_path = f'tmp/{str(uuid.uuid4())}'
        os.makedirs(tmp_path, exist_ok=True)

        supabase: Client = create_client(server_settings.supabase_url, server_settings.supabase_key)
        supabase.auth.sign_in_with_password({
            'email': server_settings.supabase_username,
            'password': server_settings.supabase_password
        })
        try:
            logger.info(f'获取机器人训练数据')
            bot = supabase.table('ops_pilot_bot').select('*').eq('name', bot_name).execute().data[0]

            logger.info('准备规则数据....')
            rules = supabase.table('ops_pilot_bot_rule').select('ops_pilot_rule(*)').eq('bot_id',
                                                                                        bot['id']).execute().data

            logger.info('准备故事数据....')
            stories = supabase.table('ops_pilot_bot_story').select('ops_pilot_story(*)').eq('bot_id',
                                                                                            bot['id']).execute().data

            logger.info('准备动作数据....')
            actions = supabase.table('ops_pilot_actions').select('*').execute().data

            logger.info('准备实体数据....')
            entities = supabase.table('ops_pilot_entity').select('*').execute().data

            logger.info('准备表单数据....')
            forms = supabase.table('ops_pilot_form').select('*').execute().data

            logger.info('准备意图数据....')
            intents = supabase.table('ops_pilot_intent').select('name,ops_pilot_intent_corpus(corpus)').execute().data

            logger.info('准备响应数据....')
            responses = supabase.table('ops_pilot_response').select(
                'name,ops_pilot_response_corpus(corpus)').execute().data

            logger.info('准备槽位数据....')
            slots = supabase.table('ops_pilot_slot').select('*').execute().data

        except Exception as e:
            logger.error(f'获取机器人训练数据失败, {e}')
            return

        supabase.auth.sign_out()

    def train(self, domain_path, model_name):
        """
        训练模型
        :param domain_path:
        :param model_name:
        :return:
        """
        process = subprocess.Popen(f"rasa train --domain {domain_path} --fixed-model-name {model_name}",
                                   stdout=subprocess.PIPE,
                                   shell=True)

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

    def upload_model(self, model_path, model_name):
        """
        上传模型
        :param model_path:
        :param model_name:
        :return:
        """
        supabase: Client = create_client(server_settings.supabase_url, server_settings.supabase_key)
        supabase.auth.sign_in_with_password({
            'email': server_settings.supabase_username,
            'password': server_settings.supabase_password
        })
        try:
            with open(model_path, 'rb') as f:
                model = f.read()
                supabase.storage.from_('models').upload(f'{model_name}', model)
        except Exception as e:
            logger.error(f'上传模型失败, {e}')
            return
        supabase.auth.sign_out()


if __name__ == "__main__":
    load_dotenv()
    fire.Fire(BootStrap)
