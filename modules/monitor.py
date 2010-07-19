#!/usr/bin/python
# -*- coding: utf-8 -*-


class datenfresserMonitorServer:

    #the monitor is a server which gathers the logs of datenfresser client instances 

    # allow access from localhost and local network
    
    def startServer( self ):
	
	os.chdir( "/usr/lib/datenfresser/web")
	
	try: 
		pid = os.fork() 
		if pid > 0:
		    return
	except OSError, e: 
		print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
		sys.exit(1) 

	print "Starting datenfresser webserver on port %s" % self.__listen_port
	httpd = MyThreadingServer( ("", self.__listen_port ), MyRequestHandler, self.AllowIPs )
	httpd.serve_forever()

class datenfresserMonitorClient:
	
	def _init_(self):
		try: 
			pid = os.fork() 
			if pid > 0:
		    		return
		except OSError, e: 
			print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
			sys.exit(1) 
		print "the monitor is running.."
	
