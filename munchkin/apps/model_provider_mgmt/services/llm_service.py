from langserve import RemoteRunnable

from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.model_provider_mgmt.models import LLMSkill, LLMModelChoices
from munchkin.components.remote_service import OPENAI_CHAT_SERVICE_URL


class LLMService:
    def __init__(self):
        self.knowledge_search_service = KnowledgeSearchService()

    def chat(self, llm_skill: LLMSkill, user_message, chat_history):
        llm_model = llm_skill.llm_model

        context = """
以下是提供给你的背景知识,背景知识的格式如下:
--------
知识标题: [标题]
知识内容: [内容]
--------
            
        """
        rag_result = []
        if llm_skill.enable_rag:
            knowledge_base_folder_list = llm_skill.knowledge_base_folders.all()
            rag_result = self.knowledge_search_service.search(knowledge_base_folder_list, user_message,
                                                              score_threshold=llm_skill.rag_score_threshold)
            for r in rag_result:
                context += "--------"
                context += f"知识标题:[{r['knowledge_title']}"
                context += f"知识内容:[{r['content'].replace('{', '').replace('}', '')}]"
                context += "--------"

        if llm_model.llm_model_type == LLMModelChoices.CHAT_GPT:
            chat_server = RemoteRunnable(OPENAI_CHAT_SERVICE_URL)
            result = chat_server.invoke({
                "system_message_prompt": llm_skill.skill_prompt,
                "openai_api_base": llm_model.decrypted_llm_config['openai_base_url'],
                "openai_api_key": llm_model.decrypted_llm_config['openai_api_key'],
                "temperature": llm_model.decrypted_llm_config['temperature'],
                "model": llm_model.decrypted_llm_config['model'],
                "user_message": user_message,
                "chat_history": chat_history,
                "conversation_window_size": llm_skill.conversation_window_size,
                "rag_context": context,
            })

        if llm_skill.enable_rag_knowledge_source:
            knowledge_titles = set([x['knowledge_title'] for x in rag_result])
            result += '\n'
            result += f'知识库来源: {", ".join(knowledge_titles)}'

        return result


llm_service = LLMService()
