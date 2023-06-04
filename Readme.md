# RasaOps

<img src="https://wedoc.canway.net/imgs/img/嘉为蓝鲸.jpg" >

RasaOps是一个基于Rasa和LLM技术的ChatBot，为运维系统提供ChatOps/LMOps的能力

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

# 版本说明


## V0.1
* **RasaOps框架初次搭建完成**
* 支持触发Jenkins流水线，在失败后支持使用LLM进行根因分析
* 支持Chitchat的能力，能够进行本地知识问答
* 支持使用本地知识库/Neo4J 进行服务器属性查询
* 支持执行重启服务器意图识别
* 支持Rasa Webchat对接
* 支持中文意图识别
* 支持调用Azure ChatGPT能力
* ........