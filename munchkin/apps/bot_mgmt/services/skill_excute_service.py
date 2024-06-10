from loguru import logger

from apps.bot_mgmt.models import Bot, BotSkillRule
from apps.model_provider_mgmt.services.llm_service import llm_service


class SkillExecuteService:
    def execute_skill(self, bot_id, action_name, user_message, chat_history, sender_id):
        logger.info(f'执行[{bot_id}]的[{action_name}]动作,用户消息: {user_message}')

        bot = Bot.objects.get(id=bot_id)
        llm_skill = bot.llm_skills.filter(skill_id=action_name).first()

        super_system_prompt = None
        if sender_id:
            if BotSkillRule.objects.filter(rule_user__user_id__in=sender_id).exists():
                logger.info(f'识别到用户[{sender_id}]的个性化规则,切换系统技能提示词')
                super_system_prompt = BotSkillRule.objects.filter(rule_user__user_id__in=sender_id).first().prompt

        result = llm_service.chat(llm_skill, user_message, chat_history, super_system_prompt)
        return result
