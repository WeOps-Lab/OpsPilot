import inspect
import json
from typing import Text, Callable, Awaitable

import requests
from loguru import logger
from rasa.core.channels import InputChannel, UserMessage
from sanic import Blueprint, Request, HTTPResponse, response

from eventbus.base_eventbus import BaseEventBus
from utils.munchkin_driver import MunchkinDriver
from utils.rasa_utils import RasaUtils


class AutomationChannel(InputChannel):
    def name(self) -> Text:
        return "automation_channel"

    def recieve_event(self, event):
        if self.event_bus.is_automation_event(event):
            logger.info(f"接收到自动化事件:{event}")

            if event['automation_event'] == 'list_jenkins_jobs':
                RasaUtils.call_external_utter(event['sender_id'], table_str, event['channel'])

    def __init__(self, ) -> None:
        super().__init__()
        self.event_bus = BaseEventBus()
        self.event_bus.consume('automation_channel', self.recieve_event)
        logger.info('自动化消息通道已启动')

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
