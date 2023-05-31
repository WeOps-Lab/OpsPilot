FROM python:3.7.16
WORKDIR /apps
ADD ./actions ./actions
ADD ./cache ./cache
ADD ./compoments ./compoments
ADD ./models ./models
ADD ./requirements.txt ./requirements.txt
RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple -r ./requirements.txt