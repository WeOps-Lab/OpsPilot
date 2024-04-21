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

ADD ./ops_pilot_cli.py ./ops_pilot_cli.py

# Install kscan
WORKDIR /apps/libs/kscan
ADD https://github.com/lcvvvv/kscan/releases/download/v1.85/kscan_linux_amd64.zip .
RUN unzip kscan_linux_amd64.zip
RUN mv kscan_linux_amd64 kscan
RUN chmod +x kscan
RUN ./kscan --download-qqwry
RUN rm -Rf kscan_linux_amd64.zip

WORKDIR /apps