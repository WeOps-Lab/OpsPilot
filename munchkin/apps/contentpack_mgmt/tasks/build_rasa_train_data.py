import os
import shutil
import tempfile

import yaml
from apps.contentpack_mgmt.models import (
    BotActions,
    Intent,
    IntentCorpus,
    RasaEntity,
    RasaForms,
    RasaModel,
    RasaRules,
    RasaSlots,
    RasaStories,
)
from django.core.files import File
from loguru import logger

from celery import shared_task


class RasaTrainDataBuilder:
    def __init__(self, rasa_model_id):
        self.rasa_model_id = rasa_model_id
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = f"{self.temp_dir}/data"
        os.makedirs(self.data_dir)
        self.rasa_model = RasaModel.objects.get(id=self.rasa_model_id)

    def generate_config(self):
        config_dict = {
            "recipe": "default.v1",
            "assistant_id": "ops-pilot",
            "language": "zh",
        }
        config_dict.update(self.rasa_model.pipeline_config)
        config_dict.update(self.rasa_model.policies_config)

        with open(f"{self.temp_dir}/config.yml", "w", encoding="utf-8") as f:
            yaml.dump(config_dict, f, allow_unicode=True)
        logger.info(f"生成config.yml成功,路径:[{self.temp_dir}/config.yml]")

    def generate_domain(self):
        domain_dict = {
            "version": "3.1",
            "session_config": {
                "session_expiration_time": 60,
                "carry_over_slots_to_new_session": True,
            },
            "intents": [],
            "actions": [],
            "entities": [],
            "slots": {},
            "forms": {},
        }

        content_packs = self.rasa_model.content_packs.all()

        for obj in content_packs:
            self.add_intents_to_domain(obj, domain_dict)
            self.add_actions_to_domain(obj, domain_dict)
            self.add_entities_to_domain(obj, domain_dict)
            self.add_slots_to_domain(obj, domain_dict)
            self.add_forms_to_domain(obj, domain_dict)

        with open(f"{self.data_dir}/domain.yml", "w", encoding="utf-8") as f:
            yaml.dump(domain_dict, f, allow_unicode=True)
        logger.info(f"生成domain.yml成功,路径:[{self.data_dir}/domain.yml]")

    def add_intents_to_domain(self, content_pack, domain_dict):
        intents = Intent.objects.filter(content_pack=content_pack)
        for intent in intents:
            domain_dict["intents"].append(intent.name)

    def add_actions_to_domain(self, content_pack, domain_dict):
        actions = BotActions.objects.filter(content_pack=content_pack)
        for action in actions:
            domain_dict["actions"].append(action.name)

    def add_entities_to_domain(self, content_pack, domain_dict):
        entities = RasaEntity.objects.filter(content_pack=content_pack)
        for entity in entities:
            domain_dict["entities"].append(entity.name)

    def add_slots_to_domain(self, content_pack, domain_dict):
        slots = RasaSlots.objects.filter(content_pack=content_pack)
        for slot in slots:
            domain_dict["slots"].update(slot.slot)

    def add_forms_to_domain(self, content_pack, domain_dict):
        forms = RasaForms.objects.filter(content_pack=content_pack)
        for form in forms:
            domain_dict["forms"].update(form.form)

    def generate_nlu(self):
        nlu_content = 'version: "3.1"\n'
        nlu_content += "nlu:\n"

        content_packs = self.rasa_model.content_packs.all()
        for obj in content_packs:
            intents = Intent.objects.filter(content_pack=obj)
            for intent in intents:
                intent_corpus = IntentCorpus.objects.filter(intent=intent).all()

                if len(intent_corpus) > 0:
                    nlu_content += "  - intent: " + intent.name + "\n"
                    nlu_content += "    examples: |\n"

                    for corpus in intent_corpus:
                        nlu_content += "      - " + corpus.corpus + "\n"

        with open(f"{self.data_dir}/nlu.yml", "w", encoding="utf-8") as f:
            f.write(nlu_content)
        logger.info(f"生成nlu.yml成功,路径:[{self.data_dir}/nlu.yml]")

    def generate_rules_and_stories(self):
        rules_dict = {"version": "3.1", "rules": []}
        stories_dict = {"version": "3.1", "stories": []}

        content_packs = self.rasa_model.content_packs.all()
        for obj in content_packs:
            rasa_rules = RasaRules.objects.filter(content_pack=obj).all()
            for rule in rasa_rules:
                rules_dict["rules"].append({"rule": rule.name, **rule.rule_steps})

            rasa_stories = RasaStories.objects.filter(content_pack=obj).all()
            for story in rasa_stories:
                stories_dict["stories"].append({"story": story.name, **story.story_steps})

        with open(f"{self.data_dir}/rules.yml", "w", encoding="utf-8") as f:
            yaml.dump(rules_dict, f, allow_unicode=True)

        with open(f"{self.data_dir}/stories.yml", "w", encoding="utf-8") as f:
            yaml.dump(stories_dict, f, allow_unicode=True)

    def save_to_model(self):
        shutil.make_archive(f"{self.temp_dir}", "zip", self.temp_dir)

        with open(f"{self.temp_dir}.zip", "rb") as f:
            self.rasa_model.train_data_file = File(f, name=os.path.basename(f.name))
            self.rasa_model.save()

        shutil.rmtree(self.temp_dir)
        os.remove(f"{self.temp_dir}.zip")


@shared_task
def build_rasa_train_data(rasa_model_id):
    builder = RasaTrainDataBuilder(rasa_model_id)
    builder.generate_config()
    builder.generate_domain()
    builder.generate_nlu()
    builder.generate_rules_and_stories()
    builder.save_to_model()
