# RasaOps

RasaOps是一个基于Rasa和ChatGPT的机器人，基于Rasa 提供NLU的能力，当无法识别的情况下，会转交给ChatGPT进行问答

## 支持的能力

* 知识问答能力: 支持基于语意的知识问答
* 知识库检索能力：支持从Neo4J，本地知识库
* 重启服务器
* Jenkins流水线构建，支持失败的时候使用LLM进行异常分析
* 与LLM进行整合，当无法识别用户具体意图或者完成指定任务的时候，支持调用LLM能力：
  * ChatGPT