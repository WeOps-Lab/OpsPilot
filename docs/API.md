# 主动触发intent

```
curl -H "Content-Type: application/json" -X POST \
    -d '{"name": "intent名称", "entities": {"plant": "Orchid"}}' \
    "http://localhost:5005/conversations/用户ID/trigger_intent?output_channel=latest"
```