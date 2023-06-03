from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import time
import os
from mininet.node import Controller
from ryu.lib import hub

import pandas as pd
from AttackGeneration import attack_generation
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri



class MyTopology(Topo):
    def __init__(self):
        Topo.__init__(self)

        # Add switches
        switches = []
        for i in range(6):
            switch = self.addSwitch('s{}'.format(i+1), cls=OVSSwitch)
            switches.append(switch)

        # Add hosts
        hosts = []
        for i in range(8):
            host = self.addHost('h{}'.format(i+1))
            hosts.append(host)

        # Add servers
        servers = []
        for i in range(4):
            server = self.addHost('server{}'.format(i+1))
            servers.append(server)

        # Add links between switches and hosts
        for i in range(len(hosts)):
            switch = switches[i % len(switches)]
            self.addLink(hosts[i], switch)

        # Add links between switches and servers
        for i in range(len(servers)):
            switch = switches[i % len(switches)]
            self.addLink(servers[i], switch)

        # Add links between switches
        for i in range(len(switches) - 1):
            self.addLink(switches[i], switches[i+1])

topology = MyTopology()

# Specify the custom Ryu controller
ryu_controller = Controller(name='ryu_controller', command='ryu-manager --verbose Controller.py')

# Create the Mininet network with the custom Ryu controller
net = Mininet(topo=topology, link=TCLink, controller=ryu_controller)

# Start the Ryu controller in a separate thread
def start_controller():
    ryu_controller.start()
hub.spawn(start_controller)

# Start the Mininet network
net.start()

attack_generation()

r_model = robjects.r['readRDS']('my_model.rds')
# Convert the Pandas DataFrame to an R DataFrame
test_attack_data = pd.read_csv("captured_data.csv")
#pandas2ri.activate()
r_data = pandas2ri.py2ri(test_attack_data)

# Make predictions using the R model
r_predictions = robjects.r['predict'](r_model, r_data)

predictions = pandas2ri.ri2py(r_predictions)
#predictions_df = pd.DataFrame(predictions, columns=['label'])
predictions_array = predictions.to_numpy()

switches = net.switches
controllers = net.controllers

# Get the target IP addresses based on the predictions
target_ips = r_data.loc[predictions_array == 'attack', 'ip_src'].values

# Block the IP addresses using OpenFlow rules
for switch in switches:
    for controller in controllers:
        switch.setController(controller)
        for target_ip in target_ips:
            command = 'ovs-ofctl add-flow {} priority=100,ip,nw_src={},actions=drop'.format(switch, target_ip)
            switch.dpctl(command)
            print("Ip address",target_ip,"Blocked")

# Configure VPN on each host
for host in net.hosts:
    host.cmd('apt-get update')
    host.cmd('apt-get install -y openvpn')

    # Copy the VPN configuration files to the host
    host.cmd('mkdir -p /etc/openvpn')
    host.cmd('cp vpn-client.ovpn /etc/openvpn/client.conf')
    host.cmd('cp vpn-client.crt /etc/openvpn/client.crt')
    host.cmd('cp vpn-client.key /etc/openvpn/client.key')

    # Start the VPN connection
    host.cmd('openvpn /etc/openvpn/client.conf &')

# Wait for the VPN connections to establish
time.sleep(10)

# Ping hosts
net.pingAll()

# Run commands on hosts
host = net.get('h1')
output = host.cmd('ifconfig')
print(output)

# Enter the Mininet CLI for further interactions
CLI(net)

# Clean up the network resources
net.stop()
