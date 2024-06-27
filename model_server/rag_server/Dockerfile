FROM ccr.ccs.tencentyun.com/megalab/pilot-base
WORKDIR /app

ADD ./requirements.in ./requirements.in
RUN pip install -r requirements.in

ADD ./conf/service.conf /etc/supervisor/conf.d/service.conf
ADD ./embedding ./embedding

ADD ./runnable ./runnable
ADD ./user_types ./user_types
ADD ./server.py ./server.py

CMD ["supervisord", "-n"]
