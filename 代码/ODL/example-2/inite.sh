#e7
sudo ovs-ofctl -O OpenFlow13 add-flow e7 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e7 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e7 priority=2,in_port=3,actions=output:1,output:2,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e7 priority=2,in_port=4,actions=output:1,output:2,output:3
#e8
sudo ovs-ofctl -O OpenFlow13 add-flow e8 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e8 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e8 priority=2,in_port=3,actions=output:1,output:2,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e8 priority=2,in_port=4,actions=output:1,output:2,output:3
#e9
sudo ovs-ofctl -O OpenFlow13 add-flow e9 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e9 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e9 priority=2,in_port=3,actions=output:1,output:2,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e9 priority=2,in_port=4,actions=output:1,output:2,output:3
#e10
sudo ovs-ofctl -O OpenFlow13 add-flow e10 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e10 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e10 priority=2,in_port=3,actions=output:1,output:2,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow e10 priority=2,in_port=4,actions=output:1,output:2,output:3
