import ConfigParser
import os
import sys
import cPickle

sys.path.append("/usr/lib/datenfresser/modules")

from core import dataContainer

from rsync import rsyncData

CONFIG_FILENAME='/etc/datenfresser.conf'


class config:


	def getDataContainer(self):
			
		config = ConfigParser.ConfigParser()
		config.readfp(open(CONFIG_FILENAME))
	
		containerList = []

		for account in config.sections():
			if account == "main": continue
					
			try: 
				localPath = config.get(account,"localPath")
			except Exception:
				print "No localPath found"
				continue
		
			try:
				remotePath = config.get(account,"remotePath")
			except Exception:
				print "No remotePath found"
				continue
	
			try:
				schedule = config.get(account,"schedule")
			except Exception:
				schedule = "weekly"

			try:
				method = config.get(account,"method")
			except Exception:
				method = "rsync"

			try: 
				group = config.get(account,"group")
			except Exception:
				group = ""

			typeData = None

			if method == "rsync":
				try:
					rsyncUser = config.get(account,"rsyncUser")
				except Exception:
					rsyncUser = "backup"

				try:
					rsyncPort = config.get(account,"rsyncPort")
				except Exception:
					rsyncPort = 22	

				typeData = rsyncData(rsyncPort,rsyncUser)
				
		
			tmp =  dataContainer(account,localPath,remotePath,method,schedule,group,typeData)
		 	containerList.append(tmp)
		return containerList
	
	def getMainSection(self):

		'''read config file and create database entries'''
		if not os.path.isfile(CONFIG_FILENAME):
			self.init_configuration();
			
		config = ConfigParser.ConfigParser()
		config.readfp(open(CONFIG_FILENAME))
		for account in config.sections():
			if account == "main":
				try:
					persistentDataPath=config.get(account,persistentDataPath)
				except Exception:
					persistentDataPath="/var/datenfresser/pickledData"
				self.persistentDataPath = persistentDataPath 


			


	
	def __init__(self):
		"""Class for Configuration Managment"""
		#parse config file
		config = ConfigParser.ConfigParser()
		if not os.path.isfile(CONFIG_FILENAME):
			self.init_configuration();
				

		config.readfp(open(CONFIG_FILENAME))
		self.base_dir="/usr/share/datenfresser"

		self.persistentDataPath=""
		self.getMainSection()	
