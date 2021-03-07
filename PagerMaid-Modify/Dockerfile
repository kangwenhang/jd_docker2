FROM ubuntu:20.10
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=zh_CN.UTF-8 \
    LC_ALL=C \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " \
    DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]
RUN source ~/.bashrc \
    && apt-get update \
    && apt-get upgrade \
    && apt-get install -y tzdata \
    git \
    libzbar-dev \
    apt-utils \
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
