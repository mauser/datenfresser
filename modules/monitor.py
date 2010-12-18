#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import socket 
import select
from string import find

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
		#state = "recv" for chunked transfer to bypass sends
		self.state = ""

class datenfresserMonitorServer:

    #the monitor is a server which gathers the logs of datenfresser client instances 
    def __init__(self,port):
	    self.port = port
	    self.database = database()
	    self.config = config()
	    self.xmlHandler = xmlHandler()
	    
	    self.startServer()

    def reply( self, mySocket, message):
	    mySocket.send(message)

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
			result = "ok"
			while 1:
				print "before recv"
				message = sock.recv(1024)
				
				if len(message) == 0: 
					reply( sock, result )
					break
			
			
				ip = sock.getpeername()[0]
				ipPortTuple = sock.getpeername()
				
				#check if this is a part of a chunked transfer
				if ipPortTuple in state.keys() and  state[ ipPortTuple ].state == "recv":
					state[ ipPortTuple ].length -= 1024
					state[ ipPortTuple ].data  += message
					if state[ ipPortTuple ].length  <= 0:
						print "end of receive"
						state[ ipPortTuple ].state = ""
						self.reply(sock, "recv ok")
						break
					continue



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
					result = "auth ok"
				else: 
					if ipPortTuple in state.keys() and state[ ipPortTuple ].authState == "authenticated":
						pass
					else:
						print "not authenticated"
						print "#Connection to %s closed" % ip 
						#sock.close() 
						#clients.remove(sock)
					
					if message[0:4] == "data":
						#format: 'data sizeof(x) 01100011....'
						print "Adding data was requested"
						parts = message.split(" ")

						#store the size of the whole data
						state[ ipPortTuple ].length = int(parts[1])

						#we have already received 1024 byte
						state[ ipPortTuple ].length -= 1024
						
						#if we're receiving multiple packates, change state of this recv. thread 
						if state[ ipPortTuple ].length > 0:
							state[ ipPortTuple ].state = "recv"
							

						startOfData = find( message, parts[1])
						startOfData = startOfData + len(parts[1])
						state[ ipPortTuple ].data = message[startOfData:]
						print message[startOfData:]
						print "received first chunk"



					if message[0:6] == "commit":
						print "Committing your data"
						m = self.xmlHandler.parseXml( state[ ipPortTuple ].data )	
						self.database.insertMonitorLog( m )
						result = "commit ok"

					if message[0:9] == "getLastID":
						parts = message.split(" ")
						host = parts[1].strip()
						print "Getting last id for host " + host
						result = str(self.database.getLastRemoteLogID( host )) 
						print result
					
					
					if message[0:4] == "exit":
						print "#Connection to %s closed" % ip
						result = "exit"
						sock.send("bye")
						sock.close() 
						del state[ipPortTuple] 
						clients.remove(sock)
						break
					
				if len(message) == 0 or len(message) < 1024 and result != "exit":
					self.reply( sock, result )
					break

	finally: 
	    for c in clients: 
		c.close() 
	    server.close()

	#print logEntry['start_timestamp']

class datenfresserMonitorClient:
	
	def __init__(self):

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.connect(("localhost", 8090))
		c = config()
		d = database()
		self.xml = xmlHandler()
		#return

		try: 
			s.send("auth " + c.getMonitorUser() + " " +  c.getMonitorPassword() )
			print s.recv(1024)
			#s.send("data " + self.xml.logEntryToXml( monitorLog() ))
			#s.send("commit")
			s.send("getLastID " + c.getHostname())
			lastId = int( s.recv(1024) )
			print lastId
			
			logs = d.getLogs( lastId)
			print len(logs)

			for i in range(0, 1):
				print i
				data = self.xml.logEntryToXml( c.getHostname(), logs[i] )
				print len(data)
				print sys.getsizeof(data)
				print "Send data, #bytes: " + str( s.sendall("data " + str(sys.getsizeof(data)) + " " + data ))
				print s.recv(1024)
				s.send("commit")
				print s.recv(1024)


			s.send("exit")
			print s.recv(1024)
		finally: 
		    s.close()


if __name__ == '__main__':
	d = datenfresserMonitorClient()
