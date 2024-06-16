# 架构概览

## 基础概念

在OpsPilot里面，有以下关键概念：

* 机器人：每个机器人就是一个Pilot，被K8S调度，扩展包告诉了Pilot能够做什么动作，AI模型赋予了动作魔法，而通道则是Pilot与用户交流的通道
* 扩展包：每个模型下可以有多个扩展包，每个扩展包是Rasa完整的训练语料
* 通道：通道是Pilot与用户连接的渠道，例如钉钉、Web、企业微信
* AI模型：AI模型为Pilot提供了技能，可以简单的认为扩展包告诉了Pilot能做哪些动作，AI模型为动作提供了魔法😁

## 系统架构

OpsPilot系统架构如下图所示，OpsPilot由Pilot和Munchkin两个关键组件组成，与用户进行连接的是Pilot

![Snipaste_2024-06-16_13-35-47.jpg](https://static.cwoa.net/e17908fe4af74502a18cc22fced23b21.jpg)
