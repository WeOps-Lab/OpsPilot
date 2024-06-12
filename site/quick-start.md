# 快速入门

## 部署K3S

```
curl https://releases.rancher.com/install-docker/20.10.sh | sh
curl -sfL https://get.k3s.io | sh -s - --docker
```

## 部署基础组件

进入 `support-files/k8s`目录，执行

```
kubectl create ns argo
kubectl create ns ops-pilot

kubectl apply -f argy.yml
kubectl apply -f elasticsearch.yml
kubectl apply -f minio.yml
kubectl apply -f postgres.yml
kubectl apply -f rabbitmq.yml
```

## 部署Munchkin

```
kubectl apply -f munchkin.yml
```

## 初始化Munchkin

首次打开Munchkin，需要先初始化超级管理员的用户名和密码

```
DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@example.com DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --noinput
```

然后在界面上初始化token

![token.png](https://static.cwoa.net/8d7fff2f7b5b463c99dc3b719afb4fc8.png)
