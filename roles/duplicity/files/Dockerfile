FROM ubuntu:14.04

MAINTAINER Edward J Kim <edward.junhyung.kim@gmail.com>

RUN apt-get update && \
    apt-get upgrade --yes --force-yes && \
    apt-get install --yes --force-yes \
        wget \
        ncftp \
        lftp \
        python-dev \
        python-pip \
        librsync-dev \
        libffi-dev \
        libssl-dev \
    && \
    apt-get clean

RUN pip install pip --upgrade && \
    pip install \
        cryptography \
        paramiko \
        pycrypto \
        boto \
        setuptools \
        lockfile

RUN cd /root && \
    wget https://code.launchpad.net/duplicity/0.7-series/0.7.06/+download/duplicity-0.7.06.tar.gz && \
    tar xvzf duplicity-0.7.06.tar.gz && \
    cd duplicity-0.7.06 && \
    python setup.py install

ADD duplicity-cron /etc/cron.d/duplicity-cron
RUN chmod 0644 /etc/cron.d/duplicity-cron
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
