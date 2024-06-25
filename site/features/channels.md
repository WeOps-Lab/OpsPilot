# 通道管理

通道是Pilot与用户接触的管道，OpsPilot提供了多种方式让用户与Pilot之间能够交互

## 消息通道

OpsPilot内置了多种消息通道，让Pilot能够与用户进行交流，支持的消息通道包含：

* Web：可以通过嵌入WebChat组件，在网页中与Pilot进行交流
* 企业微信应用
* 企业微信群机器人
* 钉钉
* Gitlab

![通道1.png](https://static.cwoa.net/90df83025a1342d9953a5a8811469993.png)

消息通道的配置，需要选择类型填写配置参数（比如企业微信，需要填写AES密钥、企微应用的agentID、企微的企业ID、企微应用的Secret密钥和用于验证消息有效性的token）

![通道2.png](https://static.cwoa.net/9721c6a08fa74c69a9fb1df40bcbc99f.png)

消息通道创建完成后，可以被机器人所使用，成为和用户交互的门户。

## 用户组

用户组属于消息通道，用于区分与Pilot进行交流的用户，属于通道的哪个用户组，目前内置的5类消息通道各有一个默认用户组。

![用户1.png](https://static.cwoa.net/49254da719794b009f58c7e3f9c95f07.png)


## 用户

记录了与Pilot进行交流的用户，当用户与Pilot进行了交流后，会自动创建用户记录，在人工介入的环节，我们就可以与用户发起主动聊天

![用户2.png](https://static.cwoa.net/0b7c841120984bab915673be3a61463f.png)