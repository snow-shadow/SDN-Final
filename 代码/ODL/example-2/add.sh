#下层
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

#中层
#a3
sudo ovs-ofctl -O OpenFlow13 add-flow a3 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a3 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a3 priority=2,in_port=3,actions=output:1,output:2,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a3 priority=2,in_port=4,actions=output:1,output:2,output:3
#a4
sudo ovs-ofctl -O OpenFlow13 add-flow a4 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a4 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a4 priority=2,in_port=3,actions=output:1,output:2,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a4 priority=2,in_port=4,actions=output:1,output:2,output:3
#a5
sudo ovs-ofctl -O OpenFlow13 add-flow a5 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a5 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a5 priority=2,in_port=3,actions=output:1,output:2,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a5 priority=2,in_port=4,actions=output:1,output:2,output:3
#a6
sudo ovs-ofctl -O OpenFlow13 add-flow a6 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a6 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a6 priority=2,in_port=3,actions=output:1,output:2,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow a6 priority=2,in_port=4,actions=output:1,output:2,output:3

#底层
#c1
sudo ovs-ofctl -O OpenFlow13 add-flow c1 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow c1 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow c1 priority=2,in_port=3,actions=output:1,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow c1 priority=2,in_port=4,actions=output:1,output:2
#c2
sudo ovs-ofctl -O OpenFlow13 add-flow c2 priority=2,in_port=1,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow c2 priority=2,in_port=2,actions=output:3,output:4
sudo ovs-ofctl -O OpenFlow13 add-flow c2 priority=2,in_port=3,actions=output:1,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow c2 priority=2,in_port=4,actions=output:1,output:2
