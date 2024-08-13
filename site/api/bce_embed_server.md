The BCE Embed service provides both ReRank and Embed capabilities and is suitable for running on servers with gpu

## Embedding

```python
remote = RemoteRunnable(f'{embed_server}/embed')
embed=remote.invoke("content")
```

## ReRanking

```python
remote = RemoteRunnable(f'{embed_server}/rerank')
rerank_result=remote.invoke({
	"docs": [],
	"query": "",
	"top_n": 10
})
```
