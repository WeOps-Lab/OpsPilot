# 快速入门

## 部署K3S

```
curl https://releases.rancher.com/install-docker/20.10.sh | sh
curl -sfL https://get.k3s.io | sh -s - --docker
```

## 获取Pilot镜像

```
docker pull ccr.ccs.tencentyun.com/megalab/pilot
```

## 创建命名空间

```
kubectl create ns ops-pilot
```

## 部署基础组件

进入 `installer/depend`目录，执行

```
kubectl apply -f elasticsearch.yml
kubectl apply -f minio.yml
kubectl apply -f postgres.yml
kubectl apply -f rabbitmq.yml
```

## 部署服务组件

进入 `installer/ai-service`目录，执行

```
kubectl apply -f bce-embed-server.yml
kubectl apply -f bce-rerank-server.yml
kubectl apply -f chat-server.yml
kubectl apply -f chunk-server.yml
kubectl apply -f fast-embed-server-zh.yml
kubectl apply -f pandoc-server.yml
kubectl apply -f rag-server.yml
kubectl apply -f 
```

## 可选组件

```
kubectl apply -f ./saltstack-server.yml
```

## 部署Munchkin

进入 `installer/munchkin`目录，执行

```
kubectl apply -f ./configmap.yml
kubectl apply -f ./svc.yml
kubectl apply -f ./ingress.yml  #修改YOUR_HOST配置
kubectl apply -f ./munchkin-sa.yml 
kubectl apply -f ./munchkin.yml 
```
