# 架构概览

## 基础模块

在OpsPilot里面，有以下关键模块：

* **机器人**：每个机器人就是一个Pilot。Pilot被K8S调度，通过通道与用户接触
* **AI模型**：AI模型为Pilot提供了技能，可以简单的认为扩展包告诉了Pilot能做哪些动作，AI模型为动作提供了魔法😁。AI模型也可以直接对外提供服务
* **通道**：通道是Pilot与用户连接的渠道，包括钉钉、Web、企业微信，也可以是Gitlab
* **知识库**：知识库为机器人提供了RAG的支撑，使得机器人可以回复私域知识



## 系统架构

OpsPilot由基础设施、AI Service以及业务层组成

![arch.png](https://static.cwoa.net/8791238859a94764a2e2c9c8e554045d.png)
