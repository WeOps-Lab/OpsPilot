import os
import shutil
import tempfile
from django.core.files import File
import yaml
from loguru import logger
from celery import shared_task

from apps.contentpack_mgmt.models import RasaModel, Intent, BotActions, RasaEntity, RasaSlots, RasaForms, IntentCorpus, \
    RasaRules, RasaStories


@shared_task
def build_rasa_train_data(rasa_model_id):
    # 1. 创建临时文件夹
    temp_dir = tempfile.mkdtemp()

    # 2.获取RasaModel,并把pipeline_config和policies_config合并,dump到config.yml
    rasa_model = RasaModel.objects.get(id=rasa_model_id)
    config_dict = {
        "recipe": "default.v1",
        "assistant_id": "ops-pilot",
        "language": "zh",
    }
    config_dict.update(rasa_model.pipeline_config)
    config_dict.update(rasa_model.policies_config)
    with open(f'{temp_dir}/config.yml', 'w', encoding='utf-8') as f:
        yaml.dump(config_dict, f, allow_unicode=True)
    logger.info(f'生成config.yml成功,路径:[{temp_dir}/config.yml]')

    # 3.在临时目录下创建data文件夹
    data_dir = f'{temp_dir}/data'
    os.makedirs(data_dir)

    # 4. 创建domain.yml文件
    domain_dict = {
        "version": "3.1",
        "session_config": {
            "session_expiration_time": 60,
            "carry_over_slots_to_new_session": True
        },
        "intents": [],
        "actions": [],
        "entities": [],
        "slots": {},
        "forms": {}
    }

    content_packs = rasa_model.content_packs.all()
    for obj in content_packs:
        intents = Intent.objects.filter(content_pack=obj)
        for intent in intents:
            domain_dict['intents'].append(intent.name)

        actions = BotActions.objects.filter(content_pack=obj)
        for action in actions:
            domain_dict['actions'].append(action.name)

        entities = RasaEntity.objects.filter(content_pack=obj)
        for entity in entities:
            domain_dict['entities'].append(entity.name)

        slots = RasaSlots.objects.filter(content_pack=obj)
        for slot in slots:
            domain_dict['slots'].update(slot.slot)

        forms = RasaForms.objects.filter(content_pack=obj)
        for form in forms:
            domain_dict['forms'].update(form.form)

    # dump domain_dict to data/domain.yml
    with open(f'{data_dir}/domain.yml', 'w', encoding='utf-8') as f:
        yaml.dump(domain_dict, f, allow_unicode=True)
    logger.info(f'生成domain.yml成功,路径:[{data_dir}/domain.yml]')

    # 生成nlu.yml文件到data/nlu.yml
    nlu_content = 'version: "3.1"\n'
    nlu_content += "nlu:\n"
    for intent in intents:
        intent_corpus = IntentCorpus.objects.filter(intent=intent).all()

        if len(intent_corpus) > 0:
            nlu_content += '  - intent: ' + intent.name + '\n'
            nlu_content += '    examples: |\n'

            for corpus in intent_corpus:
                nlu_content += '      - ' + corpus.corpus + '\n'

    with open(f'{data_dir}/nlu.yml', 'w', encoding='utf-8') as f:
        f.write(nlu_content)
    logger.info(f'生成nlu.yml成功,路径:[{data_dir}/nlu.yml]')

    # 生成rules.yml文件到data/rules.yml
    rules_dict = {
        "version": "3.1",
        "rules": []
    }
    rasa_rules = RasaRules.objects.filter(content_pack=obj).all()
    for rule in rasa_rules:
        rules_dict['rules'].append({
            "rule": rule.name,
            **rule.rule_steps
        })
    with open(f'{data_dir}/rules.yml', 'w', encoding='utf-8') as f:
        yaml.dump(rules_dict, f, allow_unicode=True)

    rasa_stories = RasaStories.objects.filter(content_pack=obj).all()
    stories_dict = {
        "version": "3.1",
        "stories": []
    }
    for story in rasa_stories:
        stories_dict['stories'].append({
            "story": story.name,
            **story.story_steps

        })
    with open(f'{data_dir}/stories.yml', 'w', encoding='utf-8') as f:
        yaml.dump(stories_dict, f, allow_unicode=True)

    # 把temp_dir打包成zip包
    shutil.make_archive(f'{temp_dir}', 'zip', temp_dir)

    # 把文件保存到rasa_model.train_data_file中
    with open(f'{temp_dir}.zip', 'rb') as f:
        rasa_model.train_data_file = File(f, name=os.path.basename(f.name))
        rasa_model.save()
    # final. 删除临时文件夹
    shutil.rmtree(temp_dir)

    # 删除zip包
    os.remove(f'{temp_dir}.zip')
