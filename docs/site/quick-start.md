# 快速入门

使用以下Docker-Compose可以快速的部署OpsPilot,

```
cd ./support-files/docker-compose/
cp ./.env.example ./.env
docker-compose up -d
```

执行`docker-compose up -d`，访问5005端口，正常的话，服务就启动完毕了。

> 注意：投入正式环境使用的时候，需要将Model以及配置文件更换为自己的。

## 环境变量

| 变量名                         | 说明                               | 默认值                    |
|-----------------------------|----------------------------------|------------------------|
| RUN_MODE                    | 运行模式                             | dev                    |
| CHATGPT_MODEL_MAX_HISTORY   | 对话历史记录最大长度（用于对话总结技能）             | 5                      |
| ENABLE_LLM_SOURCE_DETAIL    | LLM回复的时候，是否回复知识来源                | false                  |
| CELERY_BROKER_URL           | Celery Broker地址,用于长周期任务技能        |                        |
| RASA_CREDENTIALS            | Rasa认证配置文件名称，Celery任务会使用         | credentials.yml        |
| RASA_ACTION_SERVER_URL      | Rasa Action Server地址，Celery任务会使用 | http://localhost:5055/ |
| FASTGPT_ENDPOINT            | FastGPT服务地址                      |                        |
| FASTGPT_KEY                 | FastGPT服务的Key，用于LLM回复技能          |                        |
| FASTGPT_CONTENT_SUMMARY_KEY | FastGPT服务的Key，用于对话总结技能           |                        |
| FASTGPT_TICKET_KEY          | FastGPT服务的Key，用于智能提单技能           |                        |
| ENABLE_JENKINS_SKILL        | 是否启用Jenkins技能                    | false                  |
| JENKINS_URL                 | Jenkins服务地址                      |                        |
| JENKINS_USERNAME            | Jenkins用户名                       |                        |
| JENKINS_PASSWORD            | Jenkins密码                        |                        |
| CELERY_BROKER_URL           | Celery Broker地址                  |                        |
| CELERY_RESULT_BACKEND       | Celery Result Backend地址          |                        |
| RASA_CREDENTIALS            | Rasa认证配置文件名称，Celery任务会使用         | credentials.yml        |
| SUPABASE_URL                | Supabase地址,用于模型训练                |                        |
| SUPABASE_KEY                | Supabase Key                     |                        |
| SUPABASE_USERNAME           | Supabase用户名                      |                        |
| SUPABASE_PASSWORD           | Supabase密码                       |                        |