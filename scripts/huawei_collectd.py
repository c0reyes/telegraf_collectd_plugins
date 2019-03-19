#!/usr/bin/python

import urllib3
import base64
import string
import sys
import re
import collectd

username = None
password = None
host = None

def config(config): 
	global username, password, host

	for node in config.children: 
		key = node.key.lower() 
		val = node.values[0] 

		if key == 'username': 
			username = val
		elif key == 'password':
			password = val
		elif key == 'host':
			host = val 

	collectd.info('huawei_collectd plugin: Initialized')

def getInfo():
	global username, password, host
 
	http = urllib3.HTTPConnectionPool(host)
	
	# Login
	request = http.request('GET','/asp/GetRandCount.asp')
	
	## Parameters
	fields = {'': 'x.X_HW_Token={}'.format(request.data.decode('utf-8-sig'))}
	
	## Headers
	password64 = base64.b64encode(str.encode(password)).decode('ascii')
	cookie = 'Cookie=UserName:{}:PassWord:{}:Language:english:id=-1'.format(username, password64)
	headers = {'Referer': 'http://{}/'.format(host), 'Cookie' : cookie}
	
	request = http.request('POST', '/login.cgi', headers=headers, fields=fields)
	headers = {'Cookie': request.headers['set-cookie']}

	# Random page
	http.request('GET', '/frame.asp', headers=headers)

	# Data
	request = http.request('GET', '/html/status/ethinfo.asp', headers=headers)	
	data = request.data.decode('UTF-8').split('\r\n')

	eths = []
	for d in data:
		if "var userEthInfos" in d:
			d = d.replace("var userEthInfos = new Array(","").replace(",null);","").replace(")","").replace("\"","")
			eths = d.split("new LANStats(")
	
	for eth in eths:
		if(eth):
			tmp = eth.split(",")
			name = re.search("(?<=AMP\.).*(?=\.Statistics)", tmp[0])

			v_tmp = collectd.Values(plugin='huawei_collectd', type='if_octets', type_instance=name.group(0).replace(".","_"))
			v_tmp.dispatch(values=[tmp[4], tmp[2]])

collectd.register_config(config)
collectd.register_read(getInfo)


