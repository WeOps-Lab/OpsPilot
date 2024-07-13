from apps.bot_mgmt.models import Bot, RasaModel, AutomationSkill, AUTOMATION_SKILL_CHOICES


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

        AutomationSkill.objects.get_or_create(
            skill_id="list_jenkins_jobs",
            skill_type=AUTOMATION_SKILL_CHOICES.SALT_STACK,
            defaults={
                "name": "Jenkins任务列表",
                "skill_config": {
                    "client": "local",
                    "tgt": "ops-pilot",
                    "fun": "cmd.run",
                    "args": "curl -sS -u <username>:<password> 'http://<jenkins_base_url>/api/json'"
                },
            }
        )
