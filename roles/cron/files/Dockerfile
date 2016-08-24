FROM ubuntu:14.04
MAINTAINER Edward J Kim <edward.junhyung.kim@gmail.com>

ENV TZ America/Chicago

RUN apt-get update && \
    apt-get -y install \
        git \
        moreutils

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab

RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
