# fuzi bot api

[![Apache2 License](https://img.shields.io/badge/license-Apache2-orange.svg)](https://github.com/Ailln/fuzi-bot-api/blob/master/LICENSE)
[![stars](https://img.shields.io/github/stars/Ailln/fuzi-bot-api.svg)](https://github.com/Ailln/fuzi-bot-api/stargazers)
[![forks](https://img.shields.io/github/forks/Ailln/fuzi-bot-api.svg)](https://github.com/Ailln/fuzi-bot-api/network/members)

🤖️ 聊天机器人——`夫子`的「聊天接口」模块。

## 1 简介

`夫子` 聊天机器人有 8 个模块组成：
1. [fuzi-bot](https://github.com/Ailln/fuzi-bot): 聊天界面模块，与用户进行交互。
2. [fuzi-bot-api](https://github.com/Ailln/fuzi-bot-api): 聊天接口模块，与其他后端模块通信。
3. [fuzi-nlu](https://github.com/Ailln/fuzi-nlu): 自然语言处理模块，理解用户的问题。
4. [fuzi-search](https://github.com/Ailln/fuzi-search): 语义检索模块，快速查找已有问题。
5. fuzi: 对话管理模块，推断用户的意图。
6. fuzi-admin: 后台管理模块，管理机器人的设置。
7. fuzi-admin-api: 后台管理接口，与其他后端模块通信。
8. fuzi-mark: 数据标注模块，标注用户的问题。

![framework](.github/fuzi-framework.png)

## 2 快速上手

```shell
git clone https://github.com/Ailln/fuzi-bot-api.git

cd fuzi-bot-api
# 本地系统环境开发
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python -m server.main
# 服务运行在 http://localhost:8080

# 本地 docker 环境开发
docker run -it --name fuzi-bot-api -v $PWD:/app \
  -p 8080:8080 python:3.8.16-slim bash
cd /app
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python -m server.main
```

## 3 部署

### 3.1 Docker

```shell
cd fuzi-bot-api

docker build -t fuzi-bot-api:1.0.0 .
docker run -d --restart=always --name fuzi-bot-api \
  -p 8080:8080 fuzi-bot-api:1.0.0
```

### 3.2 Kubernetes

```shell
# 需要 docker registry
docker tag fuzi-bot-api:1.0.2 192.168.2.101:5000/fuzi-bot-api:1.0.0
docker push 192.168.2.101:5000/fuzi-bot-api:1.0.0

cd fuzi-bot-api
kubectl apply -f deploy/deployment.yaml
```

## 4 QPS Test

```shell
pip install locust -U

locust -f test/qps_test.py -H http://127.0.0.1:8080 -u 10 -r 2
# 打开 http://0.0.0.0:8089
```

## 5 To Do

- [ ] 聊天数据记录

## 6 许可证

[![](https://award.dovolopor.com?lt=License&rt=Apache2&rbc=orange)](./LICENSE)
[![](https://award.dovolopor.com?lt=Ailln's&rt=idea&lbc=lightgray&rbc=red&ltc=red)](https://github.com/Ailln/award)
