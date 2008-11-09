#!/usr/bin/python

class dataContainer:
	''' a dataContainer represents the entrys in the main configuration file'''
	def __init__(self , name, localPath, remotePath, comment, dataType, options , schedule, group):
		self.name =  name
		self.localPath = localPath
		self.remotePath = remotePath
		self.type = dataType
		self.schedule = schedule
		self.group = group
		self.options = options
		self.lastBackup = 0

class metaData:
	''' This class contains data which belongs do datacontainers but is not stored in the configuration file'''
	def __init__(self):
		#Timestamp of last performed backup
		self.lastBackup = 0
		



