FROM ccr.ccs.tencentyun.com/megalab/pilot-base
WORKDIR /app

ADD ./conf/service.conf /etc/supervisor/conf.d/service.conf
ADD ./requirements.in ./requirements.in

RUN pip install -r requirements.in

ADD ./utils ./utils
ADD ./server.py ./server.py

CMD ["supervisord", "-n"]
