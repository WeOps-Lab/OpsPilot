# Quick Start

## Deploy K3S

```
curl https://releases.rancher.com/install-docker/20.10.sh | sh
curl -sfL https://get.k3s.io | sh -s - --docker
```

## Get Pilot image

```
docker pull ccr.ccs.tencentyun.com/megalab/pilot
```

## Create namespace

```
kubectl create ns ops-pilot
```

## Deploy basic components

Enter the `installer/depend` directory and execute

```
kubectl apply -f elasticsearch.yml
kubectl apply -f minio.yml
kubectl apply -f postgres.yml
kubectl apply -f rabbitmq.yml
kubectl apply -f pandoc-server.yml
kubectl apply -f bionics.yml
```

## Deploy service components

Enter the `installer/ai-service` directory and execute

```
kubectl apply -f bce-embed-server.yml
kubectl apply -f bce-rerank-server.yml
kubectl apply -f chat-server.yml
kubectl apply -f chunk-server.yml
kubectl apply -f fast-embed-server-zh.yml
kubectl apply -f rag-server.yml
kubectl apply -f classicfy-aiops-server.yml
```

## Optional components

```
kubectl apply -f ./saltstack-server.yml
```

## Deploy Munchkin

Enter the `installer/munchkin` directory and execute

```
kubectl apply -f ./configmap.yml
kubectl apply -f ./svc.yml
kubectl apply -f ./ingress.yml #Modify YOUR_HOST configuration
kubectl apply -f ./munchkin-sa.yml
kubectl apply -f ./munchkin.yml
```