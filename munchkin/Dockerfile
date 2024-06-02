FROM ccr.ccs.tencentyun.com/megalab/pilot-base
WORKDIR /apps

ADD ./requirements.in ./requirements.in
RUN pip-compile -v
RUN pip-sync -v

ADD ./apps ./apps
ADD ./models ./models
ADD ./k8s-templates ./k8s-templates
ADD ./templates ./templates
ADD ./munchkin ./munchkin
ADD ./Makefile ./Makefile
ADD ./manage.py ./manage.py
ADD ./nltk_data /root/nltk_data