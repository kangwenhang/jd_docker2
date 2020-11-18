# Version 1.1.5

FROM python:3.8.3-alpine
MAINTAINER 星辰

RUN wget -O /tmp/BiliExp.tar.gz https://github.com/happy888888/BiliExp/archive/1.1.5.tar.gz \
 && mkdir /BiliExp \
 && tar -zxvf /tmp/BiliExp.tar.gz -C /tmp/ \
 && mv /tmp/BiliExp-* /tmp/BiliExp \
 && mv /tmp/BiliExp/BiliClient /tmp/BiliExp/config /tmp/BiliExp/tasks /tmp/BiliExp/BiliExp.py /tmp/BiliExp/requirements.txt /BiliExp/ \
 && rm -rf /tmp/BiliExp*

RUN apk add --no-cache build-base libffi-dev \
 && pip --no-cache-dir install -r /BiliExp/requirements.txt \
 && pip --no-cache-dir install requests \
 && apk del libffi-dev build-base
 
ENTRYPOINT ["python3", "/BiliExp/BiliExp.py"]
CMD ["-c", "/etc/BiliExp/config.json", "-l", "/etc/BiliExp/BiliExp.log"]