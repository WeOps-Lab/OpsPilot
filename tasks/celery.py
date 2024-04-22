import json

import requests
from celery import Celery
from loguru import logger

from actions.constants.server_settings import server_settings
from actions.services.kscan_service import KScanService

app = Celery('celery', broker=server_settings.celery_broker_url)


@app.task
def scan_target(conversation_id, scan_targets):
    logger.info(f'开始扫描:[{scan_targets}],会话ID:[{conversation_id}]')
    service = KScanService()
    scan_result = service.scan(scan_targets)
    url = f"http://localhost:5005/conversations/{conversation_id}/trigger_intent?output_channel=latest"
    headers = {"Content-Type": "application/json"}
    data = {"name": "EXTERNAL_UTTER", "entities": {"content": scan_result}}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    logger.info(response.text)
