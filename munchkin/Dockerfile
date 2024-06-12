FROM ccr.ccs.tencentyun.com/megalab/munchkin-base
WORKDIR /apps

RUN apt-get install -y pandoc
RUN apt-get install texlive-fonts-recommended texlive-latex-recommended -y
RUN apt-get install libgl1-mesa-glx ffmpeg libsm6 libxext6 -y

ADD ./requirements.in ./requirements.in
RUN pip-compile -v
RUN pip-sync -v

ADD ./apps ./apps
ADD ./k8s-templates ./k8s-templates
ADD ./templates ./templates
ADD ./munchkin ./munchkin
ADD ./Makefile ./Makefile
ADD ./manage.py ./manage.py

ADD ./support-files/supervisor/munchkin.conf /etc/supervisor/conf.d/munchkin.conf
ADD ./support-files/supervisor/celery.conf /etc/supervisor/conf.d/celery.conf
ADD ./support-files/supervisor/conversation.conf /etc/supervisor/conf.d/conversation.conf

RUN apt-get reinstall supervisor -y
