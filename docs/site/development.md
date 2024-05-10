# 本地开发


## 前置依赖

```
pip install pip-tools
```

## 准备虚拟环境

```
virtualenv .venv -p python3.10
```

## 安装依赖

```
make venv-install
```

## 训练模型
```
make train 
```

## 启动服务
```
make run 
make actions
make celery
```