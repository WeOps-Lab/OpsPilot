FROM ccr.ccs.tencentyun.com/megalab/pilot-base
WORKDIR /app

ADD ./models ./models

ADD ./conf/service.conf /etc/supervisor/conf.d/service.conf
ADD ./requirements.in ./requirements.in

RUN pip-compile -v
RUN pip-sync -v

ADD ./server.py ./server.py

RUN apt-get reinstall supervisor -y
CMD ["supervisord", "-n"]
