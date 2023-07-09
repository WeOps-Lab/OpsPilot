import re

from rasa_sdk import Tracker


def get_regex_entities(tracker: Tracker, entity_name):
    entities = list(
        filter(lambda d: d['entity'] == entity_name and d['extractor'] == 'RegexEntityExtractor',
               tracker.latest_message['entities']))
    return entities


def is_valid_url(url: str) -> bool:
    """
    判断字符串是否为有效的URL
    Args:
        url: 待验证的URL字符串
    Returns:
        如果URL有效则返回True，否则返回False
    """
    pattern = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    return bool(pattern.match(url))
