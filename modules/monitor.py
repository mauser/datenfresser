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
	    self.startServer()

    def startServer( self ):
	#TODO: move log to datenfresserCommon	
	#print "Starting datenfresser monitoring server on port %s" % self.__listen_port
	
	#or logEntry in self.dataBase.getLogs(0):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	server.bind(("", 50000)) 
	server.listen(1)

	clients = []

	try: 
	    while True: 
		read, write, oob = select.select([server] + clients, [], [])

		for sock in read: 
		    if sock in server: 
			client, addr = server.accept() 
			clients.append(client) 
			print "#Client %s connected" % addr[0] 
		    else: 
			nachricht = sock.recv(1024) 
			ip = sock.getpeername()[0] 
			if nachricht: 
			    print "[%s] %s" % (ip, nachricht) 
			else: 
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
	
