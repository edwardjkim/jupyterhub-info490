FROM debian:8

MAINTAINER Edward J Kim <edward.junhyung.kim@gmail.com>

# Install packages required
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    duplicity \
    cron

ADD duplicity-cron /etc/cron.d/duplicity-cron
RUN chmod 0644 /etc/cron.d/duplicity-cron
RUN touch /var/log/cron.log

ENV TZ America/Chicago

CMD cron && tail -f /var/log/cron.log
