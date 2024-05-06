import os
import subprocess
import uuid

import fire
from dotenv import load_dotenv
from loguru import logger
from supabase import create_client, Client
import yaml
from actions.constants.server_settings import server_settings
from jinja2 import FileSystemLoader, Environment


class BootStrap(object):
    def prepare_train_data(self, bot_name: str):
        """
        准备训练数据
        :param bot_name:
        :return:
        """
        jinja_env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True,
                                lstrip_blocks=True, )

        logger.info(f'创建临时目录......')
        tmp_path = f'tmp/'
        os.makedirs(tmp_path, exist_ok=True)

        supabase: Client = create_client(server_settings.supabase_url, server_settings.supabase_key)
        supabase.auth.sign_in_with_password({
            'email': server_settings.supabase_username,
            'password': server_settings.supabase_password
        })
        try:
            logger.info(f'获取机器人训练数据')
            bot = supabase.table('ops_pilot_bot').select('*').eq('name', bot_name).execute().data[0]
            with open(f'{tmp_path}/credentials.yml', 'w') as f:
                f.write(bot['credentials_config'])
            with open(f'{tmp_path}/config.yml', 'w') as f:
                f.write(bot['train_config'])
            with open(f'{tmp_path}/endpoints.yml', 'w') as f:
                f.write(bot['endpoints_config'])
            logger.info('准备规则数据....')
            rules = supabase.table('ops_pilot_bot_rule').select('ops_pilot_rule(*)').eq('bot_id',
                                                                                        bot['id']).execute().data

            rule_dict = {
                "version": "3.1",
                "rules": []
            }
            for rule in rules:
                rule_dict['rules'].append(yaml.safe_load(rule['ops_pilot_rule']['steps']))
            with open(f'{tmp_path}/rules.yml', 'w') as f:
                yaml.dump(rule_dict, f, default_flow_style=False, allow_unicode=True, encoding='utf-8')

            stories_dict = {
                "version": "3.1",
                "stories": []
            }
            logger.info('准备故事数据....')
            stories = supabase.table('ops_pilot_bot_story').select('ops_pilot_story(*)').eq('bot_id',
                                                                                            bot['id']).execute().data
            for story in stories:
                rule_dict['stories'].append(yaml.safe_load(story['ops_pilot_story']['steps']))
            with open(f'{tmp_path}/stories.yml', 'w') as f:
                yaml.dump(stories_dict, f, default_flow_style=False, allow_unicode=True, encoding='utf-8')

            logger.info('准备动作数据....')

            nlu_dict = {
                "version": "3.1",
                "nlu": []
            }
            domain_dict = {
                "version": "3.1",
                "intents": [],
                "entities": [],
                "slots": {},
                "actions": [],
                "forms": {}
            }
            actions = supabase.table('ops_pilot_actions').select('*').execute().data
            domain_dict['actions'] = [action['name'] for action in actions]

            logger.info('准备实体数据....')
            entities = supabase.table('ops_pilot_entity').select('*').execute().data
            domain_dict['entities'] = [entity['name'] for entity in entities]

            logger.info('准备表单数据....')
            forms = supabase.table('ops_pilot_form').select('*').execute().data
            for form in forms:
                domain_dict['forms'].update(yaml.safe_load(form['form_config']))

            logger.info('准备槽位数据....')
            slots = supabase.table('ops_pilot_slot').select('*').execute().data
            for slot in slots:
                domain_dict['slots'].update(yaml.safe_load(slot['slot_config']))

            logger.info('准备意图数据....')
            intents = supabase.table('ops_pilot_intent').select('name,ops_pilot_intent_corpus(corpus)').execute().data
            for intent in intents:
                nlu_dict['nlu'].append({
                    'intent': intent['name'],
                    'examples': ''.join(['- ' + x['corpus'] + '\n' for x in intent['ops_pilot_intent_corpus']])
                })
                domain_dict['intents'].append(intent['name'])

            with open(f'{tmp_path}/domain.yml', 'w') as f:
                yaml.dump(domain_dict, f, default_flow_style=False, allow_unicode=True, encoding='utf-8')

            with open(f'{tmp_path}/nlu.yml', 'w') as f:
                yaml.dump(nlu_dict, f, default_flow_style=False, allow_unicode=True, encoding='utf-8')

            logger.info('准备响应数据....')
            responses = supabase.table('ops_pilot_response').select(
                'name,ops_pilot_response_corpus(corpus)').execute().data
            response_dict = {
                "version": "3.1",
                "responses": {}
            }
            for response in responses:
                response_dict['responses'][response['name']] = []
                for x in response['ops_pilot_response_corpus']:
                    response_dict['responses'][response['name']].append({
                        'text': x['corpus'],
                    })
            with open(f'{tmp_path}/responses.yml', 'w') as f:
                yaml.dump(response_dict, f, default_flow_style=False, allow_unicode=True, encoding='utf-8')

        except Exception as e:
            logger.error(f'获取机器人训练数据失败, {e}')
            return

        supabase.auth.sign_out()

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
