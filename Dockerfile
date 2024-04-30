FROM python:3.10
WORKDIR /apps

RUN pip install pip-tools
ADD ./requirements.in ./requirements.in
RUN pip-compile -v
RUN pip-sync

ADD ./actions ./actions
ADD ./cache ./cache
ADD ./channels ./channels
ADD ./compoments ./compoments
ADD ./models ./models
ADD ./credentials.yml ./credentials.yml
ADD ./endpoints.yml ./endpoints.yml
ADD ./libs ./libs

ADD ./ops_pilot_cli.py ./ops_pilot_cli.py


WORKDIR /apps