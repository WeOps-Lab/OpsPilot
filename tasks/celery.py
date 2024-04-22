import json

import requests
import yaml
from celery import Celery
from loguru import logger
from wechatpy.enterprise import WeChatClient

from actions.constants.server_settings import server_settings
from actions.services.kscan_service import KScanService

app = Celery('celery', broker=server_settings.celery_broker_url)

with open(server_settings.rasa_credentials, 'r') as f:
    credentials = yaml.safe_load(f)
logger.info(f'成功加载配置:[{server_settings.rasa_credentials}]')


@app.task
def scan_target(channel, conversation_id, scan_targets, **kwargs):
    """
    资产测绘任务
    :param channel:
    :param conversation_id:
    :param scan_targets:
    :param kwargs:
    :return:
    """
    logger.info(f'开始扫描:[{scan_targets}],会话ID:[{conversation_id}],通道:[{channel}],附加参数:[{kwargs}]')
    service = KScanService()
    scan_result = '资产测绘结果: \n' + service.scan(scan_targets)

    if channel == 'enterprise_wechat':
        logger.info(f'发送企业微信消息回调:[{conversation_id}]')
        conf = credentials['channels.enterprise_wechat.enterprise_wechat_channel.EnterpriseWechatChannel']
        wechat_client = WeChatClient(
            conf['corp_id'],
            conf['secret'],
        )
        wechat_client.message.send_text(conf['agent_id'], conversation_id, scan_result)

        # 记录Rasa对话记录
        url = f"{server_settings.rasa_action_server_url}/conversations/{conversation_id}/tracker/events"
        headers = {"Content-Type": "application/json"}
        data = {"event": "bot", "text": scan_result}
        requests.post(url, headers=headers, data=json.dumps(data))
        logger.info(f'[{conversation_id}]事件记录已经记录到对话引擎')
    else:
        url = f"{server_settings.rasa_action_server_url}/conversations/{conversation_id}/trigger_intent?output_channel=latest"
        headers = {"Content-Type": "application/json"}
        data = {"name": "EXTERNAL_UTTER", "entities": {"content": scan_result}}
        requests.post(url, headers=headers, data=json.dumps(data))
        logger.info(f'[{conversation_id}]扫描结果已发送至对话引擎')
