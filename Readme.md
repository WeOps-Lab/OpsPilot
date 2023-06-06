# OpsPilot

<img src="https://wedoc.canway.net/imgs/img/嘉为蓝鲸.jpg" >

OpsPilot是一个基于Rasa和LLM技术的ChatBot，为运维系统提供ChatOps/LMOps的能力

<img src="./docs/images/chatbot.png" >

## 支持的能力

### 能力

* 知识问答能力: 支持基于语意的知识问答
* 知识库检索能力：支持从Neo4J，本地知识库
* 与LLM进行整合，支持使用ChatGPT进行问答
* 添加LangChain支持，能够让Chatbot进行联网检索
* 添加Scrapy支持，能够让Chatbot进行准确的联网信息搜集

### 场景

* 重启服务器
* 检索服务器的信息
* 查询服务器的属性
* Jenkins流水线构建，支持失败的时候使用LLM进行异常分析

### 参数说明

| 参数                      | 说明                             | 可选配置                     |
|-------------------------|--------------------------------|--------------------------|
| FALLBACK_LLM            | 当OpsPilot无法处理的时候，使用LLM进行回复     | AZURE_OPENAI(微软云ChatGPT) |
| FALLBACK_PROMPT         | 默认回复的PROMT                     |                          |                          |
| AZURE_OPENAI_MODEL_NAME | Azure OpenAI上部署的模型名称           |                          |
| AZURE_OPENAI_ENDPOINT   | Azure OpenAI上部署模型的终结点          |                          |
| AZURE_OPENAI_KEY        | Azure OpenAI上部署模型使用的秘钥         |                          |
| JENKINS_URL             | Jenkins URL,启用Jenkins自动化能力需要配置 |                          |
| JENKINS_USERNAME        | Jenkins 用户名,启用Jenkins自动化能力需要配置 |                          |
| JENKINS_PASSWORD        | Jenkins 密码,启用Jenkins自动化能力需要配置  |                          |
| BING_SEARCH_URL         | Bing Search端点                  |                          |
| BIND_SEARCH_KEY         | Bing Search密码                  |                          |
| RUN_MODE                | 是否以开发模式运行                      |                          |