#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib

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
		



