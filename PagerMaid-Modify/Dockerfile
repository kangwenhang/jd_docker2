FROM ubuntu:latest
RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
&& apt-get clean \
&& apt-get update \
&& apt-get install -y git \
    libffi \
    tesseract \
    openssl \
    bzip2 \
    zlib \
    readline \
    sqlite \
    fortune-mod \
    figlet \
    python3-virtualenv \
    redis \
    libxslt \
    libxml2 \
    libpqxx \
    linux-api-headers \
    freetype2 \
    jpeg-archive \
    curl \
    wget \
    neofetch \
    sudo \
    gcc \
    gcc8 \
    imagemagick \
    libwebp \
    zbar \
    ffmpeg \
    file \
    procps-ng \
&& sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers \
&& useradd pagermaid -r -m -d /pagermaid \
&& usermod -aG wheel,users pagermaid 
USER pagermaid
RUN mkdir /pagermaid/workdir \
&& git clone -b master https://github.com/xtaodada/PagerMaid-Modify.git /pagermaid/workdir \
&& cd /pagermaid/workdir \
&& python3 -m virtualenv venv \
&& source venv/bin/activate; pip3 install -r requirements.txt
WORKDIR /pagermaid/workdir
CMD ["sh","utils/docker-run.sh"]
