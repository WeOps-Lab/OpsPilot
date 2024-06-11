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

## ReRank模型

ReRank模型可以对检索出来的知识进行重排序，让大模型在使用RAG能力的时候，知识检索效果更好。OpsPilot内置以下ReRank模型的支持：

* BCEReranker
  * bce-reranker-base_v1

## LLM模型

LLM模型用于配置模型的基础配置，如凭据，方便后续的LLM技能所使用，OpsPilot内置以下LLM模型的支持：

* OpenAI
  * GPT-3.5-Turbo-16K
  * GPT-4-32K

## LLM技能

在OpsPilot里面，大模型对应的是LLM技能

> 为什么不是角色？因为在OpsPilot里面，Pilot才是真正的机器人，是OpsPilot的核心，LLM只是作为一个一个的技能，供Pilot执行动作的时候使用

LLM技能有如下可用的模板变量：

* input：用户输入的内容
* chat_history：聊天历史，在启用对话增强的使用会被自动填充

OpsPilot为每个Pilot的核心扩展包内置了以下技能：

* 开放知识问答：用于与用户进行开放型对话，让Pilot具备对话型机器人的能力。注意！技能ID必须为 `action_llm_fallback`,Pilot在不清楚应该执行什么任务的时候，会fallback到这个技能。

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

### 执行LLM技能

> POST /api/llm/execute/

```
{
  "llm_skill_id": 1,
  "user_message": "介绍一下你们团队的开发模式",
  "chat_history": [{"event":"user","text":"hello"},{"event":"bot","text":"hi"}],
  "super_system_prompt": ""
}
```
