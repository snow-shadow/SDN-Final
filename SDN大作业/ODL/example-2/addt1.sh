#c1
sudo ovs-ofctl -O OpenFlow13 add-flow c1 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow c1 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow c1 priority=2,in_port=3,actions=output:1,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow c1 priority=2,in_port=4,actions=output:1,output:2
#a3
sudo ovs-ofctl -O OpenFlow13 add-flow a3 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a3 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a3 priority=2,in_port=3,actions=output:1,output:2,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a3 priority=2,in_port=4,actions=output:1,output:2,output:3
#a5
sudo ovs-ofctl -O OpenFlow13 add-flow a5 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a5 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a5 priority=2,in_port=3,actions=output:1,output:2,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a5 priority=2,in_port=4,actions=output:1,output:2,output:3
