FROM python:3.10
WORKDIR /apps

RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple
RUN pip install pip-tools
ADD ./requirements.in ./requirements.in
RUN pip-compile -v
RUN pip-sync -v

ADD ./actions ./actions
ADD ./cache ./cache
ADD ./channels ./channels
ADD ./compoments ./compoments
ADD ./models ./models
ADD ./configs/credentials.yml ./credentials.yml
ADD ./configs/endpoints.yml ./endpoints.yml
ADD ./libs ./libs
ADD ./utils ./utils

WORKDIR /apps