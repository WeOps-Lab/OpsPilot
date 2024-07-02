# 使用官方的Ubuntu作为基础镜像
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive

# 安装需要的包
RUN apt-get update && \
    apt-get install -y  supervisor net-tools curl vim jq binutils build-essential patchelf  unzip curl pkg-config iputils-ping wget &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 添加Salt Stack的源
RUN curl -fsSL -o /etc/apt/keyrings/salt-archive-keyring-2023.gpg https://repo.saltproject.io/salt/py3/ubuntu/22.04/amd64/SALT-PROJECT-GPG-PUBKEY-2023.gpg 
RUN echo "deb [signed-by=/etc/apt/keyrings/salt-archive-keyring-2023.gpg arch=amd64] https://repo.saltproject.io/salt/py3/ubuntu/22.04/amd64/latest jammy main" | tee /etc/apt/sources.list.d/salt.list 

# 安装Salt Stack
RUN apt-get update && apt-get install -y \
    salt-master salt-minion salt-ssh salt-syndic salt-cloud salt-api \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 创建必要的文件夹
RUN mkdir -p /srv/salt

RUN /opt/saltstack/salt/bin/pip install psycopg2-binary sqlalchemy records


RUN wget -c "https://github.com/lcvvvv/kscan/releases/download/v1.85/kscan_linux_amd64.zip" &&\
    unzip kscan_linux_amd64.zip &&\
    mv kscan_linux_amd64 /usr/bin/kscan &&\
    chmod +x /usr/bin/kscan &&\
    rm -rf kscan_linux_amd64.zip
    
# 将当前目录的内容复制到容器的/app目录
ADD ./config/salt/master /etc/salt/master
ADD ./config/salt/minion /etc/salt/minion
ADD ./config/supervisor/salt-master.conf /etc/supervisor/conf.d/salt-master.conf
ADD ./config/supervisor/salt-api.conf /etc/supervisor/conf.d/salt-api.conf
ADD ./config/supervisor/salt-minion.conf /etc/supervisor/conf.d/salt-minion.conf


# 设置挂载点
VOLUME ["/etc/salt","/var/log/salt","/var/cache/salt","/srv/salt","/srv/pillar"]

# 设置开放端口
EXPOSE 4505 4506

# 创建新用户
RUN useradd -M -s /sbin/nologin saltapi
RUN echo "saltapi:Changeme" | chpasswd

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

WORKDIR /
# 定义容器启动命令
CMD [ "supervisord","-n" ]