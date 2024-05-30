# EndPoint配置

EndPoint配置存放在`endpoint.yml`文件中

## Action Server配置

action_endpoint指向Rasa Action Server的地址，当触发Action的时候，NLU Server会调用Action Server的接口,单机部署的话，使用默认配置即可

```
action_endpoint:
  url: "http://127.0.0.1:5055/webhook"
```

## 远程模型加载配置

### Rasa远程模型加载

models.url指向Rasa模型的地址，wait_time_between_pulls指定了模型拉取的间隔时间，单位是秒。
假如远端服务没有返回`ETag`，请将`wait_time_between_pulls`设置为`null`，否则会导致模型不断被拉取，NLU Server不断重启的情况

```
models:
  url: 
  wait_time_between_pulls: null
```

## Tracker配置

Tracker记录了用户对话的状态以及历史记录

### SQLite Tracker

一般使用SQLite Tracker就够用了~

```yaml
tracker_store:
  type: SQL
  dialect: "sqlite"
  url: ""
  db: "tracker.db"
  username:
  password:
```

### Postgres Tracker配置

当需要多个NLU Server共享Tracker的时候，可以使用Postgres Tracker

```yaml
tracker_store:
  type: SQL
  dialect: "postgresql"
  url: "localhost"
  db: "postgres"
  username: "postgres"
  password: "password"
```

## Event Broker配置

Event Broker用于将用户的对话事件发送到指定的服务，一般用于做消息的记录

### Postgres Event Broker

```yaml
event_broker:
  type: SQL
  url: 127.0.0.1
  port: 5432
  dialect: postgresql
  username: postgresql
  password:
  db: ops-pilot
```

## Lock Store配置

在多个NLU Server共享Tracker的时候，需要使用Lock Store来保证Tracker的顺序正确，默认用的是`InMemoryLockStore`，不会保证多个NLU
Server的Tracker的顺序正确

### Redis Lock Store

```yaml
lock_store:
  type: "redis"
  url:
  port: 6379
  password:
  db: 1
  key_prefix: ops-pilot
```