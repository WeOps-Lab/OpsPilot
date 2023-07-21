from typing import Any, Text, Dict, List

from rasa.shared.core.slots import Slot
from rasa_sdk import Action, Tracker, logger
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.core_utils import get_regex_entities


class ActionSetEntitiesValues(Action):

    def name(self) -> Text:
        return "action_set_entities_values"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = list(
            filter(lambda d: d['extractor'] == 'RegexEntityExtractor',
                   tracker.latest_message['entities']))
        slots = []
        for entity in entities:
            slots.append(Slot(entity['entity'], entity['value']))
        return slots
