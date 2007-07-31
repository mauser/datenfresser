#!/usr/bin/python

import os
from os.path import isdir


class dataContainer:
	''' a dataContainer represents the entrys in the main configuration file'''
	def __init__(self,name,localPath, remotePath,dataType,schedule,group,typeData):
		self.name =  name
		self.localPath = localPath
		self.localPath = localPath
		self.remotePath = remotePath
		self.method = dataType
		self.schedule = schedule
		self.group = group
		self.typeData = typeData
		self.lastBackup = 0
		self.lock = False

class metaData:
	''' This class contains data which belongs do datacontainers but is not stored in the configuration file'''
	def __init__(self):
		#Timestamp of last performed backup
		self.lastBackup = 0
		
		#lock is true if this container is in use 
		self.lock = False

