FROM python:3.10
WORKDIR /apps

RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple
RUN pip install pip-tools
ADD ./requirements.in ./requirements.in
RUN pip-compile -v
RUN pip-sync -v

ADD ./apps ./apps
ADD ./munckin ./munchkin
ADD ./Makefile ./Makefile
ADD ./manage.py ./manage.py
