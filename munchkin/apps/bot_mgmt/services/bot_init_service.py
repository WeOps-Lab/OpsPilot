from apps.bot_mgmt.models import Bot, RasaModel, AutomationSkill, AUTOMATION_SKILL_CHOICES, Integration, \
    INTEGRATION_CHOICES


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

        jenkins_integration, created = Integration.objects.get_or_create(
            name="jenkins",
            integration=INTEGRATION_CHOICES.JENKINS,
            defaults={
                "integration_config": {
                    "base_url": "http://<jenkins_base_url>",
                    "username": "<username>",
                    "token": "<token>",
                }

            }
        )

        AutomationSkill.objects.get_or_create(
            skill_id="list_jenkins_jobs",
            skill_type=AUTOMATION_SKILL_CHOICES.SALT_STACK,
            integration=jenkins_integration,
            defaults={
                "name": "Jenkins任务列表",
                "skill_config": {
                    "client": "local",
                    "tgt": "ops-pilot",
                    "fun": "cmd.run",
                    "args": "curl -sS -u {{username}}:{{token}} '{{base_url}}/api/json'"
                },
            }
        )

        AutomationSkill.objects.get_or_create(
            skill_id="jenkins_build_logs",
            skill_type=AUTOMATION_SKILL_CHOICES.SALT_STACK,
            integration=jenkins_integration,
            defaults={
                "name": "Jenkins构建日志",
                "skill_config": {
                    "client": "local",
                    "tgt": "ops-pilot",
                    "fun": "cmd.run",
                    "args": "curl -sS -u {{username}}:{{token}} '{{base_url}}/job/{{job_name}}/{{build_number}}/consoleText'"
                },
            }
        )

        AutomationSkill.objects.get_or_create(
            skill_id="jenkins_build",
            skill_type=AUTOMATION_SKILL_CHOICES.SALT_STACK,
            integration=jenkins_integration,
            defaults={
                "name": "Jenkins构建任务",
                "skill_config": {
                    "client": "local",
                    "tgt": "ops-pilot",
                    "fun": "cmd.run",
                    "args": "curl -X POST -sS -u {{username}}:{{token}} '{{base_url}}/job/{{job_name}}/build'"
                },
            }
        )

        AutomationSkill.objects.get_or_create(
            skill_id="jenkins_last_build_number",
            skill_type=AUTOMATION_SKILL_CHOICES.SALT_STACK,
            integration=jenkins_integration,
            defaults={
                "name": "获取Jenkins最后的构建号",
                "skill_config": {
                    "client": "local",
                    "tgt": "ops-pilot",
                    "fun": "cmd.run",
                    "args": "curl -sS -u {{username}}:{{token}} '{{base_url}}/job/{{job_name}}/lastBuild/buildNumber'"
                },
            }
        )

        AutomationSkill.objects.get_or_create(
            skill_id="jenkins_build_status",
            skill_type=AUTOMATION_SKILL_CHOICES.SALT_STACK,
            integration=jenkins_integration,
            defaults={
                "name": "Jenkins任务构建状态",
                "skill_config": {
                    "client": "local",
                    "tgt": "ops-pilot",
                    "fun": "cmd.run",
                    "args": "curl -sS -u {{username}}:{{token}} '{{base_url}}/job/{{job_name}}/{{build_number}}/api/json'"
                },
            }
        )
