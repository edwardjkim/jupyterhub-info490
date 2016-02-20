# JupyterHub deployment for INFO 490

This repository contains an Ansible playbook for launching JupyterHub for the
Intro to Data Science class at the University of Illinois.

The setup is inspired by [the compmodels class](https://github.com/compmodels/jupyterhub-deploy)
but there are some major differences:

1.  Shibboleth authentication: Jupyterhub runs behind Shibboleth (via Apache).
2.  [Consul](https://www.consul.io/): Consul serves as the back-end discovery service
    for the Swarm cluster.
3.  Instead of creating creating users on the host system and using the
    [systemuser Docker image](https://github.com/jupyter/dockerspawner/tree/master/systemuser),
    we change the ownership of the files on the host system to the `jupyter` user and mount
    the appropriate directory onto the
    [singleuser Docker image](https://github.com/jupyter/dockerspawner/tree/master/singleuser).


## Overview

When a user accesses the server, the following happens behind the scenes:

1.  First, they go to the main url for the server.
2.  This url actually points to an Apache proxy server which authenticates the TSL connection,
    and proxies the connection to Shibboleth.
3.  After students are autheticated by Shibboleth, they are redirected to the JupyterHub instance
running on the hub server. 
4.  The hub server is both a NFS server (to serve user's home directories) and the JupyterHub server.
    JupyterHub runs in a docker container called `jupyterhub`.
5.  When they access their server, JupyterHub creates a new docker container on one of the node servers
    running an IPython notebook server.
    This docker container is called "jupyter-username", where "username" is the user's username.
6.  As users open IPython notebooks and run them, they are actually communicating
    with one of the node servers.
    The URL still appears the same, because the connection is first being proxied to the hub server
    via the proxy server, and then proxied a second time to the node server via the JupyterHub proxy.
7.  Users have access to their home directory, because each node server is also a NFS client
    with the filesystem mounted at /home.

## Installation

### Clone Git repository

```shell
$ git clone https://github.com/edwardjkim/jupyterhub-info490
$ cd jupyterhub-info490
```

### Install Docker

```shell
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates
$ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
$ sudo sh -c 'echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > /etc/apt/sources.list.d/docker.list'
$ sudo apt-get update
$ sudo apt-get install docker-engine
$ sudo service docker start
```

### Install Python modules

On Scientific Linux,

```shell
$ sudo apt-get install python python-dev python-pip
$ sudo pip install paramiko PyYAML Jinja2 httplib2 six
```

### Install Ansible

```shell
$ cd $HOME
$ git clone -b stable-2.0.0.1 git://github.com/ansible/ansible.git --recursive
$ cd ./ansible
$ source ./hacking/env-setup
```

If you log out of a session, you have to do `source ./hacking/env-setup` again
when you log back in, so you might want to add e.g.,
`cd ~/ansible && source ./hacking/env-setup -q && cd ~` to `.bashrc`.

### Configuration variables

This configuration script by default assumes you are using SSH password authentication,
so you need to set the password for the user, and set the following parameters in
`/etc/ssh/sshd_config`

```
ChallengeResponseAuthentication yes
PasswordAuthentication yes
PermitRootLogin yes
```

Use the example YAML files to change your server configurations.

```shell
$ cp inventory.example inventory
$ vim inventory
```

```shell
$ cp users.yml.example users.yml
$ vim users.yml
```

```shell
$ cp vars.yml.example vars.yml
$ vim vars.yml
```

### Generate TLS/SSL certificates

You will need to generate three sets of key and certificate for the web server,
Shibboleth, and Docker sockets.

### SSL certificates for Apache

Get signed SSL certificates from a certificate authority and edit `host_vars`.

```shell
$ cp host_vars/example host_vars/proxy_server
$ vim host_vars/proxy_server
```

You can also generate and use self-signed certificates, but self-signed certificates
may not work with some web browswers (e.g. Safari).

### TLS certificates for Docker

You'll need to generate SSL/TLS certificates for the hub server and node servers.
To do this, you can use the keymaster docker container.
First, setup the certificates directory, password, and certificate authority:

```shell
$ mkdir certificates

$ touch certificates/password
$ chmod 600 certificates/password
$ cat /dev/random | head -c 128 | base64 > certificates/password
```

(Use `/dev/urandom` if `/dev/random` takes too long.)

```shell
$ KEYMASTER="sudo docker run --rm -v $(pwd)/certificates/:/certificates/ cloudpipe/keymaster"

$ ${KEYMASTER} ca
```

Then, to generate a keypair for a server:

```shell
$ ${KEYMASTER} signed-keypair -n server1 -h server1.website.com -p both -s IP:192.168.0.1
```

You'll need to generate keypairs for the hub server and for each of the node servers.
After generating the keypairs, edit `script/assemble_certs` and execute

```shell
$ ./script/assemble_certs
```
## Encrypt with ansible-vault

Some files, such as SSL certificates and `vars.yml`, should not be stored in plain text.

```shell
$ ansible-vault encrypt vars.yml
$ ansible-vault encrypt host_vars/proxy_server
$ ansible-vault encrypt host_vars/jupyterhub_host
$ ansible-vault encrypt host_vars/jupyterhub_node1
$ ansible-vault encrypt host_vars/jupyterhub_node2
```

## Set up Duplicity for backup

Generate a key pair in the `nfs_server` machine:

```shell
$ ssh-keygen -t rsa
```

Press Enter at the prompts to create a password-less SSH key with the default settings.

Transfer it to the system that will host your backups:

```shell
$ ssh-copy-id root@backupHost
```

Test that you can now log in without a password from your `nfs_server` by issuing:

```shell
$ ssh -oHostKeyAlgorithms='ssh-rsa' root@backupHost
```

We can use GPG for extra security and encryption. The commands will store our keys in a hidden directory at /root/.gnupg/:

```shell
$ gpg --gen-key
```

Use the key to define the `gpg_key` and `gpg_pass` variables in `vars.yml`.

## Deploy

```shell
$ ./script/deploy
```

This shell script will ask for SSH passwords and ansible-vault password.
