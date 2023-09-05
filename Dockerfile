FROM python:3.10
WORKDIR /apps

ADD ./requirements.txt ./requirements.txt
RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple -r ./requirements.txt

ADD ./cache ./cache
ADD ./models ./models
ADD ./actions ./actions
ADD ./channels ./channels
ADD ./compoments ./compoments
ADD ./endpoints.yml ./endpoints.yml
ADD ./credentials.yml ./credentials.yml
