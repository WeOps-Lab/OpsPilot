from typing import List

from langserve import RemoteRunnable

from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.model_provider_mgmt.models import LLMSkill, LLMModelChoices
from munchkin.components.remote_service import OPENAI_CHAT_SERVICE_URL, RAG_SERVER_URL, ONLINE_SEARCH_SERVER_URL
from langchain_core.documents import Document


class LLMService:
    def __init__(self):
        self.knowledge_search_service = KnowledgeSearchService()

    def chat(self, llm_skill: LLMSkill, user_message, chat_history, enable_online_search=False):
        llm_model = llm_skill.llm_model

        rag_result = []
        context = ""

        if llm_skill.enable_rag:
            knowledge_base_folder_list = llm_skill.knowledge_base_folders.all()
            rag_result = self.knowledge_search_service.search(knowledge_base_folder_list, user_message,
                                                              score_threshold=llm_skill.rag_score_threshold)
            context += """
            以下是提供给你的背景知识,背景知识的格式如下:
            --------
            知识标题: [标题]
            知识内容: [内容]
            --------

             """
            for r in rag_result:
                context += "--------\n"
                context += f"知识标题:[{r['knowledge_title']}\n"
                context += f"知识内容:[{r['content'].replace('{', '').replace('}', '')}]\n"

        if enable_online_search:
            rag_server = RemoteRunnable(ONLINE_SEARCH_SERVER_URL)
            online_search_result: List[Document] = rag_server.invoke(
                {
                    "query": user_message,
                }
            )
            context += "--------\n"
            context += "以下是联网在线搜索结果:\n"
            for r in online_search_result:
                context += f"标题:[{r.page_content}\n"

        if llm_model.llm_model_type == LLMModelChoices.CHAT_GPT:
            chat_server = RemoteRunnable(OPENAI_CHAT_SERVICE_URL)
            result = chat_server.invoke({
                "system_message_prompt": llm_skill.skill_prompt,
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
            result += f'引用知识: {", ".join(knowledge_titles)}\n'

        if enable_online_search:
            result += '\n'
            result += f'网站来源:\n'
            for r in online_search_result:
                result += f"* [{r.metadata['title']}]({r.metadata['url']})\n"
        return result


llm_service = LLMService()
