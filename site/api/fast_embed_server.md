Fast Embed Server hosts the Fast Embed model and can generate embed relatively quickly on the CPU

## Embedding

### LangServer API

```python
remote = RemoteRunnable(f'{fast_embed_server}')
embed=remote.invoke("content")
```
