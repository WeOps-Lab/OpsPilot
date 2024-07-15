import inspect
from typing import Text, Callable, Awaitable

from loguru import logger
from rasa.core.channels import InputChannel, UserMessage
from sanic import Blueprint, Request, HTTPResponse, response

from eventbus.automation_eventbus import AutomationEventbus
from integrations.jenkins_integration import JenkinsIntegration
from utils.rasa_utils import RasaUtils


class AutomationChannel(InputChannel):
    def name(self) -> Text:
        return "automation_channel"

    def recieve_event(self, event):
        if self.event_bus.is_automation_event(event):
            logger.info(f"接收到自动化事件:{event}")

            if event['skill_id'] == 'list_jenkins_jobs':
                result = self.jenkins_integration.list_jenkins_job(event['sender_id'])
                RasaUtils.call_external_utter(event['sender_id'], result, event['channel'])
            elif event['skill_id'] == 'jenkins_build_log':
                result = self.jenkins_integration.get_build_log(event['params']['job_name'], event['sender_id'])
                RasaUtils.call_external_utter(event['sender_id'], result, event['channel'])
            elif event['skill_id'] == 'build_jenkins_pipeline':
                result = self.jenkins_integration.build_jenkins_job(event['params']['job_name'], event['sender_id'])
                RasaUtils.call_external_utter(event['sender_id'], result, event['channel'])

    def __init__(self, ) -> None:
        super().__init__()
        self.jenkins_integration = JenkinsIntegration()
        logger.info('自动化消息通道已启动')
        self.event_bus = AutomationEventbus()
        self.event_bus.consume('automation_channel', self.recieve_event)

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        hook = Blueprint(
            "automation_channel{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @hook.route("/", methods=["GET"])
        async def index(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        return hook