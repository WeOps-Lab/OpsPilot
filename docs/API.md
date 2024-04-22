# 主动触发intent

```
curl -H "Content-Type: application/json" -X POST \
    -d '{"name": "intent名称", "entities": {"content": "Orchid"}}' \
    "http://localhost:5005/conversations/602449064/trigger_intent?output_channel=latest"
```