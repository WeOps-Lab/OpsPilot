from eventbus.base_eventbus import BaseEventBus
import json

AUTOMATION_EVENT = "automation_event"


class AutomationEventbus(BaseEventBus):
    def is_automation_event(self, event):
        return event['event_type'] == AUTOMATION_EVENT

    def publish_automation_event(self, skill_id, sender_id, channel, params={}):
        event = {
            "event_type": AUTOMATION_EVENT,
            "skill_id": skill_id,
            "sender_id": sender_id,
            "channel": channel,
            "params": params
        }
        self.publish(json.dumps(event))
