from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.constant.server_settings import server_settings
from actions.utils.jenkins_utils import list_jenkins_job


class ActionFindJenkinsPipeline(Action):
    def name(self) -> Text:
        return "action_list_jenkins_pipline"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if server_settings.enable_jenkins_skill is False:
            dispatcher.utter_message('OpsPilot没有启用Jenkins自动化能力....')
            return []

        results = list_jenkins_job()
        if len(results) > 10:
            message = f'Jenkins上的流水线共有[{len(results)}]个，这里是我列出来的其中十个:'
            dispatcher.utter_message(text=message)
            for i in results[:10]:
                dispatcher.utter_message(text=i)
        else:
            message = f'Jenkins上的流水线共有[{len(results)}]个，这里是我找到的所有流水线:'
            dispatcher.utter_message(text=message)
            for i in results:
                dispatcher.utter_message(text=i)
            return []
