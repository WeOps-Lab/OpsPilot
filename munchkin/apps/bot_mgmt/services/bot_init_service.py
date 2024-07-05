from apps.bot_mgmt.models import Bot, RasaModel
from apps.bot_mgmt.models.integrations import Integrations
from apps.channel_mgmt.models import CHANNEL_CHOICES, Channel
from apps.model_provider_mgmt.models import LLMSkill


class BotInitService:
    def __init__(self, owner):
        self.owner = owner

    def init(self):
        rasa_model, created = RasaModel.objects.get_or_create(name="核心模型", description="核心模型",
                                                              owner=self.owner)
        if created:
            with open("support-files/data/ops-pilot.tar.gz", "rb") as f:
                rasa_model.model_file.save("core_model.tar.gz", f)
            rasa_model.save()

        bot, created = Bot.objects.get_or_create(
            name="OpsPilot",
            description="智能运维助理",
            assistant_id="ops-pilot",
            owner=self.owner,
            rasa_model=rasa_model,
        )

        Integrations.objects.get_or_create(
            name="Salt",
            bot_id=bot,
            integration_type="salt",
            defaults={
                "description": "SaltStack集成",
                "config": {
                    "base_url": "http://salt-master.ops-pilot:8000",
                    "username": "salt",
                    "password": "salt",
                }
            },
        )

        Integrations.objects.get_or_create(
            name="WeOps",
            bot_id=bot,
            integration_type="weops",
            defaults={
                "description": "WeOps集成",
                "config": {
                    "base_url": "http://weops.ops-pilot:8000",
                    "username": "weops",
                    "password": "weops",
                }
            },
        )

        Integrations.objects.get_or_create(
            name="Jenkins",
            bot_id=bot,
            integration_type="jenkins",
            defaults={
                "description": "Jenkins集成",
                "config": {
                    "base_url": "http://jenkins.ops-pilot:8000",
                    "username": "jenkins",
                    "password": "jenkins",
                }
            },
        )
