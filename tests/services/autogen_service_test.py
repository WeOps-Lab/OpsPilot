import logging

from actions.services.autogen_service import AutogenService


def test_chat():
    service = AutogenService()
    results = service.chat('这是一个什么网站: https://www.oschina.net/')
    logging.info(results)
