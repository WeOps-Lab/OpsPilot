from apps.bot_mgmt.models import Bot, RasaModel
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
