#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from config import config
from db import database

class datenfresserMonitorServer:

    #the monitor is a server which gathers the logs of datenfresser client instances 
    def __init__(self,port):
	    self.port = port
	    self.dataBase = database()
	    self.startServer()

    def startServer( self ):
	#TODO: move log to datenfresserCommon	
	#print "Starting datenfresser monitoring server on port %s" % self.__listen_port
	for logEntry in self.dataBase.getLogs(0):
		print logEntry['start_timestamp']

class datenfresserMonitorClient:
	
	def __init__(self):
		try: 
			pid = os.fork() 
			if pid > 0:
		    		return
		except OSError, e: 
			print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
			sys.exit(1) 
		print "the monitor is running.."
	
