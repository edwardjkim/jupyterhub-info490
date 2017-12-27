FROM ubuntu:14.04
MAINTAINER Edward J Kim <edward.junhyung.kim@gmail.com>

ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get -y install \
        cron \
        git \
        moreutils \
        python

ADD crontab /etc/cron.d/jupyterhub-cron
RUN chmod 0644 /etc/cron.d/jupyterhub-cron

RUN touch /var/log/cron.log

ADD studentlist /tmp/studentlist

ADD release_to_students.sh /tmp/release_to_students.sh
RUN chmod +x /tmp/release_to_students.sh

ADD collect.sh /tmp/collect.sh
RUN chmod +x /tmp/collect.sh

CMD touch /etc/crontab /etc/cron.*/* && cron && tail -f /var/log/cron.log
