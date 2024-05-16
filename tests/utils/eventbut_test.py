from utils.eventbus import EventBus


def test_send_notify():
    e = EventBus()
    e.publish('{"content": "OpsPilot消息总线通知", "type": "notification"}')
