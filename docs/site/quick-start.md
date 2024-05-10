# 快速入门

使用以下Docker-Compose可以快速的部署OpsPilot,

```
cd ./support-files/docker-compose/
cp ./.env.example ./.env
docker-compose up -d
```

执行`docker-compose up -d`，访问5005端口，正常的话，服务就启动完毕了。

> 注意：投入正式环境使用的时候，需要将Model以及配置文件更换为自己的。