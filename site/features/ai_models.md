# AI模型

在AI模型功能块，可以对OpsPilot能够使用的AI技能进行管理，包括配置AI能力的通道配置，技能配置

## Embed模型

Embed模型为知识提供向量化的能力，是知识库能够进行语义检索的支撑功能，OpsPilot内置以下Embed模型，内置的这些模块可以在“知识管理-知识”中进行使用。

* [FastEmbed](https://qdrant.github.io/fastembed/)
  * bge-small-zh-v1.5
  * bge-small-en-v1.5
* [BCEmbedding](https://github.com/netease-youdao/BCEmbedding)
  * bec-embedding-base_v1
* OpenAI
  * text-embedding-ada-002

![模型1.png](https://static.cwoa.net/63fca4df4b93470d991944a39573e05a.png)

Embed模型支持新增/编辑和删除等操作，新增模型时需要选择类型（langserver类型是用于使用Embed模型进行语言处理任务的服务类型，可以通过不同的API（如HTTP的RESTful API、GRPC、WebSocket）与服务器进行交互，OpenAI类型是指OpenAI GPT模型的服务类型，通过OpenAI API可与OpenAI服务器进行交互，并使用GPT模型进行自然语言处理任务。）和配置信息（比如基本url）

![模型1-1.png](https://static.cwoa.net/8810c79527b643ef930251d41e57884b.png)

## ReRank模型

ReRank模型可以对检索出来的知识进行重排序，让大模型在使用RAG能力的时候，知识检索效果更好。

OpsPilot内置以下ReRank模型，内置的这些模块可以在“知识管理-知识”中进行使用。


* BCEReranker
  * bce-reranker-base_v1

![模型2.png](https://static.cwoa.net/1d101b079b8a4c13ad49ba55e0bade60.png)

ReRank模型支持新增/编辑和删除等操作，新增模型时需要选择类型（langserver类型是允许开发人员通过标准化API与服务器交互，以使用Rerank模型进行语言处理任务的服务）和配置信息（比如基本url）

![模型2-2.png](https://static.cwoa.net/b3a5b63566fe4dec8410543df7ebfb2a.png)

## LLM模型

LLM模型用于配置模型的基础配置，如凭据，方便后续的LLM技能所使用，OpsPilot内置以下LLM模型的支持：

* OpenAI
  * GPT-3.5-Turbo-16K
  * GPT-4-32K

![模型3.png](https://static.cwoa.net/fc7cd10259584a74a3478021e25d169a.png)

LLM模型支持新增/编辑和删除等操作，新增模型时需要选择类型（比如ChatGPT）和配置信息（比如model、OpenAI API所需的API密钥、与OpenAI API进行交互的服务器地址、生成文本时控制多样性的参数数值较低会使结果更保守和一致，而数值较高会使结果更多样化。）

![模型3-3.png](https://static.cwoa.net/3cfdffb027394a30a55c32717c856605.png)

## LLM技能

在OpsPilot里面，大模型对应的是LLM技能

> 为什么不是角色？因为在OpsPilot里面，Pilot才是真正的机器人，是OpsPilot的核心，LLM只是作为一个一个的技能，供Pilot执行动作的时候使用

LLM技能有如下可用的模板变量：

* input：用户输入的内容
* chat_history：聊天历史，在启用对话增强的使用会被自动填充

![模型4.png](https://static.cwoa.net/23bf0d66d9984cdcbcbfb7f60ba675df.png)

LLM技能创建完成后，可以被机器人所使用。

OpsPilot为每个Pilot的核心扩展包内置了以下技能：

* 开放知识问答：用于与用户进行开放型对话，让Pilot具备对话型机器人的能力。注意！技能ID必须为 `action_llm_fallback`,Pilot在不清楚应该执行什么任务的时候，会fallback到这个技能。该技能可调整如下参数
  * LLM模型：指定要使用的LLM模型版本，如"gpt-4-32k"。这决定了LLM技能使用的基础语言生成模型。
  * 技能提示词：为了更好地引导LLM技能生成相关的回复，可以提供技能提示词。这些提示词可以是一些关键词、短语或句子，有助于模型理解预期的回复内容。
  * 对话增强：对话增强功能用于处理对话历史和设置对话窗口大小。对话历史是指将过去的对话文本提供给模型，以便它能够更好地理解上下文。对话窗口大小指定了对话历史的文本数量或长度。
  * 知识库：启用RAG（Retrieve and Generate）知识库功能。RAG模型结合了信息检索和语言生成，以生成更具信息量和相关性的回复。配置知识库会涉及指定RAG模型以及相关参数，如显示RAG知识来源和RAG分数阈值（RAG分数阈值是设定的一个限制值，用于筛选出高于该阈值的知识片段，只有分数高于阈值的片段，才会被用于生成回复，以控制生成回复的质量和相关性。）。

![模型4-4.png](https://static.cwoa.net/710cea7cf66d4a4e88afcb06a951a475.png)


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
