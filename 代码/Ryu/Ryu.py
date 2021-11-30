from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import MAIN_DISPATCHER, HANDSHAKE_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ether
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import ipv6
from ryu import utils

class MULTIPATH_13(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]


    #初始化函数，使用其超类也就是ryuapp程序的初始化并且创建mac地址与端口的映射表，以及一个标识符
    def __init__(self, *args, **kwargs):

        super(MULTIPATH_13, self).__init__(*args, **kwargs)

        self.mac_to_port = {}

        self.datapaths = {}

        self.FLAGS = True

    #错误处理函数，用与汇报消息msg的错误类型错误码等
    @set_ev_cls(

        ofp_event.EventOFPErrorMsg,

        [HANDSHAKE_DISPATCHER, CONFIG_DISPATCHER, MAIN_DISPATCHER])

    def error_msg_handler(self, ev):

        msg = ev.msg

        self.logger.debug('OFPErrorMsg received: type=0x%02x code=0x%02x '

                          'message=%s', msg.type, msg.code,

                          utils.hex_array(msg.data))


    #状态切换函数

    @set_ev_cls(ofp_event.EventOFPStateChange,

                [MAIN_DISPATCHER, DEAD_DISPATCHER])

    def _state_change_handler(self, ev):

        #将需要更换状态的交换机传参进来并记录下交换机datapath

        datapath = ev.datapath

        #如果该交换机是正常状态MAIN_DISPATCHER，则把该交换机加入列表datapaths中

        if ev.state == MAIN_DISPATCHER:

            if not datapath.id in self.datapaths:

                self.logger.debug('register datapath: %016x', datapath.id)

                self.datapaths[datapath.id] = datapath

        #如果是连接断开的状态DEAD_DISPATCHER，则把该交换机从列表datapaths中删除

        elif ev.state == DEAD_DISPATCHER:

            if datapath.id in self.datapaths:

                self.logger.debug('unregister datapath: %016x', datapath.id)

                del self.datapaths[datapath.id]

    #控制器配置交换机

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)

    def switch_features_handler(self, ev):

        datapath = ev.msg.datapath
        #交换机
        dpid = datapath.id
        #交换机id编号
        ofproto = datapath.ofproto
        #采用的协议（openflow1.3）
        parser = datapath.ofproto_parser
        #协议解析parser
        match = parser.OFPMatch()
        #匹配域
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,

                                          ofproto.OFPCML_NO_BUFFER)]
        #动作（使用opf1.3协议让控制器连接上交换机）
        self.add_flow(datapath, 0, 0, match, actions)
        #下发连接流表到对应交换机上实现连接
        self.logger.info("switch:%s connected", dpid)

    #下发流表
    def add_flow(self, datapath, hard_timeout, priority, match, actions):

        ofproto = datapath.ofproto

        #这个交换机采用的协议

        parser = datapath.ofproto_parser

        #协议解析

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,

                                             actions)]

        #inst调用南向接口实现动作actions的应用

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,

                                hard_timeout=hard_timeout,

                                match=match, instructions=inst)

        #mod消息结构，通过mod消息对流表操作

        datapath.send_msg(mod)

    #packetout消息

    def _build_packet_out(self, datapath, buffer_id, src_port, dst_port, data):

        actions = []

        if dst_port:

            actions.append(datapath.ofproto_parser.OFPActionOutput(dst_port))

        #如果存在目的端口则在动作列表中添加动作：交换机.协议解析.转发规则动作（目的端口）

        msg_data = None

        if buffer_id == datapath.ofproto.OFP_NO_BUFFER:

            if data is None:

                return None

            msg_data = data

        #如果这是个无效缓冲区间的buffer，而且里面有数据，就传给msg_data，否则返回空值

        out = datapath.ofproto_parser.OFPPacketOut(

            datapath=datapath, buffer_id=buffer_id,

            data=msg_data, in_port=src_port, actions=actions)

        return out

        #返回out消息

    #下发packet_out消息的函数
    def send_packet_out(self, datapath, buffer_id, src_port, dst_port, data):

        out = self._build_packet_out(datapath, buffer_id,

                                     src_port, dst_port, data)

        if out:

            datapath.send_msg(out)


    #广播消息
    def flood(self, msg):

        datapath = msg.datapath

        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser

        out = self._build_packet_out(datapath, ofproto.OFP_NO_BUFFER,

                                     ofproto.OFPP_CONTROLLER,

                                     ofproto.OFPP_FLOOD, msg.data)

        #广播消息的datapath，对应协议，协议解析器，消息结构设置

        datapath.send_msg(out)

        #下发给交换机

        self.logger.debug("Flooding msg")


    #ARP转发函数
    def arp_forwarding(self, msg, src_ip, dst_ip, eth_pkt):

        datapath = msg.datapath

        parser = datapath.ofproto_parser

        in_port = msg.match['in_port']

        out_port = self.mac_to_port[datapath.id].get(eth_pkt.dst)

        #交换机，协议解析器，入端口，出端口（来自于映射表中的目的地址）

        #如果出端口在映射表中，则转发

        if out_port is not None:

            match = parser.OFPMatch(in_port=in_port, eth_dst=eth_pkt.dst,

                                    eth_type=eth_pkt.ethertype)

            actions = [parser.OFPActionOutput(out_port)]

            self.add_flow(datapath, 0, 1, match, actions)

            self.send_packet_out(datapath, msg.buffer_id, in_port,

                                 out_port, msg.data)

            self.logger.debug("Reply ARP to knew host")

             #匹配域，动作，packetout消息下发，提供转发规则

        else:

            #因为找不到所以广播

            self.flood(msg)


    #地址学习，传参有交换机id，源地址，入端口
    def mac_learning(self, dpid, src_mac, in_port):

        self.mac_to_port.setdefault(dpid, {})

        #把源地址与该交换机的入端口匹配，返回值表示匹配是否成功

        if src_mac in self.mac_to_port[dpid]:

            if in_port != self.mac_to_port[dpid][src_mac]:

                return False

        else:

            self.mac_to_port[dpid][src_mac] = in_port

            return True

    #发送组表消息（用于控制负载均衡）

    def send_group_mod(self, datapath,):

        ofproto = datapath.ofproto

        ofp_parser = datapath.ofproto_parser

        #协议以及协议解析器

        port_1 = 3

        queue_1 = ofp_parser.OFPActionSetQueue(0)

        actions_1 = [queue_1, ofp_parser.OFPActionOutput(port_1)]



        port_2 = 2

        queue_2 = ofp_parser.OFPActionSetQueue(0)

        actions_2 = [queue_2, ofp_parser.OFPActionOutput(port_2)]

        #设置了两种动作两个队列让流量入队，当队列达到带宽限制的时候就不能入队，此时需要入另外一个队

        weight_1 = 50

        weight_2 = 50



        watch_port = ofproto_v1_3.OFPP_ANY

        watch_group = ofproto_v1_3.OFPQ_ALL



        buckets = [

            ofp_parser.OFPBucket(weight_1, watch_port, watch_group, actions_1),

            ofp_parser.OFPBucket(weight_2, watch_port, watch_group, actions_2)]

        #设置了组表的规则buckets

        group_id = 50

        req = ofp_parser.OFPGroupMod(datapath, ofproto.OFPFC_ADD,

                                     ofproto.OFPGT_SELECT, group_id, buckets)



        datapath.send_msg(req)

        #下发组表规则

    #包的处理程序，分为ipv4包和ipv6包
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)

    def _packet_in_handler(self, ev):

        msg = ev.msg

        datapath = msg.datapath

        dpid = datapath.id

        parser = datapath.ofproto_parser

        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)

        eth = pkt.get_protocols(ethernet.ethernet)[0]

        arp_pkt = pkt.get_protocol(arp.arp)

        ip_pkt = pkt.get_protocol(ipv4.ipv4)

        ip_pkt_6 = pkt.get_protocol(ipv6.ipv6)

        #消息，交换机，交换机id，协议解析器，入端口，数据包，以太网协议，arp包，ip4包，ipv6包

        #如果ipv6是实例，则采用含有ipv6的规则
        if isinstance(ip_pkt_6, ipv6.ipv6):

            actions = []

            match = parser.OFPMatch(eth_type=ether.ETH_TYPE_IPV6)

            self.add_flow(datapath, 0, 1, match, actions)

            return


        #如果arp是实例，则采用含有arp的规则
        if isinstance(arp_pkt, arp.arp):

            self.logger.debug("ARP processing")

            if self.mac_learning(dpid, eth.src, in_port) is False:

                self.logger.debug("ARP packet enter in different ports")

                return



            self.arp_forwarding(msg, arp_pkt.src_ip, arp_pkt.dst_ip, eth)

        #如果ipv4是实例，则采用含有ipv4协议的规则
        if isinstance(ip_pkt, ipv4.ipv4):

            self.logger.debug("IPV4 processing")

            out_port = None
            #如果以太网的目的地址在映射表中存在则下发组表
            if eth.dst in self.mac_to_port[dpid]:

	#如果是1/2/3号交换机则下发组表（负载均衡规则），因为1/2/3号交换机是分岔口

               if (dpid == 1 or dpid == 2 or dpid == 3) and in_port == 1:

                    if self.FLAGS1 is True:

                        self.send_group_mod(datapath)

                        self.logger.info("send_group_mod to s1")

                        self.FLAGS1 = False
		    
                    if self.FLAGS2 is True:

                        self.send_group_mod(datapath)

                        self.logger.info("send_group_mod to s2")

                        self.FLAGS2 = False

                    if self.FLAGS3 is True:

                        self.send_group_mod(datapath)

                        self.logger.info("send_group_mod to s3")

                        self.FLAGS3 = False

	    #从组表中选择一个规则进行下发

                    actions = [parser.OFPActionGroup(group_id=50)]

                    match = parser.OFPMatch(in_port=in_port,

                                            eth_type=eth.ethertype,

                                            ipv4_src=ip_pkt.src)

                    self.add_flow(datapath, 0, 3, match, actions)

                    self.send_packet_out(datapath, msg.buffer_id,

                                         in_port, 2, msg.data)

               else:

                    #普通交换机的普通流

                    out_port = self.mac_to_port[dpid][eth.dst]

                    actions = [parser.OFPActionOutput(out_port)]

                    match = parser.OFPMatch(in_port=in_port, eth_dst=eth.dst,

                                            eth_type=eth.ethertype)

                    self.add_flow(datapath, 0, 1, match, actions)

                    self.send_packet_out(datapath, msg.buffer_id, in_port,

                                         out_port, msg.data)

            else:

                if self.mac_learning(dpid, eth.src, in_port) is False:

                    self.logger.debug("IPV4 packet enter in different ports")

                    return

                else:

                    self.flood(msg)
