#!/usr/bin/env python3

import argparse
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

# Base port number for iperf3 tests
BASE_PORT = 5201

class MyTopo(Topo):
    def __init__(self, bw_config=False, loss_param=0, **opts):
        """
        bw_config: if True, configure inter-switch links with bandwidth limits.
        loss_param: if > 0 and bw_config is True, apply this loss percentage on the s2-s3 link.
        """
        self.bw_config = bw_config
        self.loss_param = loss_param
        Topo.__init__(self, **opts)

    def build(self):

        # Add switches.
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Add hosts.
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')  # TCP server

        # Connect hosts to switches.
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s3)
        self.addLink(h5, s3)
        self.addLink(h6, s4)
        self.addLink(h7, s4)

        # Connect switches.
        if self.bw_config:
            self.addLink(s1, s2, bw=100)
            if self.loss_param > 0:
                self.addLink(s2, s3, bw=50, loss=self.loss_param)
            else:
                self.addLink(s2, s3, bw=50)
            self.addLink(s3, s4, bw=100)
        else:
            self.addLink(s1, s2)
            self.addLink(s2, s3)
            self.addLink(s3, s4)

# Allow loading via "sudo mn --custom setup.py --topo mytopo"
topos = { 'mytopo': (lambda: MyTopo()) }

def task_a(net, cc_scheme):
    """
    Experiment (a): Single flow from h1 to h7.
    """
    h1 = net.get('h1')
    h7 = net.get('h7')
    serverIP = h7.IP()
    
    print("Starting iperf3 server on h7 (port {})...".format(BASE_PORT))
    h7.cmd("iperf3 -s -p {} -D".format(BASE_PORT))
    time.sleep(2)
    
    input("Press Enter to start the iperf3 client on h1...")

    cmd = ("iperf3 -c {} -p {} -b 10M -P 10 -t 150 -C {} "
           "> /tmp/iperf_h1.log 2>&1 &").format(serverIP, BASE_PORT, cc_scheme)
    print("Starting iperf3 client on h1 with scheme '{}' on port {}".format(cc_scheme, BASE_PORT))
    h1.cmd(cmd)
    time.sleep(155)
    print("Experiment (a) completed. Check /tmp/iperf_h1.log for results.")




if __name__ == '__main__':
    setLogLevel('info')
    
    parser = argparse.ArgumentParser(description="Mininet TCP Congestion Control Experiment - Part A")
    parser.add_argument("--cc", type=str, default="reno",
                        help="TCP congestion control scheme")
    args = parser.parse_args()
    
    net = Mininet(topo=MyTopo(bw_config=False), controller=OVSController)
    net.start()
    task_a(net, cc_scheme=args.cc)
    CLI(net)
    net.stop()

