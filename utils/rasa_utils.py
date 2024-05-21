import tiktoken
from rasa_sdk import Tracker
from loguru import logger


class RasaUtils:
    @staticmethod
    def log_error(tracker: Tracker, content):
        logger.error(f'通道:[{tracker.get_latest_input_channel()}],会话ID:[{tracker.sender_id}]. {content}')

    @staticmethod
    def log_info(tracker: Tracker, content):
        logger.info(f'通道:[{tracker.get_latest_input_channel()}],会话ID:[{tracker.sender_id}]. {content}')

    @staticmethod
    def load_chat_history(tracker: Tracker, max_history: int, limit_token=None):
        """
        获取聊天历史对话记录
        :param tracker:
        :param max_history: 最大对话记录数
        :return:
        """
        events = list(
            filter(
                lambda x: x.get("event") == "user" or x.get("event") == "bot",
                tracker.events[:-1],
            )
        )

        conversation_history = ""
        for index, event in enumerate(reversed(events)):
            if index >= max_history:
                break
            if limit_token is not None and len(
                    tiktoken.get_encoding('cl100k_base').encode(conversation_history)) >= limit_token:
                break

            conversation_history += f"{'assistant:' if event.get('event') == 'bot' else 'user:'} {event['text']}\n"
        return conversation_history

    @staticmethod
    def get_tracker_entity(tracker: Tracker, entity_key: str):
        """
        获取指定实体对象
        :param tracker:
        :param entity_key:
        :return:
        """
        entities = tracker.latest_message.get('entities')
        target_entity = next(
            (x['value'] for x in entities if x['entity'] == entity_key),
            None
        )
        return target_entity
