import transmissionrpc
import sys
import getopt

def getStats(host, port, username, password):
	try:
	    client = transmissionrpc.Client(host, port=port, user=username, password=password)
	except transmissionrpc.transmission.TransmissionError, err:
	    print err
	    sys.exit(1)
	
	stats = client.session_stats(10)
	
	print("transmission,name=stats torrentCount={}i,activeTorrentCount={}i,pausedTorrentCount={}i,downloadedBytes={}i,uploadedBytes={}i".format(stats.torrentCount, stats.activeTorrentCount, stats.pausedTorrentCount, stats.cumulative_stats['downloadedBytes'], stats.cumulative_stats['uploadedBytes']))

def usage():
   print("Usage: {} -u <username> -p <password> -i <ip> -p <port>".format(sys.argv[0]))
   sys.exit(1)

def main():
	username = None
	password = None
	host = None
	port = 0
	
	opts, args = getopt.getopt(sys.argv[1:], 'u:p:i:x:', ['username=',
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
	    elif opt in ('-x'):
	    	port = arg

	if username is None or password is None or host is None or port == 0:
		usage()

	getStats(username=username, password=password, host=host, port=port)

if __name__ == '__main__':
    main()
