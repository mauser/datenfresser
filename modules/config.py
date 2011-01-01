# -*- coding: utf-8 -*-
import ConfigParser
import getopt

import os
import sys

class config:

	__configHash={}

	def __init__(self):
		"""Class for Configuration Managment"""
	
		self.__username = ""
		self.__main_volume = ""

		config = ConfigParser.ConfigParser()
		config.readfp(open('/etc/datenfresser.conf'))
		
		self.__main_volume = config.get("main","mainVolume")
		self.__db_location = config.get("main","db_location")
		self.__poll_interval = config.get("main","poll_interval")
		self.__automatic_shutdown = config.get("main","automatic_shutdown")
		self.__sync_dir=config.get("main","sync_dir")
		self.__start_delay=config.get("main","start_delay")
		self.__debug=config.get("main","debug")
		self.__username=config.get("main","username")	
		self.__hostname=config.get("main","hostname")	
		
		self.__webserver = config.get("webserver","webserver_enabled")
		self.__webserver_port = config.get("webserver","webserver_port")
		
		try:
			self.__monitorClientEnabled = config.get("monitoring","monitorClient_enabled")
		except ConfigParser.NoSectionError:
			self.__monitorClientEnabled = "false"
			self.__remoteMonitorPort = 0 
			self.__remoteMonitorUser = ""
			self.__remoteMonitorPassword = ""

		
		try:
			self.__monitorServerEnabled = config.get("monitoring","monitorServer_enabled")
		except ConfigParser.NoSectionError:
			self.__monitorServerEnabled = "false"
			self.__localMonitorPort = 0 
			self.__localMonitorUser = ""
			self.__localMonitorPassword = ""

		try:
			self.__localMonitorPort = config.get("monitoring","localMonitorPort")
		except ConfigParser.NoOptionError:
			self.__localMonitorPort = 0 

		try:
			self.__localMonitorUser = config.get("monitoring","localMonitorUser")
		except ConfigParser.NoOptionError:
			self.__localMonitorUser = ""
		
		try:
			self.__localMonitorPassword = config.get("monitoring","localMonitorPassword")
		except ConfigParser.NoOptionError:
			self.__localMonitorPassword = ""

		try:
			self.__remoteMonitorServer = config.get("monitoring","remoteMonitorServer")
		except ConfigParser.NoOptionError:
			self.__remoteMonitorServer = ""

		try:
			self.__remoteMonitorPort = config.get("monitoring","remoteMonitorPort")
		except ConfigParser.NoOptionError:
			self.__remoteMonitorPort = 0 

		try:
			self.__remoteMonitorUser = config.get("monitoring","remoteMonitorUser")
		except ConfigParser.NoOptionError:
			self.__remoteMonitorUser = ""
		
		try:
			self.__remoteMonitorPassword = config.get("monitoring","remoteMonitorPassword")
		except ConfigParser.NoOptionError:
			self.__remoteMonitorPassword = ""



	def getDebug( self ):
		return self.__debug

	def getUsername( self ):
		return self.__username
	
	def getHostname( self ):
		return self.__hostname


	def getStartDelay( self ):
		return self.__start_delay

	def getMainVolume( self ):
		return self.__main_volume

	def getDbLocation( self ):
		return self.__db_location
	
	def getWebserverEnabled( self ):
		return self.__webserver
		
	def getWebserverPort( self ):
		return self.__webserver_port



	def getMonitorServerEnabled( self ):
		return self.__monitorServerEnabled

	def getRemoteMonitorUser( self ):
		return self.__remoteMonitorUser

	def detRemoteMonitorServer(self):
		return self.__remoteMonitorServer

	def getRemoteMonitorPassword( self ):
		return self.__remoteMonitorPassword
		
	def getRemoteMonitorPort( self ):
		return self.__remoteMonitorPort


	def getMonitorClientEnabled( self ):
		return self.__monitorClientEnabled

	def getLocalMonitorUser( self ):
		return self.__localMonitorUser

	def getLocalMonitorPassword( self ):
		return self.__localMonitorPassword
		
	def getLocalMonitorPort( self ):
		return self.__localMonitorPort




		
		
	def getPollInterval( self ):
		return self.__poll_interval

	def getAutomaticShutdown( self ):
		return self.__automatic_shutdown
		
	def getSyncDir( self ):
		return self.__sync_dir


class CliArguments:
	def __init__( self ):
		self.monitor = False
		self.verbose = False




