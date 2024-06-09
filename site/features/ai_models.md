# AI模型

在AI模型功能块，可以对OpsPilot能够使用的AI技能进行管理，包括配置AI能力的通道配置，技能配置

## Embed模型

Embed模型为知识提供向量化的能力，是知识库能够进行语义检索的支撑功能。OpsPilot内置以下Embed模型的支持

* [FastEmbed](https://qdrant.github.io/fastembed/)
  * bge-small-zh-v1.5
  * bge-small-en-v1.5
* [BCEmbedding](https://github.com/netease-youdao/BCEmbedding)
  * bec-embedding-base_v1
* OpenAI
  * text-embedding-ada-002
    ## LLM模型

## API

### 文本向量化

> POST /api/embed/embed_content/

```
{
  "embed_model_id": 1,
  "content": "介绍一下你的团队"
}
```

### 内容重排序

> POST /api/rerank/rerank_sentences/

```
{
  "rerank_id": 1,
  "query": "介绍一下Rasa",
  "top_k": 2,
  "sentences": [
    "今天天气真好",
    "Rasa是什么",
    "Django和Rasa怎么结合起来用"
  ]
}
```
