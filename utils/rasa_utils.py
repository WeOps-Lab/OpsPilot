from rasa_sdk import Tracker


def load_chat_history(tracker: Tracker, max_history: int):
    events = list(
        filter(
            lambda x: x.get("event") == "user"
                      or x.get("event") == "bot",
            tracker.events,
        )
    )
    user_messages = []
    for event in reversed(events):
        if len(user_messages) >= max_history:
            break
        user_messages.insert(0, event)
    user_prompt = ""
    for user_message in user_messages:
        user_prompt += f"{user_message['text']}\n"
    return user_prompt


def get_tracker_entity(tracker: Tracker, entity_key):
    entities = tracker.latest_message.get('entities')
    content = next(
        (x['value'] for x in entities if x['entity'] == entity_key),
        None
    )
    return content
