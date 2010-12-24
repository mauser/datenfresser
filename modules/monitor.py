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
		#hostname
		self.hostname = "example.org"

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
				ip = sock.getpeername()[0]
				ipPortTuple = sock.getpeername()
				
				if ipPortTuple in state.keys():
					print "before recv; waiting for " + str(state[ ipPortTuple ].length) + " bytes "
				else:
					print "before recv"

				#receive outstanding data
				message = sock.recv(1024)
			
				if ipPortTuple in state.keys() and state[ ipPortTuple ].length == 0:
					print "message: " + message
				

				if len(message) == 0: 
					print "first exit"
					self.reply( sock, "first exit" )
					break
			
		
				#check if this is a part of a chunked transfer
				lastChunk = False
				if ipPortTuple in state.keys() and  state[ ipPortTuple ].state == "recv":
					state[ ipPortTuple ].length -= len(message)
					state[ ipPortTuple ].data  += message
					if state[ ipPortTuple ].length  <= 0: 
						#this was the last chunk, handle the event later
						lastChunk = True
					else:
						#omit a reply and recv the other chunks..
						continue
				
				#check if this was the last chunk
				if lastChunk:
					print "end of receive for"
					print ipPortTuple
					state[ ipPortTuple ].state = ""
					state[ ipPortTuple ].length = 0
					self.reply(sock, "recv ok")
					break

				print "after if for " 
				print ipPortTuple


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
				
					if message[0:4] == "host":
						#announce the clients host name
						parts = message.split(" ")
						state[ ipPortTuple ].hostname = parts[1]
					
					if message[0:11] == "checkDataID":
						#checkDataID id checksum
						#used to check if a data container with this id already exists
						parts = message.split(" ")
						id = parts[1]
						checksum = parts[2]

						if self.database.checkForRemoteContainer( id, state[ ipPortTuple ].hostname , checksum ):
							result = "dataID known"
						else:
							result = "dataID unknown"

					if message[0:17] == "pushDataContainer":
						#checkDataID id checksum
						#used to check if a data container with this id already exists
						parts = message.split(" ")
						id = parts[1]
						checksum = parts[2]

						if self.database.checkForRemoteContainer( id, state[ ipPortTuple ].hostname , checksum ):
							result = "dataID known"
						else:
							result = "dataID unknown"






					if message[0:4] == "data":
						#format: 'data sizeof(x) 01100011....'
						print "Adding data was requested"
						parts = message.split(" ")

						#store the size of the whole data
						state[ ipPortTuple ].length = int(parts[1])

				
						#calculate the payload size
						startOfData = find( message, parts[1])
						startOfData = startOfData + len(parts[1])
						payload = message[startOfData:]
						payloadSize = len(payload)

						#we have already received the first chunk 
						state[ ipPortTuple ].length -= payloadSize 
						
						#if we're receiving multiple packates, change state of this recv. thread 
						if state[ ipPortTuple ].length > 0:
							state[ ipPortTuple ].state = "recv"
							
						state[ ipPortTuple ].data = payload						
						print "received first chunk"



					if message[0:6] == "commit":
						print "Committing your data"
						#print state[ ipPortTuple ].data 
						m = self.xmlHandler.parseXml( state[ ipPortTuple ].data )	
						self.database.insertMonitorLog( m )
						result = "commit ok"

					if message[0:9] == "getLastID":
						parts = message.split(" ")
						host = parts[1].strip()
						print "Getting last id for host " + host
						result = str(self.database.getLastRemoteLogID( host ))
					
					
					if message[0:4] == "exit":
						print "#Connection to %s closed" % ip
						result = "exit"
						sock.send("bye")
						sock.close() 
						del state[ipPortTuple] 
						clients.remove(sock)
						break
					
				if len(message) == 0 or len(message) < 1024 and result != "exit" and result != "recv ok":
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
			s.send("host " + c.getHostname() )
			print s.recv(1024)
			
			s.send("checkDataID 0 0")
			print "data:" +  str( s.recv(1024) )
			
			
			#s.send("data " + self.xml.logEntryToXml( monitorLog() ))
			#s.send("commit")
			#s.send("getLastID " + c.getHostname())
			#lastId = int( s.recv(1024) )
			#logs = d.getLogs( lastId)

			#for i in range(0, len(logs)):
			#	print i
			#	data = self.xml.logEntryToXml( c.getHostname(), logs[i] )
			#	print "Size of data: " + str(len(data))
			#	print "Send data, #bytes: " + str( s.sendall("data " + str(len(data)) + " " + data ))
			#	print "Answer to data:" +  s.recv(1024)
			#	s.send("commit")
			#	print "Answer to commit: " + s.recv(1024)


			s.send("exit")
			print s.recv(1024)
		finally: 
		    s.close()


if __name__ == '__main__':
	d = datenfresserMonitorClient()
