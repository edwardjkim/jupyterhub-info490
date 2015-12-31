# JupyterHub deployment for INFO 490

This repository contains an Ansible playbook for launching JupyterHub for the
Intro to Data Science class at the University of Illinois.

## Installation

### Install Docker

```shell
$ sudo yum update
$ sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/$releasever/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
$ sudo yum install docker-engine
$ sudo service docker start
```

### Install Python modules

On Scientific Linux,

```shell
$ sudo yum install python python-devel python-pip
$ sudo pip install paramiko PyYAML Jinja2 httplib2 six
```

### Install Ansible

```shell
$ git clone git://github.com/ansible/ansible.git --recursive
$ cd ./ansible
$ source ./hacking/env-setup
```

If you log out of a session, you have to do `source ./hacking/env-setup` again
when you log back in, so you might want to add `source ./hacking/env-setup` to
`.bashrc`.

### Configuration variables

Use the example YAML files to change your server configurations.

```shell
$ cp inventory.example inventory
$ vim inventory
```

```shell
$ cp users.yml.example users.yml
$ vim users.yml
```

### Generate TLS/SSL certificates

You'll need to generate SSL/TLS certificates for the hub server and node servers.
To do this, you can use the keymaster docker container.
First, setup the certificates directory, password, and certificate authority:

```shell
$ mkdir certificates

$ touch certificates/password
$ chmod 600 certificates/password
$ cat /dev/random | head -c 128 | base64 > certificates/password

$ KEYMASTER="sudo docker run --rm -v $(pwd)/certificates/:/certificates/ cloudpipe/keymaster"
```

Then, to generate a keypair for a server:

```shell
${KEYMASTER} signed-keypair -n server1 -h server1.website.com -p both -s IP:192.168.0.1
```

You'll need to generate keypairs for the hub server and for each of the node servers.

## Deploy

```shell
$ ./script/deploy
```

This shell script asks for SSH passwords.
