# JupyterHub deployment for INFO 490

This repository contains an Ansible playbook for launching JupyterHub for the
Intro to Data Science class at the University of Illinois.

## Installation

### Install Python modules

On Scientific Linux,

```bash
$ sudo yum install python python-devel python-pip
$ sudo pip install paramiko PyYAML Jinja2 httplib2 six
```

### Install Ansible

```bash
$ git clone git://github.com/ansible/ansible.git --recursive
$ cd ./ansible
$ source ./hacking/env-setup
```

If you log out of a session, you have to do `source ./hacking/env-setup` again
when you log back in, so you might want to add `source ./hacking/env-setup` to
`.bashrc`.

### Configuration variables

Use the example YAML files to change your server configurations.

```bash
$ cp inventory.example inventory
$ vim inventory
```

```bash
$ cp users.yml.example users.yml
$ vim users.yml
```

## Deploy

```bash
$ ./script/deploy
```

This shell script asks for SSH passwords.
