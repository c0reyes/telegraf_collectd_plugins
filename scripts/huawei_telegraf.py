#!/usr/bin/python

import urllib3
import base64
import string
import sys
import getopt
import os
import re

def getInfo(username, password, host):
	http = urllib3.HTTPConnectionPool(host)

	# Login
	request = http.request('GET','/asp/GetRandCount.asp')

	## Parameters
	password64 = base64.b64encode(str.encode(password)).decode('ascii')
    fields = 'UserName={}&PassWord={}&x.X_HW_Token={}'.format(username, password64, request.data.decode('utf-8-sig'))

    ## Headers
    cookie = 'Cookie=body:Language:english:id=-1'.format(username, password64)
    headers = {'Referer': 'http://{}/'.format(host), 'Cookie' : cookie}

    request = http.request('POST', '/login.cgi', body=fields, headers=headers)
    headers = {'Cookie': request.headers['set-cookie']}

    # Random page
    http.request('GET', '/frame.asp', headers=headers)

    # Data
    request = http.request('GET', '/html/amp/ethinfo/ethinfo.asp', headers=headers)
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
			print("port,name={} rx={}i,tx={}i".format(name.group(0).replace(".","_"), tmp[4], tmp[2]))

	# Device
	request = http.request('GET', '/html/status/deviceinfo.asp', headers=headers)
	data = request.data.decode('UTF-8').split('\r\n')

	cpu = 0
	mem = 0

	for d in data:
		if "var cpuUsed" in d:
			cpu1 = re.search("(?<=var cpuUsed = \')\d+(?=\%\'\;)", d)
			cpu = float(cpu1.group(0)) / 100

		if "var memUsed" in d:
			mem1 = re.search("(?<=var memUsed = \')\d+(?=\%\'\;)", d)
			mem = float(mem1.group(0)) / 100

	print("info,name=device mem={},cpu={}".format(mem, cpu))

def usage():
   print("Usage: {} -u <username> -p <password> -i <ip> [-l <interval>".format(sys.argv[0]))
   sys.exit(1)

def main():
	username = None
	password = None
	host = None

	opts, args = getopt.getopt(sys.argv[1:], 'u:p:i:', ['username=',
                                                  'password=',
                                                  'ip='])

	if not opts:
	    usage()
	    sys.exit(1)

	for opt, arg in opts:
	    if opt in ('-u', '--username'):
	        username = arg
	    elif opt in ('-p', '--password'):
	        password = arg
	    elif opt in ('-i', '--ip'):
	        host = arg

	if username is None or password is None or host is None:
		usage()

	getInfo(username=username, password=password, host=host)

if __name__ == '__main__':
    main()
