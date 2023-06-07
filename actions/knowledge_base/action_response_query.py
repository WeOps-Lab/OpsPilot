import os
import json

from typing import Any, Dict, List, Text

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.utils import SLOT_OBJECT_TYPE, SLOT_LAST_OBJECT_TYPE, SLOT_ATTRIBUTE

USE_NEO4J = bool(os.getenv("USE_NEO4J", False))

if USE_NEO4J:
    from neo4j_knowledge_base import Neo4jKnowledgeBase


class EnToZh:
    def __init__(self, data_file):
        with open(data_file, encoding='utf-8') as fd:
            self.data = json.load(fd)

    def __call__(self, key):
        return self.data.get(key, key)


class MyKnowledgeBaseAction(ActionQueryKnowledgeBase):
    def name(self) -> Text:
        return "action_response_query"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> List[
        Dict[Text, Any]]:
        object_type = tracker.get_slot(SLOT_OBJECT_TYPE)
        last_object_type = tracker.get_slot(SLOT_LAST_OBJECT_TYPE)
        attribute = tracker.get_slot(SLOT_ATTRIBUTE)

        if last_object_type is None:
            new_request = False
        else:
            new_request = object_type != last_object_type

        if not object_type:
            dispatcher.utter_message(response="utter_ask_rephrase")
            return []

        if not attribute or new_request:
            return await self._query_objects(dispatcher, object_type, tracker)
        elif attribute:
            results = []
            for fields in attribute:
                results.append(await self._query_attribute(
                    dispatcher, object_type, fields, tracker
                ))
            return results

        dispatcher.utter_message(response="utter_ask_rephrase")
        return []

    def __init__(self):
        if USE_NEO4J:
            print("using Neo4jKnowledgeBase")
            knowledge_base = Neo4jKnowledgeBase(
                "bolt://localhost:7687", "neo4j", "43215678"
            )
        else:
            print("using InMemoryKnowledgeBase")
            knowledge_base = InMemoryKnowledgeBase("./actions/knowledge_base/data/data.json")

        super().__init__(knowledge_base)

        self.en_to_zh = EnToZh("./actions/knowledge_base/data/en_to_zh.json")

    async def utter_objects(
            self,
            dispatcher: CollectingDispatcher,
            object_type: Text,
            objects: List[Dict[Text, Any]],
    ) -> None:
        """
        Utters a response to the user that lists all found objects.
        Args:
            dispatcher: the dispatcher
            object_type: the object type
            objects: the list of objects
        """
        if objects:
            dispatcher.utter_message(text="找到下列{}:".format(self.en_to_zh(object_type)))

            repr_function = await self.knowledge_base.get_representation_function_of_object(
                object_type
            )

            for i, obj in enumerate(objects, 1):
                dispatcher.utter_message(text=f"{i}: {repr_function(obj)}")
        else:
            dispatcher.utter_message(
                text="我没找到任何{}.".format(self.en_to_zh(object_type))
            )

    def utter_attribute_value(
            self,
            dispatcher: CollectingDispatcher,
            object_name: Text,
            attribute_name: Text,
            attribute_value: Text,
    ) -> None:
        """
        Utters a response that informs the user about the attribute value of the
        attribute of interest.
        Args:
            dispatcher: the dispatcher
            object_name: the name of the object
            attribute_name: the name of the attribute
            attribute_value: the value of the attribute
        """
        if attribute_value:
            dispatcher.utter_message(
                text="{}的{}:{}".format(
                    self.en_to_zh(object_name),
                    self.en_to_zh(attribute_name),
                    self.en_to_zh(attribute_value),
                )
            )
        else:
            dispatcher.utter_message(
                text="没有找到{}的{}。".format(
                    self.en_to_zh(object_name), self.en_to_zh(attribute_name)
                )
            )
