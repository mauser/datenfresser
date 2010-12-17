#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append("/usr/lib/datenfresser/modules")
sys.path.append("/usr/lib/datenfresser")

from config import config
from db import database

import socket 
import select


class datenfresserMonitorServer:

    #the monitor is a server which gathers the logs of datenfresser client instances 
    def __init__(self,port):
	    self.port = port
	    self.dataBase = database()
	    self.config = config()
	    
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
			ip = sock.getpeername()[0]
			ipPortTuple = sock.getpeername()
			

			#every client has to authenticate itself at the
			#beginning of a transmission
			if message[0:4] == "auth":
				parts = message.split(" ")
				user = parts[1].strip()
				password = parts[2].strip()

				if user == self.config.getMonitorUser() and password == self.config.getMonitorPassword():
					state[ ipPortTuple ] = "ok"
				else:
					print "wrong credentials"
					sock.close()
					clients.remove(sock)	
	
			    	print "[%s] %s" % (ip, message)
				print state
			else: 
				if ipPortTuple in state.keys() and state[ ipPortTuple ] == "ok":
					print "authenticated!"
				else:
					print "not authenticated"
			    		print "#Connection to %s closed" % ip 
			    		sock.close() 
			    		clients.remove(sock)
				
				
				if message[0:3] == "add":
			    		print "Adding was requested"
					

				
				if message[0:4] == "exit":
			    		print "#Connection to %s closed" % ip 
			    		sock.close() 
			    		clients.remove(sock)





	finally: 
	    for c in clients: 
		c.close() 
	    server.close()

	#print logEntry['start_timestamp']

class datenfresserMonitorClient:
	
	def __init__(self):

		print "the monitor is running.."
		import socket

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.connect(("smoors.de", 50000))

		try: 
		    while True: 
			nachricht = raw_input("Enter a message: ") 
			s.send(nachricht) 
		finally: 
		    s.close()
	
