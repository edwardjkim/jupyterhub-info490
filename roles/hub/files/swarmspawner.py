from tornado import gen
from dockerspawner import DockerSpawner
import os
from traitlets import Unicode

# urllib3 complains that we're making unverified HTTPS connections to swarm,
# but this is ok because we're connecting to swarm via 127.0.0.1. I don't
# actually want swarm listening on a public port, so I don't want to connect
# to swarm via the host's FQDN, which means we can't do fully verified HTTPS
# connections. To prevent the warning from appearing over and over and over
# again, I'm just disabling it for now.
import requests
requests.packages.urllib3.disable_warnings()


class SwarmSpawner(DockerSpawner):

    container_ip = '0.0.0.0'

    singleuser = Unicode('jupyter', config=True)

    @gen.coroutine
    def lookup_node_name(self):
        """Find the name of the swarm node that the container is running on."""
        containers = yield self.docker('containers', all=True)
        for container in containers:
            if container['Id'] == self.container_id:
                name, = container['Names']
                node, container_name = name.lstrip("/").split("/")
                raise gen.Return(node)

    @gen.coroutine
    def start(self, image=None, extra_create_kwargs=None, extra_host_config=None):
        # look up mapping of node names to ip addresses
        info = yield self.docker('info')
        self.log.debug(info)
        num_nodes = int(info['SystemStatus'][3][1])
        node_info = info['SystemStatus'][4::9]
        self.node_info = {}
        for i in range(num_nodes):
            node, ip_port = node_info[i]
            self.node_info[node.strip()] = ip_port.strip().split(":")[0]
        self.log.debug("Swarm nodes are: {}".format(self.node_info))

        # specify extra host configuration
        if extra_host_config is None:
            extra_host_config = {}
        if 'mem_limit' not in extra_host_config:
            extra_host_config['mem_limit'] = '512m'

        # specify extra creation options
        if extra_create_kwargs is None:
            extra_create_kwargs = {}
        if 'working_dir' not in extra_create_kwargs:
            extra_create_kwargs['working_dir'] = "/home/{}".format(self.singleuser)

        # start the container
        yield DockerSpawner.start(
            self, image=image,
            extra_create_kwargs=extra_create_kwargs,
            extra_host_config=extra_host_config)

        # figure out what the node is and then get its ip
        name = yield self.lookup_node_name()
        self.user.server.ip = self.node_info[name]
        self.log.info("{} was started on {} ({}:{})".format(
            self.container_name, name, self.user.server.ip, self.user.server.port))

        self.log.info(self.env)


class SwarmFormSpawner(SwarmSpawner):

    def _options_form_default(self):
        return """
        <label for="env">Select environment.</label>
        <select class="form-control" name="env" style="width: 300px;">
            <option value="singleuser">lcdm/info490 (Weeks 1-11)</option>
            <option value="hadoop">lcdm/info490-hadoop (Week 12)</option>
            <option value="singleuser">lcdm/info490 (Week 13)</option>
            <option value="spark">lcdm/info490-spark (Week 14)</option>
            <option value="singleuser">lcdm/info490 (Week 15)</option>
        </select>
        <p>
          <br><br>
          lcdm/info490-hadoop takes a while to load. Please be patient.
          If your browser displays an error, try reloading the page (Ctrl+F5).
        </p>
        """

    def options_from_form(self, formdata):
        options = {}
        options['env'] = env = {}
        
        env_lines = formdata.get('env', [''])
        options['env'] = formdata['env'][0] 

        return options
    
    def get_env(self):
        env = super().get_env()
        if self.user_options.get('env'):
            env.update(self.user_options)
        return env

    @gen.coroutine
    def start(self, image=None, extra_create_kwargs=None, extra_host_config=None):
        # look up mapping of node names to ip addresses
        info = yield self.docker('info')
        num_nodes = int(info['DriverStatus'][3][1])
        node_info = info['DriverStatus'][4::6]
        self.node_info = {}
        for i in range(num_nodes):
            node, ip_port = node_info[i]
            self.node_info[node] = ip_port.split(":")[0]
        self.log.debug("Swarm nodes are: {}".format(self.node_info))

        # specify extra creation options
        if extra_create_kwargs is None:
            extra_create_kwargs = {}
        if 'working_dir' not in extra_create_kwargs:
            extra_create_kwargs['working_dir'] = "/home/{}".format(self.singleuser)

        # specify extra host configuration
        if extra_host_config is None:
            extra_host_config = {}

        if self.user_options['env'] == 'singleuser':
            image = 'singleuser'
            if 'mem_limit' not in extra_host_config:
                extra_host_config['mem_limit'] = '1g'
        elif self.user_options['env'] == 'hadoop':
            image = 'hadoop'
            if 'mem_limit' not in extra_host_config:
                extra_host_config['mem_limit'] = '3g'
        elif self.user_options['env'] == 'spark':
            image = 'spark'
            if 'mem_limit' not in extra_host_config:
                extra_host_config['mem_limit'] = '2g'
        else:
            image = 'singleuser'
            if 'mem_limit' not in extra_host_config:
                extra_host_config['mem_limit'] = '1g'

        # start the container
        yield DockerSpawner.start(
            self, image=image,
            extra_create_kwargs=extra_create_kwargs,
            extra_host_config=extra_host_config)

        # figure out what the node is and then get its ip
        name = yield self.lookup_node_name()
        self.user.server.ip = self.node_info[name]
        self.log.info("{} was started on {} ({}:{})".format(
            self.container_name, name, self.user.server.ip, self.user.server.port))

        self.log.info(self.env)
