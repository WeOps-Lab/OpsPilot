# 企业微信

## 企业微信应用

要开启OpsPilot企业应用集成，需要在`creadentials.yml`中配置企业微信应用的相关信息。

```yaml
channels.enterprise_wechat.enterprise_wechat_channel.EnterpriseWechatChannel:
  corp_id: ""
  secret: ""
  token: ""
  aes_key: ""
  agent_id: ""
```

在企业微信中找到上述配置，填入即可

## 企业微信Jenkins构建分析机器人

```yaml
channels.jenkins_notifycation.enterprise_wechat_jenkins_notification.EnterpriseWeChatJenkinsNotification:
  fastgpt_url:
  fastgpt_token:
  enterprise_bot_url:
  secret_token:
```
