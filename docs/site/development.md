# 本地开发

## 环境准备

> 开始之前，请参考[系统架构](architecture.md)章节完成基础环境的准备

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