FROM ccr.ccs.tencentyun.com/megalab/pilot-base
WORKDIR /apps
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y pandoc texlive-latex-base texlive-fonts-recommended texlive-extra-utils texlive-latex-extra texlive-xetex &&\
    apt-get install -y texlive-lang-chinese librsvg2-bin texlive-fonts-extra &&\
    apt-get install -y ttf-wqy-zenhei xfonts-wqy fonts-wqy-zenhei &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD ./conf/service.conf /etc/supervisor/conf.d/service.conf
ADD ./requirements.in ./requirements.in

RUN pip install -r requirements.in

ADD ./latex ./latex
ADD ./server.py ./server.py

CMD ["supervisord", "-n"]
