import httplib2
import time
import json
class OdlUtil:
	url = ''
	def __init__(self, host, port):
		self.url = 'http://' + host + ':' + str(port)
	def install_flow(self, container_name='default',username="admin", password="admin"):
		http = httplib2.Http()
		http.add_credentials(username, password)
		headers = {'Accept': 'application/json'}
		flow_name = 'flow_' + str(int(time.time()*1000))
		
		s1h2body1='{"flow": [{"id": "0","match": {"ethernet-match":'\
            		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.2/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
            		'"apply-actions": {"action": [{"output-action": {'\
            		'"output-node-connector": "1"},"order": "0"}]}}]},'\
            		'"priority": "101","cookie": "1","table_id": "0"}]}'
		s1h3body1='{"flow": [{"id": "1","match": {"ethernet-match":'\
            		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
            		'"apply-actions": {"action": [{"output-action": {'\
            		'"output-node-connector": "1"},"order": "0"}]}}]},'\
            		'"priority": "101","cookie": "1","table_id": "0"}]}'
	
		h2s2body1 ='{"flow": [{"id": "0","match": {"ethernet-match":'\
               		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.2/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
            		'"apply-actions": {"action": [{"output-action": {'\
                	'"output-node-connector": "1"},"order": "0"}]}}]},'\
            		'"priority": "101","cookie": "1","table_id": "0"}]}'
		
		h3s2body1 ='{"flow": [{"id": "1","match": {"ethernet-match":'\
               		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
                	'"apply-actions": {"action": [{"output-action": {'\
                	'"output-node-connector": "1"},"order": "0"}]}}]},'\
            		'"priority": "101","cookie": "1","table_id": "0"}]}'
		mh3s2body1 ='{"flow": [{"id": "1","match": {"ethernet-match":'\
               		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
                	'"apply-actions": {"action": [{"output-action": {'\
                	'"output-node-connector": "1"},"order": "0"}]}}]},'\
            		'"priority": "100","cookie": "1","table_id": "0"}]}'
		
		h3s2body2 ='{"flow": [{"id": "2","match": {"ethernet-match":'\
               		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
                	'"apply-actions": {"action": [{"output-action": {'\
                	'"output-node-connector": "2"},"order": "0"}]}}]},'\
            		'"priority": "101","cookie": "1","table_id": "0"}]}'
		mh3s2body2 ='{"flow": [{"id": "2","match": {"ethernet-match":'\
               		'{"ethernet-type": {"type": "2048"}},'\
					'"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
            		'"instructions": {"instruction": [{"order": "0",'\
                	'"apply-actions": {"action": [{"output-action": {'\
                	'"output-node-connector": "2"},"order": "0"}]}}]},'\
            		'"priority": "100","cookie": "1","table_id": "0"}]}'
		
		s3_1='{"flow": [{"id": "0","match": {"ethernet-match":'\
                '{"ethernet-type": {"type": "2048"}},'\
			        '"ipv4-source":"10.0.0.3/32","ipv4-destination": "10.0.0.1/32"},'\
                '"instructions": {"instruction": [{"order": "0",'\
                '"apply-actions": {"action": [{"output-action": {'\
                '"output-node-connector": "1"},"order": "0"}]}}]},'\
                '"priority": "101","cookie": "1","table_id": "0"}]}'
	
		headers = {'Content-type': 'application/json'}
		num=0
	
		#??????s1???s3?????????
		response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/flow-node-inventory:table/0/flow/0', body=s1h2body1, method='PUT',headers=headers)	
		response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/flow-node-inventory:table/0/flow/1', body=s1h3body1, method='PUT',headers=headers)
		response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:3/flow-node-inventory:table/0/flow/0', body=s3_1, method='PUT',headers=headers)
		#s2??????h2???1?????????			
		response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0/flow/0', body=h2s2body1, method='PUT',headers=headers)
		while num < 4 :
			#??????s2??????1?????????
			uri = 'http://127.0.0.1:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:2/node-connector/openflow:2:1'
			response, content = http.request(uri=uri, method='GET')
			content = json.loads(content)
			statistics = content['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']
			bytes1 = statistics['bytes']['transmitted']
			#0.1??????????????????
			time.sleep(0.1)
			response, content = http.request(uri=uri, method='GET')
			content = json.loads(content)
			statistics = content['node-connector'][0]['opendaylight-port-statistics:flow-capable-node-connector-statistics']
			bytes2 = statistics['bytes']['transmitted']
			#????????????s2???1??????????????????????????????
			speed = float(bytes2-bytes1)/1
			if speed != 0 :#?????????????????????
				if speed < 1000 :
					print('??????s2??????1?????????h3???????????????1?????????')
					response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0/flow/1', body=h3s2body1, method='PUT',headers=headers)
					response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0/flow/2', body=mh3s2body2, method='PUT',headers=headers)
				#????????????s2???1??????????????????????????????
				else :
					print('??????s2??????1?????????h3??????????????????2?????????')
					response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0/flow/1', body=mh3s2body1, method='PUT',headers=headers)
					response, content = http.request(uri='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:2/flow-node-inventory:table/0/flow/2', body=h3s2body2, method='PUT',headers=headers)
odl = OdlUtil('127.0.0.1', '8181')
odl.install_flow()
