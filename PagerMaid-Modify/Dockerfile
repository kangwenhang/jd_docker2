FROM ubuntu:20.10
RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
&& sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
&& apt-get update && apt-get upgrade \
&& apt-get install -y git \
    openssl \
    bzip2 \
    sqlite \
    fortune-mod \
    figlet \
    python3-virtualenv \
    redis \
    libxml2 \
    curl \
    wget \
    neofetch \
    sudo \
    gcc \
    imagemagick \
    ffmpeg \
    file \
    python3-pip \
&& sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers \
&& mkdir -p /pagermaid/workdir \
&& git clone -b master https://github.com/xtaodada/PagerMaid-Modify.git /pagermaid/workdir \
&& cd /pagermaid/workdir \
&& python3 -m virtualenv venv \
&& source venv/bin/activate; pip3 install -r requirements.txt
WORKDIR /pagermaid/workdir
CMD ["sh","utils/docker-run.sh"]
