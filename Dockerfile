FROM python:3.12
WORKDIR /apps

RUN pip install pip-tools
ADD ./requirements.in ./requirements.in
RUN pip-compile
RUN pip-sync

ADD ./actions ./actions
ADD ./cache ./cache
ADD ./channels ./channels
ADD ./compoments ./compoments
ADD ./models ./models
ADD ./credentials.yml ./credentials.yml
ADD ./endpoints.yml ./endpoints.yml

ADD ./ops_pilot_cli.py ./ops_pilot_cli.py