import inspect
from typing import Text, Callable, Awaitable, Optional, Dict, Any

from loguru import logger
from rasa.core.channels import InputChannel, UserMessage
from sanic import Blueprint, Request, HTTPResponse, response

from eventbus.automation_eventbus import AutomationEventbus
from eventbus.notification_eventbus import NotificationEventBus
from integrations.jenkins_integration import JenkinsIntegration
from utils.rasa_utils import RasaUtils
import threading


class AutomationChannel(InputChannel):
    def name(self) -> Text:
        return "automation_channel"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get("secret_token"),
        )

    def handle_automation_event(self, event):
        logger.info(f"接收到自动化事件:{event}")
        if event['skill_id'] == 'list_jenkins_jobs':
            result = self.jenkins_integration.list_jenkins_job(event['sender_id'])
            RasaUtils.call_external_utter(event['sender_id'], result, event['channel'])
        elif event['skill_id'] == 'jenkins_build_log':
            result = self.jenkins_integration.get_build_log(event['params']['job_name'], event['sender_id'])
            RasaUtils.call_external_utter(event['sender_id'], result[-5000:], event['channel'])
        elif event['skill_id'] == 'build_jenkins_pipeline':
            result = self.jenkins_integration.build_jenkins_job(event['params']['job_name'], event['sender_id'])
            RasaUtils.call_external_utter(event['sender_id'], result[-30000:], event['channel'])

        elif event['skill_id'] == 'analyze_build_log':
            result = self.jenkins_integration.analyze_build_log(event['params']['job_name'], event['sender_id'])
            RasaUtils.call_external_utter(event['sender_id'], result, event['channel'])

    def process_event(self, event):
        # 接受到不属于本通道的消息
        if self.event_bus.is_automation_event(event) is False:
            return

        threading.Thread(target=self.handle_automation_event, args=(event,)).start()

    def __init__(self, secret_token) -> None:
        super().__init__()
        self.jenkins_integration = JenkinsIntegration()
        logger.info('自动化消息通道已启动')
        self.event_bus = AutomationEventbus()
        self.event_bus.consume('automation_channel', self.process_event)

        self.notification_eventbus = NotificationEventBus()
        self.secret_token = secret_token

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

        @hook.route("/jenkins/notification", methods=["POST"])
        async def jenkins_notification(request: Request) -> HTTPResponse:
            if request.args.get('secret_token') != self.secret_token:
                return response.json({"status": "error"}, status=401)
            body = request.json
            job_name = body.get("job_name")

            def execute(analyze_job_name):
                result = self.jenkins_integration.analyze_build_log(analyze_job_name, "")
                self.notification_eventbus.publist_notification_event(result, "",
                                                                      "enterprise_wechat_bot_channel")

            threading.Thread(target=execute, args=job_name).start()
            return response.json({"status": "ok"})

        return hook
