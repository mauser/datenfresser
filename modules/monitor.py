#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import socket 
import select

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from config import config
from db import database
from db import monitorLog
from xmlHandler import xmlHandler


class stateContainer:
	#holds all the state which is related to a client request
	def __init__( self ):
		#current authentication status
		self.authState = "unauthenticated"
		#number of data packets (a 1024 byte) which will be sent
		self.length = 0
		#data which already arrived
		self.data = ""

class datenfresserMonitorServer:

    #the monitor is a server which gathers the logs of datenfresser client instances 
    def __init__(self,port):
	    self.port = port
	    self.dataBase = database()
	    self.config = config()
	    self.xmlHandler = xmlHandler()
	    
	    self.startServer()

    def startServer( self ):
	print "Starting datenfresser monitoring server on port %s" % self.port
	
	#or logEntry in self.dataBase.getLogs(0):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
	server.bind(("", int(self.port))) 
	server.listen(1)

	clients = []
	state = {}

	try: 
	    while True: 
		read, write, oob = select.select([server] + clients, [], [])

		for sock in read: 
		    if sock is server: 
			client, addr = server.accept() 
			clients.append(client) 
			print "#Client %s connected" % addr[0] 
		    else: 
			message = sock.recv(1024)
			#if len(message) == 0: break
			ip = sock.getpeername()[0]
			ipPortTuple = sock.getpeername()
			

			#every client has to authenticate itself at the
			#beginning of a transmission
			if message[0:4] == "auth":
				parts = message.split(" ")
				user = parts[1].strip()
				password = parts[2].strip()

				if user == self.config.getMonitorUser() and password == self.config.getMonitorPassword():
					newState = stateContainer()
					newState.authState = "authenticated"
					state[ ipPortTuple ] = newState
				else:
					print "wrong credentials"
					sock.close()
					clients.remove(sock)	
	
			    	print "[%s] %s" % (ip, message)
				print state
			else: 

				if ipPortTuple in state.keys() and state[ ipPortTuple ].authState == "authenticated":
					print "authenticated!"
				else:
					print "not authenticated"
			    		print "#Connection to %s closed" % ip 
			    		sock.close() 
			    		clients.remove(sock)
				
				
				if message[0:4] == "data":
			    		print "Adding data was requested"
					parts = message.split(" ")
					state[ ipPortTuple ].data += parts[1].rstrip()
					print state[ ipPortTuple ].data


				if message[0:6] == "commit":
			    		print "Committing your data"
					self.xmlHandler.parseXml( state[ ipPortTuple ].data )	

				if message[0:8] == "getLastID":
					parts = message.split(" ")
					host = parts[1].strip()
			    		print "Getting last id for host " + host 
					self.xmlHandler.parseXml( state[ ipPortTuple ].data )	

				
				if message[0:4] == "exit":
			    		print "#Connection to %s closed" % ip

					sock.close() 
					del state[ipPortTuple] 
			    		clients.remove(sock)

	finally: 
	    for c in clients: 
		c.close() 
	    server.close()

	#print logEntry['start_timestamp']

class datenfresserMonitorClient:
	
	def __init__(self):

		#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		#s.connect(("localhost", 8090))
		c = config()
		self.xml = xmlHandler()
		self.xml.logEntryToXml( monitorLog() )
		return

		try: 
			s.send("auth " + c.getMonitorUser() + " " +  c.getMonitorPassword() )
			s.send("data " + self.xml.logEntryToXml( monitorLog() ))
			s.send("commit")
			s.send("exit")
		finally: 
		    s.close()


if __name__ == '__main__':
	d = datenfresserMonitorClient()
