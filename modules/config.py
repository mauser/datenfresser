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
		
		self.__webserver = config.get("webserver","webserver_enabled")
		self.__webserver_port = config.get("webserver","webserver_port")
		
		try:
			self.__monitor = config.get("monitor","monitor_enabled")
		except ConfigParser.NoSectionError:
			self.__monitor = "false"

		try:
			self.__monitor_port = config.get("monitor","monitor_port")
		except ConfigParser.NoSectionError:
			self.__monitor_port = 0  


	def getDebug( self ):
		return self.__debug

	def getUsername( self ):
		return self.__username

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
	
	def getMonitorEnabled( self ):
		return self.__monitor
		
	def getMonitorPort( self ):
		return self.__monitor_port
		
		
	def getPollInterval( self ):
		return self.__poll_interval

	def getAutomaticShutdown( self ):
		return self.__automatic_shutdown
		
	def getSyncDir( self ):
		return self.__sync_dir




