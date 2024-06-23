FROM ccr.ccs.tencentyun.com/megalab/pilot-base
WORKDIR /app

ADD ./models/nltk_data /root/nltk_data

ADD ./conf/service.conf /etc/supervisor/conf.d/service.conf

ADD ./requirements.in ./requirements.in

RUN pip install -r requirements.in

ADD ./embedding ./embedding
ADD ./loader ./loader
ADD ./utils ./utils
ADD ./server.py ./server.py

CMD ["supervisord", "-n"]
