from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.model_provider_mgmt.models import LLMSkill
from apps.model_provider_mgmt.utils.llm_driver import LLMDriver
from langchain.memory import ChatMessageHistory


class LLMService:
    def __init__(self):
        self.knowledge_search_service = KnowledgeSearchService()

    def chat(self, llm_skill: LLMSkill, user_message, chat_history):
        llm_model = llm_skill.llm_model
        llm_driver = LLMDriver(llm_model)

        system_skill_prompt = llm_skill.skill_prompt

        context = ""
        rag_result = []
        if llm_skill.enable_rag:
            knowledge_base_folder_list = llm_skill.knowledge_base_folders.all()
            rag_result = self.knowledge_search_service.search(knowledge_base_folder_list, user_message,
                                                              score_threshold=llm_skill.rag_score_threshold)

            for r in rag_result:
                context += r['content'].replace("{", "").replace("}", "") + "\n"

        if llm_skill.enable_conversation_history:
            llm_chat_history = ChatMessageHistory()

            for event in chat_history:
                if event["event"] == "user":
                    llm_chat_history.add_user_message(event["text"])
                elif event["event"] == "bot":
                    llm_chat_history.add_ai_message(event["text"])

            result = llm_driver.chat_with_history(
                system_message_prompt=system_skill_prompt,
                user_message=user_message,
                message_history=llm_chat_history,
                window_size=llm_skill.conversation_window_size,
                rag_content=context,
            )
        else:
            system_skill_prompt = system_skill_prompt.replace("{", "").replace("}", "")
            result = llm_driver.chat(
                system_message_prompt=system_skill_prompt,
                user_message=user_message,
            )

        if result.startswith("AI:"):
            result = result[4:]

        if llm_skill.enable_rag_knowledge_source:
            knowledge_titles = set([x['knowledge_title'] for x in rag_result])
            result += '\n'
            result += f'知识库来源: {", ".join(knowledge_titles)}'

        return result


llm_service = LLMService()
