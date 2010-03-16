#!/usr/bin/python
# -*- coding: utf-8 -*-

class dataContainer:
	''' a dataContainer represents the entrys in the main configuration file'''
	def __init__(self , dataID, name, comment, localPath, remotePath, dataType, options , schedule, group):
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
		



