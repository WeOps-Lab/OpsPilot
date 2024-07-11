FROM ccr.ccs.tencentyun.com/megalab/pilot-base
WORKDIR /apps

ADD ./requirements.in ./requirements.in
RUN pip install pip-tools
RUN pip-compile -v && pip-sync -v

ADD ./apps ./apps
ADD ./k8s-templates ./k8s-templates
ADD ./templates ./templates
ADD ./munchkin ./munchkin
ADD ./Makefile ./Makefile
ADD ./manage.py ./manage.py

ADD ./support-files/supervisor/munchkin.conf /etc/supervisor/conf.d/munchkin.conf
ADD ./support-files/supervisor/celery.conf /etc/supervisor/conf.d/celery.conf
ADD ./support-files/supervisor/conversation.conf /etc/supervisor/conf.d/conversation.conf

ADD ./support-files ./support-files
