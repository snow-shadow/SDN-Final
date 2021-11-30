#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
import time
import logging
import os


def multiControllerNet(con_num=1, sw_num=11, host_num=4):

	controller_list = []
	switch_list = []
	host_list = []
	
	net = Mininet(controller=None, switch=OVSSwitch, link=TCLink)
	
	name = 'controller0' 
	c = net.addController(name, controller=RemoteController,ip='127.0.0.1',port=6633)
	controller_list.append(c)
	print("*** Creating %s" % name)
	
	print("*** Creating switches")
	switch_list = [net.addSwitch('s%d' % n) for n in xrange(sw_num)]
	print(switch_list)
	print("*** Creating hosts")
	
	host_list = [net.addHost('h%d' % n) for n in xrange(1,host_num+1)]
	
	print("*** Creating links")
	
	net.addLink(switch_list[1], host_list[0],1).bw=10
	net.addLink(switch_list[10], host_list[1],3).bw=10
	net.addLink(switch_list[10], host_list[2],4).bw=10
	net.addLink(switch_list[10], host_list[3],5).bw=10
	net.addLink(switch_list[1], switch_list[2],2,1).bw=10
	net.addLink(switch_list[1], switch_list[3],3,1).bw=10
	net.addLink(switch_list[2], switch_list[4],2,1).bw=10
	net.addLink(switch_list[2], switch_list[5],3,1).bw=10
	net.addLink(switch_list[3], switch_list[6],2,1).bw=10
	net.addLink(switch_list[3], switch_list[7],3,1).bw=10
	net.addLink(switch_list[4], switch_list[8],2,1).bw=10
	net.addLink(switch_list[5], switch_list[8],2,2).bw=10
	net.addLink(switch_list[6], switch_list[9],2,1).bw=10
	net.addLink(switch_list[7], switch_list[9],2,2).bw=10
	net.addLink(switch_list[8], switch_list[10],3,1).bw=10
	net.addLink(switch_list[9], switch_list[10],3,2).bw=10
		
	
	print("*** Starting network")
	net.build()
	c.start()
	
	for i in xrange(sw_num):
		switch_list[i].start([c])
	
	
	print("*** Running CLI")
	
	CLI(net)
	
	print("*** Stopping network")
	
	net.stop()

if __name__ == '__main__':
	setLogLevel('info') 
	multiControllerNet(con_num=1, sw_num=11, host_num=4)
