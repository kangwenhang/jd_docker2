FROM ubuntu:20.10
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=zh_CN.UTF-8 \
    LC_ALL=C \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " \
    DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]
RUN source ~/.bashrc \
&&  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
&& sed -i s@/ports.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
&& apt-get update \
&& apt-get install -y tzdata \
    git \
    python3.6 \
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
&& cd /pagermaid/workdir \
&& python3 -m virtualenv venv \
&& pip3 install virtualenv dateparser \
&& source venv/bin/activate; pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt \
&& apt-get autoremove -y libxml2-dev libxslt1-dev zlib1g-dev libevent-dev libffi-dev gcc \
&& apt-get clean 
WORKDIR /pagermaid/workdir
CMD ["sh","utils/docker-run.sh"]
