FROM python:3.6.13-alpine
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=zh_CN.UTF-8 \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " 
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade \
    && apk --no-cache add -f git \
    openssl \
    bzip2 \
    sqlite \
    fortune-mod \
    figlet \
    python3.8 \
    redis \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libevent-dev \
    libffi-dev \
    curl \
    wget \
    neofetch \
    sudo \
    gcc \
    imagemagick \
    ffmpeg \
    file \
    python3-pip \
&& pip3 install virtualenv \
&& sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers \
&& mkdir -p /pagermaid/workdir \
&& git clone -b master https://github.com/xtaodada/PagerMaid-Modify.git /pagermaid/workdir \
&& cd /pagermaid/workdir \
&& python3 -m virtualenv venv \
&& source venv/bin/activate; pip3 install -r requirements.txt
WORKDIR /pagermaid/workdir
CMD ["sh","utils/docker-run.sh"]
