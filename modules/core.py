#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime

def log( string , level="normal" ):
	print string

	today = datetime.today()

	logfile = open("/var/log/datenfresser.log" , "a")
	logfile.write(today.isoformat() + "\t" + string + "\n"  )
	logfile.close()

class monitorLog:

	host ="example.org"
	start = 0
	end = 0
	dataId = 0
	remoteId = 0
	status = "no status available"
	error = "no error information available"
	transfered = 0

	classname = "monitorLog"

	def setTransferredData(self, v):
		self.transfered = v
	def getTranserredData(self):
		return self.transfered

	def setHost(self, h):
		self.host = h
	def getHost(self):
		return self.host

	def getDataId(self):
		return self.dataId
	def setDataId(self, v):
		self.dataId = v

	def setStartTimestamp(self, t):
		self.start = t
	def getStartTimestamp(self):
		return self.start

	def setEndTimestamp(self, t):
		self.end = t
	def getEndTimestamp(self):
		return self.end
	
	def setStatus(self, s):
		self.status = s
	def getStatus(self):
		return self.status

	def setError(self, e):
		self.error = e
	def getError(self):
		return self.error

	def setRemoteLogId(self, i):
		self.remoteId = i
	def getRemoteLogId(self):
		return self.remoteId


class dataContainer:
	''' a dataContainer represents the entrys in the main configuration file'''
	def __init__(self , dataID=0, name="", comment="", localPath="", remotePath="", dataType="rsync", options="" , schedule="", group=""):
		self.name =  name
		self.localPath = localPath
		self.remotePath = remotePath
		self.type = dataType
		self.schedule = schedule
		self.group = group
		self.options = options
		self.lastBackup = 0
		self.comment = comment
		self.dataID = dataID
		self.archive = ""
		self.archive_ttl = ""
		self.archive_method = ""
		self.compress = ""
		self.volume = ""

		#not used at the moment
		self.pre_command = ""
		self.post_command = ""

		self.classname = "dataContainer"


	def updateChecksum(self):
		algo = hashlib.sha1()
		string =  self.name + self.localPath + self.remotePath  + self.schedule + self.options + self.comment 
		algo.update(string)
		self.checksum = algo.hexdigest()


class job:
    def __init__( self, dataID , startTimestamp , name ):
	    self.name = name
	    self.dataID = dataID
	    self.startTimestamp = startTimestamp
	    
	    
class logEntry:
    def __init__( self, logID, type, dataID , startTimestamp , endTimestamp ,  status, errorMessage ):
	    self.logID = logID
	    self.dataID = dataID
	    self.type = type
	    self.startTimestamp = startTimestamp
	    self.endTimestamp = endTimestamp
	    self.status = status
	    self.errorMessage = errorMessage
	    
class metaData:
	''' This class contains data which belongs do datacontainers but is not stored in the configuration file'''
	def __init__(self):
		#Timestamp of last performed backup
		self.lastBackup = 0
		



