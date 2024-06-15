from apps.bot_mgmt.models import Bot
from apps.channel_mgmt.models import CHANNEL_CHOICES, Channel
from apps.contentpack_mgmt.models import RasaModel
from apps.model_provider_mgmt.models import LLMSkill


class BotInitService:
    def __init__(self, owner):
        self.owner = owner

    def init(self):
        rasa_model = RasaModel.objects.filter(name="核心模型", owner=self.owner).first()
        ops_pilot, created = Bot.objects.get_or_create(
            name="OpsPilot",
            description="智能运维助理",
            assistant_id="ops-pilot",
            owner=self.owner,
            rasa_model=rasa_model,
        )
        if created:
            llm_skill = LLMSkill.objects.filter(name="开放问答(GPT3.5-16k)").first()
            ops_pilot.llm_skills.add(llm_skill)

            ops_pilot.channels.add(Channel.objects.get(channel_type=CHANNEL_CHOICES.WEB))
            ops_pilot.save()
