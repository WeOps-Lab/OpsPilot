from loguru import logger
from rasa_sdk import Tracker


def log_error(tracker: Tracker, content):
    logger.error(f'通道:[{tracker.get_latest_input_channel()}],会话ID:[{tracker.sender_id}]. {content}')


def log_info(tracker: Tracker, content):
    logger.info(f'通道:[{tracker.get_latest_input_channel()}],会话ID:[{tracker.sender_id}]. {content}')
