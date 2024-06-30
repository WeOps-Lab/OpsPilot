FROM ccr.ccs.tencentyun.com/megalab/pilot-base
WORKDIR /app
RUN pip3 install "fschat[model_worker,webui]"

ADD ./conf/controller.conf /etc/supervisor/conf.d/controller.conf
ADD ./conf/api.conf /etc/supervisor/conf.d/api.conf
ADD ./conf/worker.conf /etc/supervisor/conf.d/worker.conf

CMD ["supervisord", "-n"]