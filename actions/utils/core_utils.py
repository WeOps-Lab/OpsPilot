from rasa_sdk import Tracker


def get_regex_entities(tracker: Tracker, entity_name):
    entities = list(
        filter(lambda d: d['entity'] == entity_name and d['extractor'] == 'RegexEntityExtractor',
               tracker.latest_message['entities']))
    return entities
