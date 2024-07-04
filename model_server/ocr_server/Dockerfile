FROM ccr.ccs.tencentyun.com/megalab/pilot-base
WORKDIR /apps
ENV DEBIAN_FRONTEND=noninteractive


ADD ./conf/service.conf /etc/supervisor/conf.d/service.conf
ADD ./requirements.in ./requirements.in

RUN pip install -r requirements.in

ADD ./server.py ./server.py
ADD ./models ./models
CMD ["supervisord", "-n"]
