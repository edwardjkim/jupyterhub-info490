#!/bin/bash

: ${HADOOP_PREFIX:=/usr/local/hadoop}

$HADOOP_PREFIX/etc/hadoop/hadoop-env.sh

rm /tmp/*.pid

# installing libraries if any - (resource urls added comma separated to the ACP system variable)
cd $HADOOP_PREFIX/share/hadoop/common ; for cp in ${ACP//,/ }; do  echo == $cp; curl -LO $cp ; done; cd -

# altering the core-site configuration
sed s/HOSTNAME/$HOSTNAME/ /usr/local/hadoop/etc/hadoop/core-site.xml.template > /usr/local/hadoop/etc/hadoop/core-site.xml
sed s/HOSTNAME/$HOSTNAME/ /usr/local/hadoop/etc/hadoop/mapred-site.xml.template > /usr/local/hadoop/etc/hadoop/mapred-site.xml

# need this workaround to regenerate ssh keys because we will mount home directory and overwrite ~/.ssh
mkdir /home/$NB_USER/.ssh
echo -e "Host *\nUserKnownHostsFile /dev/null\nStrictHostKeyChecking no\nLogLevel quiet\nPort 2122" > /home/$NB_USER/.ssh/config
ssh-keygen -q -N '' -t rsa -f /home/$NB_USER/.ssh/id_rsa
cat /home/$NB_USER/.ssh/id_rsa.pub >> /home/$NB_USER/.ssh/authorized_keys

service ssh start

$HADOOP_PREFIX/sbin/start-dfs.sh
$HADOOP_PREFIX/sbin/start-yarn.sh

# Pig relies on job history server
$HADOOP_PREFIX/sbin/mr-jobhistory-daemon.sh start historyserver

jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user=$JPY_USER \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL
