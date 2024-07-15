from apps.bot_mgmt.models import Bot, BotSkillRule
from apps.model_provider_mgmt.services.llm_service import llm_service
from loguru import logger


class SkillExecuteService:
    def execute_skill(self, bot_id, action_name, user_message, chat_history, sender_id):
        logger.info(f"执行[{bot_id}]的[{action_name}]动作,发送者ID:[{sender_id}],消息: {user_message}")

        bot = Bot.objects.get(id=bot_id)
        llm_skill = bot.llm_skills.get(skill_id=action_name)

        if sender_id:
            # TODO: 要配合pilot改造，把通道带上，暂时不支持用户组和通道过滤
            if BotSkillRule.objects.filter(rule_user__user_id=sender_id, bot_id=bot,
                                           llm_skill__skill_id=action_name).exists():
                logger.info(f"识别到用户[{sender_id}]的个性化规则,切换系统技能提示词")
                llm_skill = BotSkillRule.objects.get(rule_user__user_id=sender_id, bot_id=bot,
                                                     llm_skill__skill_id=action_name).llm_skill

        result = llm_service.chat(llm_skill, user_message, chat_history)
        return result
