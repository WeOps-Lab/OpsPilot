from typing import Dict

from langchain.memory import ChatMessageHistory
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_elasticsearch import ElasticsearchRetriever

from apps.contentpack_mgmt.models import BotActions
from apps.core.utils.llm_driver import LLMDriver
from apps.model_provider_mgmt.models import EmbedModelChoices
from munchkin.components.elasticsearch import ELASTICSEARCH_URL, ELASTICSEARCH_PASSWORD


class RagService:
    def bot_action_skill(self, bot_id, action_name, user_message, chat_history):
        context = ''

        bot_actions = BotActions.objects.filter(
            content_pack__rasamodel__bot=bot_id,
            name=action_name
        ).first()
        knowledge_base_folder_list = bot_actions.llm_skill.knowledge_base_folders.all()
        for knowledge_base_folder in knowledge_base_folder_list:
            if knowledge_base_folder.embed_model.embed_model == EmbedModelChoices.FASTEMBED:
                model_configs = knowledge_base_folder.embed_model.embed_config
                embedding = FastEmbedEmbeddings(model_name=model_configs['model'], cache_dir='models')

            index_name = f"knowledge_base_{knowledge_base_folder.id}"

            vector_retriever = ElasticsearchRetriever.from_es_params(
                index_name=index_name,
                body_func=lambda x: self.vector_query(x, embedding,
                                                      knowledge_base_folder.rag_k,
                                                      knowledge_base_folder.rag_num_candidates),
                content_field='text',
                url=ELASTICSEARCH_URL,
                username='elastic',
                password=ELASTICSEARCH_PASSWORD
            )

            result = vector_retriever.invoke(user_message)

            for r in result:
                context += r.page_content.replace('{', '').replace('}', '') + '\n'

        llm_driver = LLMDriver()
        llm_model = bot_actions.llm_skill.llm_model
        if bot_actions.llm_skill.enable_rag:
            llm_chat_history = ChatMessageHistory()
            for event in chat_history:
                if event['event'] == 'user':
                    llm_chat_history.add_user_message(event['text'])
                elif event['event'] == 'bot':
                    llm_chat_history.add_ai_message(event['text'])

            result = llm_driver.openai_chat_with_history(
                openai_base_url=llm_model.llm_config['openai_base_url'],
                openai_api_key=llm_model.llm_config['openai_api_key'],
                system_message_prompt=bot_actions.llm_skill.skill_prompt,
                user_message=user_message,
                message_history=llm_chat_history,
                window_size=bot_actions.llm_skill.conversation_window_size,
                rag_content=context,
                model=llm_model.llm_model,
                temperature=0.7
            )
            if result.startswith("AI:"):
                result = result[4:]
        else:
            result = llm_driver.openai_chat(
                openai_base_url=llm_model.llm_config['openai_base_url'],
                openai_api_key=llm_model.llm_config['openai_api_key'],
                system_message_prompt=bot_actions.llm_skill.skill_prompt,
                user_message=user_message,
                model=llm_model.llm_model,
                temperature=0.7
            )
        return result

    #
    def vector_query(self, search_query: str, embeddings, k, num_candidates) -> Dict:
        vector = embeddings.embed_query(search_query)
        return {
            "query": {
                "match": {
                    'text': {
                        "query": search_query,
                        "boost": 0.9
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
                "boost": 0.1
            }
        }
