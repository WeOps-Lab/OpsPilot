# OpsPilot

<img src="https://wedoc.canway.net/imgs/img/嘉为蓝鲸.jpg" >


OpsPilot是一个基于Rasa和LLM技术的ChatBot，为运维系统提供ChatOps/LMOps的能力

<img src="./docs/images/chatbot.png" >


## 使用场景

### Jenkins

* 列出Jenkins上的流水线
* 构建指定流水线
* 查找包含指定名称的流水线

> 场景化模型处于闭源状态，需要的小伙伴可以通过添加“小嘉”微信，加入官方沟通群，获取专业的场景化模型哦
>
<img src="./docs/images/canway.jpeg" width="30%" height="30%">

### 部署

```
export AZURE_OPENAI_MODEL_NAME=
export AZURE_OPENAI_ENDPOINT=
export AZURE_OPENAI_KEY=
cd ./support-files/
docker-compose up -d
```

### 开发环境搭建
Python:3.10
```
pip install -r ./requirements.txt
pip install -r ./requirements-test.txt
```

常用指令参考Makefile

### 常见问题

#### 如何启用WebSocket的JWT验证

修改`credentials.yml`,添加`jwt_key`、`jwt_method`配置即可

```
socketio:
  user_message_evt: user_uttered
  bot_message_evt: bot_uttered
  session_persistence: true
  jwt_key: key
  jwt_method: HS256
```

### Mac如何安装requirements.txt

```
export HNSWLIB_NO_NATIVE=1  
pip install -r requirements.txt
```

### 参数说明

| 参数                 | 说明                             | 可选配置   |
|--------------------|--------------------------------|--------|
| FALLBACK_LLM       | 当OpsPilot无法处理的时候，使用LLM进行回复     | OPENAI |
| FALLBACK_PROMPT    | 默认回复的PROMT                     |        |                          |
| OPENAI_ENDPOINT    | OpenAI上部署模型的终结点                |        |
| OPENAI_KEY         | OpenAI上部署模型使用的秘钥               |        |
| JENKINS_URL        | Jenkins URL,启用Jenkins自动化能力需要配置 |        |
| JENKINS_USERNAME   | Jenkins 用户名,启用Jenkins自动化能力需要配置 |        |
| JENKINS_PASSWORD   | Jenkins 密码,启用Jenkins自动化能力需要配置  |        |
| BING_SEARCH_URL    | Bing Search端点                  |        |
| BIND_SEARCH_KEY    | Bing Search密码                  |        |
| VEC_DB_PATH        | 向量数据库的路径                       |        |
| RUN_MODE           | 是否以开发模式运行                      |        |
| FALLBACK_CHAT_MODE | LLM使用本地知识库模式还是闲聊模式             |        |

# 版本说明

## 0.1

* 完成基础框架搭建