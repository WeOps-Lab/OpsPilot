FROM node:22
ENV LANG C.UTF-8
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y libcairo2-dev libjpeg-dev libpango1.0-dev libgif-dev build-essential g++ ttf-wqy-microhei
RUN ln /etc/fonts/conf.d/65-wqy-microhei.conf /etc/fonts/conf.d/69-language-selector-zh-cn.conf

WORKDIR /apps/app
ADD package.json ./package.json
ADD ./app ./app
ADD ./config ./config
ADD ./app.js ./app.js
ADD ./opentelemetry.js ./opentelemetry.js
ADD ./docker-entrypoint.sh ./docker-entrypoint.sh

ENV OTLP_URL http://127.0.0.1:4318/v1/traces
ENV SERVICE_NAME bionics
ENV ENABLE_OTEL false

RUN chmod 0755  ./docker-entrypoint.sh

RUN yarn install
ENTRYPOINT ["/apps/app/docker-entrypoint.sh"]
