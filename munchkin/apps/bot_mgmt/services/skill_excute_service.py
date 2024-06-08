from typing import Dict

from BCEmbedding.tools.langchain import BCERerank
from langchain.memory import ChatMessageHistory
from langchain.retrievers import ContextualCompressionRetriever
from langchain_elasticsearch import ElasticsearchRetriever
from loguru import logger

from apps.bot_mgmt.models import Bot, BotSkillRule
from apps.contentpack_mgmt.models import BotActions
from apps.core.utils.embedding_driver import EmbeddingDriver
from apps.core.utils.llm_driver import LLMDriver
from apps.model_provider_mgmt.models import RerankModelChoices
from munchkin.components.elasticsearch import ELASTICSEARCH_URL, ELASTICSEARCH_PASSWORD


class SkillExecuteService:
    def execute_skill(self, bot_id, action_name, user_message, chat_history, sender_id):
        logger.info(f'执行[{bot_id}]的[{action_name}]动作,用户消息: {user_message}')

        context = ''

        bot = Bot.objects.get(id=bot_id)
        llm_skill = bot.llm_skills.filter(skill_id=action_name).first()

        if llm_skill.enable_rag:
            knowledge_base_folder_list = llm_skill.knowledge_base_folders.all()
            for knowledge_base_folder in knowledge_base_folder_list:
                embedding = EmbeddingDriver().get_embedding(knowledge_base_folder.embed_model)

                index_name = f"knowledge_base_{knowledge_base_folder.id}"

                vector_retriever = ElasticsearchRetriever.from_es_params(
                    index_name=index_name,
                    body_func=lambda x: self.vector_query(x, embedding,
                                                          knowledge_base_folder.rag_k,
                                                          knowledge_base_folder.rag_num_candidates,
                                                          knowledge_base_folder.text_search_weight,
                                                          knowledge_base_folder.vector_search_weight),
                    content_field='text',
                    url=ELASTICSEARCH_URL,
                    username='elastic',
                    password=ELASTICSEARCH_PASSWORD
                )

                if knowledge_base_folder.enable_rerank is False:
                    result = vector_retriever.invoke(user_message)
                else:
                    if knowledge_base_folder.rerank_model.rerank_model == RerankModelChoices.BCE:
                        reranker_args = {'model': knowledge_base_folder.rerank_model.rerank_config['model'],
                                         'top_n': knowledge_base_folder.rerank_top_k}
                        reranker = BCERerank(**reranker_args)

                    compression_retriever = ContextualCompressionRetriever(
                        base_compressor=reranker, base_retriever=vector_retriever
                    )
                    result = compression_retriever.get_relevant_documents(user_message)
                    logger.info(f'Rerank结果: {result}')

                for r in result:
                    context += r.page_content.replace('{', '').replace('}', '') + '\n'

        llm_model = llm_skill.llm_model
        llm_driver = LLMDriver(llm_model)

        system_skill_prompt = llm_skill.skill_prompt

        if sender_id:
            if BotSkillRule.objects.filter(rule_user__user_id__in=sender_id).exists():
                logger.info(f'识别到用户[{sender_id}]的个性化规则,切换系统技能提示词')
                system_skill_prompt = BotSkillRule.objects.filter(rule_user__user_id__in=sender_id).first().prompt
        if llm_skill.enable_conversation_history:
            llm_chat_history = ChatMessageHistory()
            for event in chat_history:
                if event['event'] == 'user':
                    llm_chat_history.add_user_message(event['text'])
                elif event['event'] == 'bot':
                    llm_chat_history.add_ai_message(event['text'])

            result = llm_driver.openai_chat_with_history(
                system_message_prompt=system_skill_prompt,
                user_message=user_message,
                message_history=llm_chat_history,
                window_size=llm_skill.conversation_window_size,
                rag_content=context
            )

        else:
            result = llm_driver.chat(
                system_message_prompt=system_skill_prompt,
                user_message=user_message,
            )

        if result.startswith("AI:"):
            result = result[4:]

        return result

    def vector_query(self, search_query: str, embeddings,
                     k, num_candidates,
                     text_search_weight=0.9,
                     vector_search_weight=0.1) -> Dict:
        vector = embeddings.embed_query(search_query)
        return {
            "query": {
                "match": {
                    'text': {
                        "query": search_query,
                        "boost": text_search_weight
                    }
                },
            },
            "knn": {
                "field": 'vector',
                "query_vector": vector,
                "k": k,
                "num_candidates": num_candidates,
                "filter": {
                    "term": {
                        "text": "knowledge_base",
                    },
                },
                "boost": vector_search_weight
            }
        }