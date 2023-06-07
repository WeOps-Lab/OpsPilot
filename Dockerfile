FROM python:3.10
WORKDIR /apps

ADD ./requirements.txt ./requirements.txt
RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple -r ./requirements.txt

ADD ./actions ./actions
ADD ./cache ./cache
ADD ./channels ./channels
ADD ./compoments ./compoments
ADD ./endpoints.yml ./endpoints.yml
ADD ./models ./models

ADD ./credentials.yml ./credentials.yml
