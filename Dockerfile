FROM python:3.10
WORKDIR /apps

ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

ADD ./actions ./actions
ADD ./cache ./cache
ADD ./channels ./channels
ADD ./compoments ./compoments
ADD ./models ./models
ADD ./credentials.yml ./credentials.yml
ADD ./endpoints.yml ./endpoints.yml

ADD ./ops_pilot_cli.py ./ops_pilot_cli.py