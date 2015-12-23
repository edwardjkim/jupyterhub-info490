# JupyterHub deployment for INFO 490

This repository contains an Ansible playbook for launching JupyterHub for the
Intro to Data Science class at the University of Illinois.

## Install Python modules

On Scientific Linux,

```bash
$ sudo yum install python python-devel python-pip
$ sudo pip install paramiko PyYAML Jinja2 httplib2 six
```

## Install Ansible

```bash
$ git clone git://github.com/ansible/ansible.git --recursive
$ cd ./ansible
$ source ./hacking/env-setup
```
