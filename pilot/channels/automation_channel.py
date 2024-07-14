import asyncio
import inspect
import json
import threading
from threading import Thread
from typing import Text, Optional, Dict, Any, Callable, Awaitable
import requests
from loguru import logger
from rasa.core.channels import InputChannel, CollectingOutputChannel, UserMessage
from sanic import Blueprint, Request, HTTPResponse, response

from utils.eventbus import EventBus
from utils.munchkin_driver import MunchkinDriver


class AutomationChannel(InputChannel):
    def name(self) -> Text:
        return "automation_channel"

    def recieve_event(self, event):
        if self.event_bus.is_automation_event(event):
            logger.info(f"接收到自动化事件:{event}")
            munchkin = MunchkinDriver()
            if event['automation_event'] == 'list_jenkins_jobs':
                result = munchkin.automation_skills_execute(
                    event['automation_event'],
                    "",
                    event['sender_id'])
                keys = result['return'][0].keys()
                first_key = list(keys)[0]
                color_map = {
                    'blue': '构建成功',
                    'yellow': '构建不稳定',
                    'red': '构建失败',
                    'notbuilt': '尚未构建',
                    'disabled': '被禁用',
                    'aborted': '构建被中止',
                    'blue_anime': '正在构建，上次成功',
                    'yellow_anime': '正在构建，上次不稳定',
                    'red_anime': '正在构建，上次失败'
                }
                jobs = json.loads(result['return'][0][first_key])['jobs']
                table_str = "| 名称 | 状态 |\n| --- | --- |\n"
                for job in jobs:
                    if 'color' not in job:
                        status = '未知'
                    else:
                        status = color_map.get(job['color'], '未知')
                    table_str += f"| {job['name']} | {status} |\n"
                utter_response = requests.post(
                    f'http://127.0.0.1:5005/conversations/{event["sender_id"]}/trigger_intent',
                    json={
                        "name": "EXTERNAL_UTTER",
                        "entities": {
                            "external_utter_content": f"{table_str}",
                            "external_utter_channel": f"{event['channel']}"
                        }
                    })
                utter_response.raise_for_status()

    def __init__(self, ) -> None:
        super().__init__()
        self.event_bus = EventBus()
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
