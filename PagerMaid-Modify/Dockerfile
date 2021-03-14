FROM ubuntu:20.10
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=zh_CN.UTF-8 \
    LC_ALL=C \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " \
    DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]
COPY /PagerMaid-Modify/docker-run.sh /root
RUN source ~/.bashrc \
&& apt-get update \
&& apt-get install -y tzdata \
    git \
    python3 \
    python3-pip \
    imagemagick \
    libzbar-dev \
    fortune-mod \
    neofetch \
    tesseract-ocr \
    gdebi \
    ffmpeg \
    file \
    net-tools \
    iputils-ping \
    iproute2 \
    apt-utils \
    openssl \
    bzip2 \
    sqlite \
    figlet \
    redis \
    curl \
    wget \
    sudo \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libevent-dev \
    libffi-dev \
    gcc \
&& sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers \
&& mkdir -p /pagermaid/workdir \
&& git clone -b master https://github.com/xtaodada/PagerMaid-Modify.git /pagermaid/workdir \
&& mv -f /root/docker-run.sh /pagermaid/workdir/utils/docker-run.sh \
&& cd /pagermaid/workdir \
&& pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt \
&& apt-get clean \
&& apt-get autoclean \
&& rm -rf /var/lib/apt/lists/*
WORKDIR /pagermaid/workdir
CMD ["sh","utils/docker-run.sh"]
