import json

from utils.eventbus import EventBus, NOTIFICATION_EVENT


class NotificationEventBus(EventBus):
    def publist_notification_event(self, content, sender_id):
        # 发送通道通知消息总线
        data = {
            "event_type": NOTIFICATION_EVENT,
            "notification_content": content,
            "sender_id": sender_id
        }
        self.publish(json.dumps(data))

    def get_notification_event_sender_id(self, event):
        return event['sender_id']

    def get_notification_event_content(self, event):
        return event['notification_content']

    def is_notification_event(self, event):
        return event['event_type'] == NOTIFICATION_EVENT
