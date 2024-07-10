FROM ccr.ccs.tencentyun.com/megalab/pilot-base
WORKDIR /apps

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y libomp-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD ./requirements.in ./requirements.in
RUN pip install -r requirements.in

ADD ./conf/service.conf /etc/supervisor/conf.d/service.conf

ADD ./conf ./conf
ADD ./libs ./libs
ADD ./runnable ./runnable
ADD ./user_types ./user_types
ADD ./server.py ./server.py

CMD ["supervisord", "-n"]
